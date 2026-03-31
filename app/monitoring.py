import json
import logging
import os
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

logger = logging.getLogger("llm_monitor")


# -----------------------------
# Custom LLM Monitoring Handler
# -----------------------------
class LLMMonitoringHandler(BaseCallbackHandler):
    """Logs every LLM call's inputs, outputs, token usage, and errors."""

    def __init__(self):
        self.runs: dict[str, dict] = {}

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Capture text-completion model inputs."""
        self.runs[str(run_id)] = {
            "type": "llm",
            "model": serialized.get("kwargs", {}).get("model_name", "unknown"),
            "input_prompts": prompts,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "tags": tags or [],
            "metadata": metadata or {},
        }
        logger.info(
            "LLM call started | run_id=%s model=%s",
            run_id,
            self.runs[str(run_id)]["model"],
        )

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Capture chat model inputs (ChatOpenAI via OpenRouter)."""
        self.runs[str(run_id)] = {
            "type": "chat_model",
            "model": serialized.get("kwargs", {}).get("model_name", "unknown"),
            "input_messages": [
                [{"role": m.type, "content": m.content} for m in msg_list]
                for msg_list in messages
            ],
            "start_time": datetime.now(timezone.utc).isoformat(),
            "tags": tags or [],
            "metadata": metadata or {},
        }
        logger.info(
            "Chat model call started | run_id=%s model=%s messages=%d",
            run_id,
            self.runs[str(run_id)]["model"],
            sum(len(msg_list) for msg_list in messages),
        )

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, **kwargs: Any) -> None:
        """Capture output completions and token usage."""
        run_data = self.runs.get(str(run_id), {})
        run_data["end_time"] = datetime.now(timezone.utc).isoformat()

        # Extract generated text
        run_data["output_generations"] = [
            [{"text": gen.text, "info": gen.generation_info} for gen in gen_list]
            for gen_list in response.generations
        ]

        # Extract token usage
        llm_output = response.llm_output or {}
        token_usage = llm_output.get("token_usage", {})
        run_data["token_usage"] = token_usage
        run_data["model_name"] = llm_output.get("model_name", run_data.get("model"))

        logger.info(
            "LLM call completed | run_id=%s model=%s tokens=%s",
            run_id,
            run_data.get("model_name", "unknown"),
            json.dumps(token_usage, default=str),
        )

        self.runs.pop(str(run_id), None)

    def on_llm_error(
        self, error: BaseException, *, run_id: UUID, **kwargs: Any
    ) -> None:
        """Capture LLM errors for debugging."""
        run_data = self.runs.get(str(run_id), {})
        run_data["error"] = str(error)
        run_data["error_type"] = type(error).__name__
        run_data["end_time"] = datetime.now(timezone.utc).isoformat()

        logger.error(
            "LLM call failed | run_id=%s error_type=%s error=%s",
            run_id,
            type(error).__name__,
            error,
        )

        self.runs.pop(str(run_id), None)


# -----------------------------
# Callback Factory
# -----------------------------
def get_callbacks() -> list[BaseCallbackHandler]:
    """
    Build the list of callback handlers based on environment configuration.

    Always includes the custom LLMMonitoringHandler.
    Optionally includes Langfuse if LANGFUSE_PUBLIC_KEY is set.
    """
    callbacks: list[BaseCallbackHandler] = [LLMMonitoringHandler()]

    # Langfuse integration (if configured)
    if os.getenv("LANGFUSE_PUBLIC_KEY"):
        try:
            from langfuse.langchain import CallbackHandler as LangfuseHandler

            langfuse_handler = LangfuseHandler()
            callbacks.append(langfuse_handler)
            logger.info("Langfuse monitoring enabled")
        except ImportError:
            logger.warning(
                "LANGFUSE_PUBLIC_KEY is set but langfuse package is not installed. "
                "Install with: pip install langfuse"
            )

    return callbacks
