# RAG Service

Python FastAPI service providing RAG capabilities for the Component AI Agent.

## Features

- **ChromaDB Vector Store**: Persistent vector storage for component embeddings
- **Sentence Transformers**: Local embedding generation using HuggingFace models
- **Semantic Search**: Find components by description or functionality
- **REST API**: FastAPI-based REST endpoints
- **Component CRUD**: Full component lifecycle management

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 8765

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8765
```

## API Endpoints

### Health Check
- `GET /api/health` - Check service health

### Search
- `POST /api/search` - Semantic component search
- `POST /api/search/suggest` - Suggest components for UI

### Components
- `GET /api/components` - List all components
- `GET /api/components/{id}` - Get component by ID
- `GET /api/components/name/{name}` - Get components by name
- `POST /api/components` - Create component
- `PUT /api/components/{id}` - Update component
- `DELETE /api/components/{id}` - Delete component

### Scanning
- `POST /api/scan` - Scan component folder (coming soon)

## Configuration

Create a `.env` file or set environment variables:

```env
CHROMA_PERSIST_DIRECTORY=./chroma_data
CHROMA_COLLECTION_NAME=components
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Development

```bash
# Format code
black src/

# Lint code
ruff check src/

# Run tests
pytest
```

## Architecture

```
src/
├── main.py              # FastAPI app entry point
├── api/                 # API routes and models
├── rag/                 # RAG pipeline components
├── db/                  # Database and vector store
├── intelligence/        # Component scanning and parsing
└── config/              # Configuration
```

