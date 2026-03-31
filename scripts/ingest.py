import os
import uuid
from typing import List

import chromadb
from dotenv import load_dotenv
from markdown_chunker import MarkdownChunkingStrategy
from openai import OpenAI

# Load environment variables
load_dotenv()

# ----------------------------
# OpenRouter Client
# ----------------------------
_raw_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

try:
    from langsmith.wrappers import wrap_openai

    client = wrap_openai(_raw_client)
except ImportError:
    client = _raw_client

# ----------------------------
# ChromaDB Initialization
# ----------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(name="prompt_guidelines")


# ----------------------------
# Chunking Function
# ----------------------------
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# ----------------------------
# Batch Embedding Function
# ----------------------------
def get_embeddings(texts):

    formatted_input = [{"content": [{"type": "text", "text": text}]} for text in texts]

    response = client.embeddings.create(
        model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
        input=formatted_input,
        encoding_format="float",
    )

    return [item.embedding for item in response.data]


# ----------------------------
# Document Processing
# ----------------------------
def process_and_store_document(filepath: str):

    print(f"\nReading document: {filepath}")

    # Read file
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"Document length: {len(text)} characters")

    # Chunk document
    strategy = MarkdownChunkingStrategy(
        min_chunk_len=500,
        soft_max_len=2000,
        hard_max_len=5000,
        detect_headers_footers=False,
        remove_duplicates=False,
        add_metadata=True,
    )

    chunks = strategy.chunk_markdown(text)

    documents = []

    for chunk in chunks:
        # chunk may contain metadata or be plain string
        chunk_text = chunk.text if hasattr(chunk, "text") else str(chunk)

        chunk_text = chunk_text.strip()

        if chunk_text:
            documents.append(chunk_text)

    print(f"Generated {len(documents)} semantic chunks")

    # Generate embeddings in batches
    embeddings = get_embeddings(chunks)

    # Generate unique IDs
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Store in Chroma
    collection.add(embeddings=embeddings, documents=chunks, ids=ids)

    print(f"\n✅ Ingestion complete!")
    print(f"Stored {len(chunks)} chunks in ChromaDB")


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    process_and_store_document(
        r"C:\Users\aksha\Documents\makerCheckerAgent\source_documents\proccessed_documents\better-writer-handbook-and-tutorials(proccessed).md"
    )
