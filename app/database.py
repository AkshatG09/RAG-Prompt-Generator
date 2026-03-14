import os

import chromadb
from motor.motor_asyncio import AsyncIOMotorClient

# Globals initialized during FastAPI startup
mongo_client = None
mongo_db = None

chroma_client = None
chroma_collection = None


# -------------------------
# MongoDB Connection
# -------------------------
async def connect_to_mongo():
    global mongo_client, mongo_db

    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable not set")

    mongo_client = AsyncIOMotorClient(mongo_uri)

    # database name
    mongo_db = mongo_client["rag_prompts_db"]

    print("✅ Connected to MongoDB")


async def close_mongo_connection():
    global mongo_client

    if mongo_client:
        mongo_client.close()
        print("🔌 MongoDB connection closed")


# -------------------------
# ChromaDB Connection
# -------------------------
def connect_to_chroma():
    global chroma_client, chroma_collection

    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    chroma_collection = chroma_client.get_or_create_collection(name="prompt_guidelines")

    print("✅ Connected to ChromaDB")
