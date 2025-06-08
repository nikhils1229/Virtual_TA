# app/main.py
import os
import json
import base64
import io
from typing import Optional, List
from PIL import Image
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .rag_system import RAGSystem
from .models import QuestionRequest, TAResponse
from .utils import setup_logging, process_image

# Initialize logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="TDS Virtual Teaching Assistant",
    description="API for answering TDS course questions using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    try:
        rag_system = RAGSystem()
        await rag_system.initialize()
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "TDS Virtual TA API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "rag_system": "initialized" if rag_system else "not initialized",
        "version": "1.0.0"
    }

@app.post("/api/", response_model=TAResponse)
async def answer_question(request: QuestionRequest):
    """
    Main endpoint for answering student questions
    
    Accepts JSON with:
    - question: str (required) - The student's question
    - image: str (optional) - Base64 encoded image
    
    Returns:
    - answer: str - The generated answer
    - links: List[dict] - Relevant links with URL and text
    """
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        # Process image if provided
        image_context = None
        if request.image:
            try:
                image_context = process_image(request.image)
                logger.info("Image processed successfully")
            except Exception as e:
                logger.warning(f"Failed to process image: {e}")
        
        # Get answer from RAG system
        result = await rag_system.answer_question(
            question=request.question,
            image_context=image_context
        )
        
        return TAResponse(
            answer=result["answer"],
            links=result["links"]
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reload")
async def reload_data():
    """Reload the knowledge base (admin endpoint)"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        await rag_system.reload_knowledge_base()
        return {"message": "Knowledge base reloaded successfully"}
        
    except Exception as e:
        logger.error(f"Error reloading knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )
