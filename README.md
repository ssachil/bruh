# Enterprise Data Ingestion Pipeline

A powerful data ingestion pipeline for processing various document types and extracting structured information for enterprise data visualization.

## Features

- Support for multiple document types (PDF, CSV, TXT)
- Advanced entity extraction using spaCy
- RESTful API interface
- Entity type classification
- Context preservation
- Confidence scoring

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy language model:
```bash
python -m spacy download en_core_web_lg
```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /upload
Upload a document for entity extraction.

Example using curl:
```bash
curl -X POST -F "file=@your_document.pdf" http://localhost:8000/upload
```

### GET /health
Health check endpoint.

## Response Format

The `/upload` endpoint returns a list of entities in the following format:
```json
[
  {
    "name": "Entity Name",
    "type": "Entity Type",
    "source_file": "original_filename.pdf",
    "confidence": 0.95,
    "context": "Surrounding text context..."
  }
]
```

## Supported Entity Types

- Person
- Organization
- Location
- Date
- Event
- Product
- Law
- Work of Art

## Development

To add support for new document types or entity types, modify the respective processor classes in:
- `document_processor.py`
- `entity_extractor.py` 