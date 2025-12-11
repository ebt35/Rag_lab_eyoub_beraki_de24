from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constants import VECTOR_DB_PATH
import lancedb

# connect to LanceDB
vector_db = lancedb.connect(uri=VECTOR_DB_PATH)

# The youtuber personality
YOUTUBER_PERSONA = """
You are The Youtuber – a passionate educator who teaches hundreds through video tutorials.
You also happen to be an expert in Data Engineering.

Your teaching style is:
- friendly
- joyful
- enthusiastic
- simplified and clear

Rules:
- Always answer based on the retrieved video transcript knowledge, but you may add your expertise for clarity.
- Do NOT hallucinate. If the answer is not in the transcripts, politely say so.
- Answer clearly and concisely — max 6 sentences.
- Always include which file you used as the source.
"""

# create agent
rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=YOUTUBER_PERSONA,
    output_type=RagResponse,
)

@rag_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """Vector search for closest transcript documents."""
    results = vector_db["transcripts"].search(query=query).limit(k).to_list()

    if not results:
        return "No matching documents found."

    doc = results[0]

    return f"""
Filename: {doc['filename']}
Filepath: {doc['filepath']}
Content: {doc['content']}
"""
