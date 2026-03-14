# 🎯 LLM Prompt Generator RAG API

A FastAPI-based Retrieval-Augmented Generation (RAG) application designed to automatically generate highly optimized LLM prompts and system prompts. By leveraging a custom knowledge base of prompt engineering best practices, this API tailors prompts to specific user requests and professional specializations.

## ✨ Features Implemented

* **Custom Knowledge Base Ingestion:** A standalone ingestion pipeline to process raw `.txt` files containing prompt engineering guidelines, chunk the data, and store vector representations.
* **Semantic Retrieval (RAG):** Utilizes similarity search to fetch the most relevant prompt engineering techniques based on the user's specific use case.
* **Context-Aware Generation:** Combines the user's request, their specified professional specialization, and the retrieved best practices to generate a highly tailored prompt.
* **Conversation Memory:** Asynchronously logs all user interactions, requests, and generated prompts to a database for auditing, continuous context, and future fine-tuning.
* **Modular Architecture:** Clean, scalable FastAPI project structure separating database connections, Pydantic schemas, and core RAG logic.

## 🛠️ Technical Specifications

* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Local persistent storage)
* **NoSQL Database:** [MongoDB](https://www.mongodb.com/) (Accessed asynchronously via `motor`)
* **LLM Gateway:** [OpenRouter](https://openrouter.ai/)
* **Embedding Model:** `nvidia/llama-nemotron-embed-vl-1b-v2:free` (via OpenRouter)
* **Generation Model:** `qwen/qwen3.5-9b` (via OpenRouter)

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ installed and a running instance of MongoDB (either locally or via MongoDB Atlas).

### 2. Installation
Clone the repository and install the required dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

*(Note: Ensure your `requirements.txt` includes `fastapi`, `uvicorn`, `openai`, `chromadb`, `motor`, `pydantic`, and `python-dotenv`)*

### 3. Environment Variables
Create a `.env` file in the root directory and add your credentials:
\`\`\`env
OPENROUTER_API_KEY="your_openrouter_api_key_here"
MONGO_URI="mongodb://localhost:27017" # Or your Atlas connection string
\`\`\`

### 4. Data Ingestion
Place your prompt engineering guidelines into `./source_documents` and run the ingestion script to populate ChromaDB:
\`\`\`bash
python ingest.py
\`\`\`

### 5. Run the API
Start the FastAPI server:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`
Access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## 🗺️ Future Plans (Roadmap)

* **Prompt vs. System Prompt Segregation:** Update the generation logic to explicitly output distinct, clearly separated System Prompts (instructions) and User Prompts (inputs).
* **Expansion of Specializations:** Incorporate distinct `.txt` knowledge bases and logic handling for a wider array of professions (e.g., Legal, Medical, Readme).
* **User Interface (UI):** Develop a frontend application (using Streamlit) to make the tool accessible to non-technical users.
* **Custom Data Ingestions:** Allow users to upload their own `.txt` or `.pdf` files dynamically via the API to create highly personalized prompt knowledge bases.
