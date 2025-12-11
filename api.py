from fastapi import FastAPI
from backend.rag import rag_agent
from backend.data_models import Prompt, History, RagResponse
from typing import List

app = FastAPI()

chat_history: List[History] = []


@app.post("/rag/query", response_model=RagResponse)
async def query_documentation(query: Prompt):
    global chat_history

    chat_history.append(History(role="user", content=query.prompt))

    message_history = [
        {"role": h.role, "content": h.content}
        for h in chat_history
    ]

    result = await rag_agent.run(
        query.prompt,
        message_history=message_history,
    )

    answer = result.output.answer
    chat_history.append(History(role="assistant", content=answer))

    return result.output


@app.get("/rag/history", response_model=List[History])
async def get_history():
    return chat_history


@app.post("/rag/reset")
async def reset_chat():
    global chat_history
    chat_history = []
    return {"status": "history cleared"}
