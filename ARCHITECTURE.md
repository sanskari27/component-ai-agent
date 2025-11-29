# Architecture Overview

## System Architecture

The Component AI Agent is built as a distributed system with three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                        VS Code IDE                          │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Copilot   │  │  Extension   │  │   Sidebar UI    │  │
│  │    Chat     │◄─┤   Backend    │◄─┤   (Webview)     │  │
│  └─────────────┘  └──────────────┘  └─────────────────┘  │
│         ▲              │                      │             │
└─────────┼──────────────┼──────────────────────┼─────────────┘
          │              │                      │
          │              ▼                      ▼
          │         HTTP Client           Component
          │              │                   Manager
          │              │                      │
          └──────────────┼──────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │     RAG Service (Python)     │
          │                              │
          │  ┌─────────┐  ┌───────────┐ │
          │  │   API   │  │    RAG    │ │
          │  │ Routes  │─►│  Pipeline │ │
          │  └─────────┘  └───────────┘ │
          │       │            │         │
          │       ▼            ▼         │
          │  ┌─────────┐  ┌───────────┐ │
          │  │Scanner/ │  │ Embedding │ │
          │  │  Parser │  │  Service  │ │
          │  └─────────┘  └───────────┘ │
          │                    │         │
          └────────────────────┼─────────┘
                               ▼
                    ┌──────────────────┐
                    │    ChromaDB      │
                    │ (Vector Storage) │
                    └──────────────────┘
```

## Component Details

### 1. VS Code Extension Layer

#### Copilot Agent (`copilot/agent.ts`)
- Registers as `@components` chat participant
- Handles natural language queries
- Routes requests to appropriate handlers
- Formats responses with code examples

#### Extension Backend (`extension.ts`)
- Manages extension lifecycle
- Starts/stops RAG service
- Handles commands
- Coordinates between UI and service

#### Sidebar UI (`sidebar/provider.ts`)
- Webview-based component browser
- Search and filter components
- CRUD operations
- Real-time updates

#### RAG Client (`rag-client/client.ts`)
- HTTP client for RAG service
- Request/response handling
- Error management
- Health checking

### 2. RAG Service Layer

#### API Routes (`api/routes/`)
- **search.py**: Semantic search endpoints
- **components.py**: Component CRUD operations
- **scan.py**: Folder scanning endpoint

#### RAG Pipeline (`rag/pipeline.py`)
- Orchestrates search and retrieval
- Component indexing
- Query processing
- Result ranking

#### Embedding Service (`rag/embeddings.py`)
- Generates embeddings using Sentence Transformers
- Model: all-MiniLM-L6-v2 (384 dimensions)
- Supports batch processing

#### Vector Store (`db/vector_store.py`)
- ChromaDB wrapper
- Persistent storage
- Similarity search
- Metadata filtering

#### Component Intelligence (`intelligence/`)
- **ast_parser.py**: Parse TypeScript/React files
- **storybook_parser.py**: Extract Storybook examples
- **metadata_extractor.py**: Generate component metadata
- **component_scanner.py**: Folder scanning and indexing

### 3. Data Flow

#### Indexing Flow
```
Component Folder
     │
     ▼
Scanner ──► AST Parser ──► Metadata Extractor
     │                           │
     ▼                           ▼
Storybook Parser            Component Data
     │                           │
     └───────────┬───────────────┘
                 ▼
          Embedding Service
                 │
                 ▼
            Vector Store
```

#### Search Flow
```
User Query (Copilot Chat)
     │
     ▼
Copilot Agent
     │
     ▼
RAG Client (HTTP)
     │
     ▼
Search Endpoint
     │
     ▼
Embedding Service (Query)
     │
     ▼
Vector Store (Similarity Search)
     │
     ▼
RAG Pipeline (Re-ranking)
     │
     ▼
Search Results
     │
     ▼
Formatted Response (Markdown)
     │
     ▼
Copilot Chat UI
```

## Technology Stack

### Frontend (Extension)
- **Language**: TypeScript
- **Framework**: VS Code Extension API
- **UI**: Webview with vanilla HTML/CSS/JS
- **HTTP Client**: Axios
- **Build**: Webpack

### Backend (RAG Service)
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers
- **Server**: Uvicorn (ASGI)

### Shared
- **Types**: TypeScript definitions
- **Protocol**: HTTP/REST
- **Format**: JSON

## Design Patterns

### 1. Repository Pattern
- Vector store abstraction
- Pluggable storage backend

### 2. Service Layer
- RAG pipeline
- Embedding service
- Component scanner

### 3. Factory Pattern
- Singleton services
- Client instances

### 4. Observer Pattern
- Webview messaging
- Component updates

### 5. Strategy Pattern
- Search strategies
- Parsing strategies

## Scalability Considerations

### Current Limits
- Single-node deployment
- Local vector storage
- In-memory caching

### Future Scaling
- Distributed ChromaDB
- Redis caching
- Load balancing
- Horizontal scaling

## Security

### Current
- Local-only by default
- No external API calls
- Isolated Python process
- Sandboxed webview

### Best Practices
- Input validation
- Path sanitization
- CORS configuration
- Error handling

## Performance

### Optimization Strategies
1. **Embedding caching**: Reuse embeddings
2. **Batch processing**: Process multiple files
3. **Lazy loading**: Load components on demand
4. **Debouncing**: Throttle search requests
5. **Pagination**: Limit result sets

### Bottlenecks
1. Initial embedding generation
2. Large folder scanning
3. AST parsing for large files
4. Vector search at scale

## Extension Points

### Custom Parsers
Add new parsers in `intelligence/`:
```python
class CustomParser:
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        # Custom parsing logic
        pass
```

### Custom Embeddings
Configure different models:
```python
embedding_model = "sentence-transformers/all-mpnet-base-v2"
```

### Custom Tools
Add Copilot tools:
```typescript
export const customTool: CopilotTool = {
  name: 'customAction',
  handler: async (params) => { /* ... */ }
};
```

## Monitoring

### Logs
- Extension: VS Code Output Channel
- RAG Service: stdout/stderr
- ChromaDB: Log files

### Metrics
- Components indexed
- Search latency
- Embedding generation time
- API response times

## Testing Strategy

### Unit Tests
- Component extraction
- Embedding generation
- Vector operations
- API endpoints

### Integration Tests
- End-to-end search
- Folder scanning
- Service health

### Manual Testing
- Copilot chat interactions
- Sidebar UI operations
- Extension commands

---

For implementation details, see the source code and inline documentation.

