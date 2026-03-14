import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app import database, services
from app.models import PromptRequest, PromptResponse

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
