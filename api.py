from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.data_models import Prompt, RagResponse, History
from backend.rag import rag_agent
import asyncio

app = FastAPI(title="RAG API")

# allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# memory storage
chat_history: list[History] = []
rag_cache = {}  # Caching dictionary


# casched rag
async def cached_rag(prompt: str) -> RagResponse:
    """Return cached result or compute and store new one."""
    if prompt in rag_cache:
        return rag_cache[prompt]

    result = await rag_agent.run(prompt)  # IMPORTANT: async/await, NOT asyncio.run()

    rag_cache[prompt] = result.output
    return result.output


# query endpoint
@app.post("/rag/query", response_model=RagResponse)
async def query_documentation(query: Prompt):
    global chat_history

    chat_history.append(History(role="user", content=query.prompt))

    result = await cached_rag(query.prompt)

    chat_history.append(History(role="assistant", content=result.answer))

    return result


# hostory endpoint
@app.get("/rag/history")
async def get_history():
    return chat_history


# reset endpoint
@app.post("/rag/reset")
async def reset_chat():
    global chat_history, rag_cache
    chat_history.clear()
    rag_cache.clear()
    return {"status": "history cleared"}

