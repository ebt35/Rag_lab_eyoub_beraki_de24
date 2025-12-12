from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name= "gemini-embedding-001")

EMBEDDINNG_DIM = 3072

class Transcript(LanceModel):
    doc_id: str
    filepath: str 
    filename: str = Field(description="the stem of the file, i. e without the suffix ")
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDINNG_DIM) = embedding_model.VectorField()
    
class Prompt(BaseModel):
    prompt: str = Field(description="prompt from user")
    
class RagResponse(BaseModel):
    filename: str = Field(description="filename of retrieved filepath without suffix")
    filepath: str = Field(description= "absolute path to retrieved file")
    answer: str = Field(description="answer based retrieved file")

