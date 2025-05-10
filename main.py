from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from document_processor import DocumentProcessor
from entity_extractor import EntityExtractor

app = FastAPI(title="Enterprise Data Ingestion Pipeline")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
doc_processor = DocumentProcessor()
entity_extractor = EntityExtractor()

class Entity(BaseModel):
    name: str
    type: str
    source_file: str
    confidence: float
    context: Optional[str] = None

@app.post("/upload", response_model=List[Entity])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and extract entities from it.
    """
    # Process the document
    content = await doc_processor.process_file(file)
    
    # Extract entities
    entities = entity_extractor.extract_entities(content, file.filename)
    
    return entities

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 