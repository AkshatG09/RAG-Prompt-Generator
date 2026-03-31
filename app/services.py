import os
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai import OpenAI

from app import database
from app.models import PromptRequest
from app.monitoring import get_callbacks

load_dotenv()

# -----------------------------
# LangChain Chat Model (OpenRouter)
# -----------------------------
llm = ChatOpenAI(
    model="qwen/qwen3.5-9b",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# -----------------------------
# Raw OpenAI Client for Embeddings
# -----------------------------
embedding_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2:free"


# -----------------------------
# Embedding Function
# -----------------------------
def get_embedding(text: str) -> list[float]:
    """Calls OpenRouter to get vector embeddings for the given text."""

    formatted_input = [{"content": [{"type": "text", "text": text}]}]

    response = embedding_client.embeddings.create(
        model=EMBEDDING_MODEL, input=formatted_input, encoding_format="float"
    )

    return response.data[0].embedding


# -----------------------------
# RAG Retrieval
# -----------------------------
def retrieve_guidelines(query_text: str, n_results: int = 3) -> str:
    """Embeds the query and fetches relevant chunks from ChromaDB."""

    query_embedding = get_embedding(query_text)

    results = database.chroma_collection.query(
        query_embeddings=[query_embedding], n_results=n_results
    )

    documents = results.get("documents", [[]])[0]

    return "\n\n".join(documents)


# -----------------------------
# MongoDB History Retrieval
# -----------------------------
async def get_user_history(user_id: str) -> list[dict]:
    """Fetches past conversations for this user from MongoDB."""

    collection = database.mongo_db["conversations"]

    cursor = collection.find({"user_id": user_id}).sort("timestamp", -1).limit(5)

    history = []

    async for doc in cursor:
        history.append(
            {
                "user_request": doc["user_request"],
                "generated_prompt": doc["generated_prompt"],
            }
        )

    return history


# -----------------------------
# MongoDB Save Interaction
# -----------------------------
async def save_interaction(
    user_id: str, user_request: str, generated_prompt: str, retrieved_context: list[str]
):
    """Saves the user request and generated prompt to MongoDB."""

    collection = database.mongo_db["conversations"]

    document = {
        "user_id": user_id,
        "user_request": user_request,
        "generated_prompt": generated_prompt,
        "retrieved_context": retrieved_context,
        "timestamp": datetime.now(),
    }

    await collection.insert_one(document)


# -----------------------------
# Main Orchestration
# -----------------------------
async def generate_final_prompt(request: PromptRequest) -> dict:
    """Main orchestration logic for prompt generation."""

    guidelines_context = retrieve_guidelines(request.request_description)

    user_history = await get_user_history(request.user_id)

    history_text = ""

    if user_history:
        history_text = "\n\nPrevious interactions:\n"
        for item in user_history:
            history_text += f"""
User request: {item["user_request"]}
Generated prompt: {item["generated_prompt"]}
"""

    system_content = f"""
You are an expert prompt engineer.

Use the following guidelines to generate high-quality prompts.

Guidelines:
{guidelines_context}
"""

    user_content = f"""
User specialization: {request.specialization}

User request:
{request.request_description}

{history_text}

Generate a high-quality prompt the user can use with an LLM.
Return only the final prompt.
"""

    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=user_content),
    ]

    response = llm.invoke(
        messages,
        config={
            "callbacks": get_callbacks(),
            "metadata": {
                "user_id": request.user_id,
                "specialization": request.specialization,
            },
            "tags": ["prompt-generation", "rag"],
        },
    )

    generated_prompt = response.content.strip()

    await save_interaction(
        request.user_id,
        request.request_description,
        generated_prompt,
        [guidelines_context],
    )

    return {"prompt": generated_prompt, "context": guidelines_context}
