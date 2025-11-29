from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from src.config.settings import get_settings
from src.api.routes import search, components, scan
from src.api.models import HealthResponse
from src.db.vector_store import get_vector_store
from src.rag.embeddings import get_embedding_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="RAG service for Component AI Agent"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting RAG service...")
    
    try:
        # Initialize vector store
        vector_store = get_vector_store()
        logger.info(f"Vector store initialized with {vector_store.count()} components")
        
        # Initialize embedding service
        embedding_service = get_embedding_service()
        logger.info(f"Embedding service initialized (dimension: {embedding_service.get_dimension()})")
        
        logger.info("RAG service started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start RAG service: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down RAG service...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        vector_store = get_vector_store()
        chroma_healthy = vector_store.health_check()
        
        embedding_service = get_embedding_service()
        
        return HealthResponse(
            status="healthy" if chroma_healthy else "degraded",
            version=settings.app_version,
            chroma_status="healthy" if chroma_healthy else "unhealthy",
            embedding_model=settings.embedding_model
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version=settings.app_version,
            chroma_status="unhealthy",
            embedding_model=settings.embedding_model
        )


# Include routers
app.include_router(search.router, prefix=settings.api_prefix)
app.include_router(components.router, prefix=settings.api_prefix)
app.include_router(scan.router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

