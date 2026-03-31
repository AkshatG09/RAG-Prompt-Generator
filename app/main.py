import logging
from contextlib import asynccontextmanager

from app import database, services
from app.models import HistoryResponse, PromptRequest, PromptResponse
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------
# Lifespan (startup/shutdown)
# ---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    logger.info("🚀 Starting API - Connecting to databases")

    await database.connect_to_mongo()
    database.connect_to_chroma()

    logger.info("✅ Databases connected")

    from app.monitoring import get_callbacks

    active_callbacks = get_callbacks()
    callback_names = [type(cb).__name__ for cb in active_callbacks]
    logger.info("📊 LLM monitoring initialized with: %s", callback_names)

    yield

    # Shutdown
    logger.info("🛑 Shutting down API")

    await database.close_mongo_connection()

    logger.info("🔌 MongoDB connection closed")


# ---------------------------
# FastAPI App
# ---------------------------
app = FastAPI(title="Prompt Engineer RAG API", version="1.0.0", lifespan=lifespan)

# ---------------------------
# CORS Middleware
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# Health Check Endpoint
# ---------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------------------------
# Prompt Generation Endpoint
# ---------------------------
@app.post("/api/generate", response_model=PromptResponse)
async def generate_prompt_endpoint(request: PromptRequest):

    try:
        result = await services.generate_final_prompt(request)

        return PromptResponse(
            generated_prompt=result["prompt"],
            retrieved_context_used=[result["context"]],
        )

    except Exception as e:
        logger.exception("Prompt generation failed")

        raise HTTPException(status_code=500, detail="Failed to generate prompt.")


# ---------------------------
# History Endpoint
# ---------------------------
@app.get("/api/history/{user_id}", response_model=HistoryResponse)
async def get_history(user_id: str, limit: int = 30, offset: int = 0):

    try:
        result = await services.get_paginated_history(user_id, limit, offset)
        return result

    except Exception as e:
        logger.exception("History retrieval failed")
        raise HTTPException(status_code=500, detail="Failed to retrieve history.")
