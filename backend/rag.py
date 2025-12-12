from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constants import VECTOR_DB_PATH
import lancedb

vector_db = lancedb.connect(uri=VECTOR_DB_PATH)

YOUTUBER_PERSONA = (
    "You are The Youtuber - a passionate educator who teaches hundreds through video tutorials. "
    "You also happen to be an expert in Data Engineering. "
    "You have a friendly, joyful and enthusiastic teaching style and love helping people learn data engineering. "
    "Always answer based on the retrieved video transcript knowledge, but you can mix in your expertise to make the answer more coherent. "
    "Don't hallucinate; if the user prompts outside the retrieved knowledge, politely say so. "
    "Keep the answer clear and concise, max 6 sentences. "
    "Always describe which file you used as source."
)

rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=YOUTUBER_PERSONA,
    output_type=RagResponse,
)

@rag_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching video transcripts to the query
    """
    results = vector_db["transcripts"].search(query=query).limit(k).to_list()
    top_result = results[0]

    return f"""
    Video Title: {top_result["filename"]},
    Filepath: {top_result["filepath"]},
    Content: {top_result["content"]}
    """