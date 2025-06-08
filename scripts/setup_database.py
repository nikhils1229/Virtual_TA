#!/usr/bin/env python3
"""
Database setup script for TDS Virtual TA
Creates necessary directories and initializes ChromaDB
"""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils import setup_logging
from app.rag_system import RAGSystem

logger = setup_logging()

async def setup_database():
    """Initialize the database and directory structure"""
    try:
        # Create directory structure
        directories = [
            "data/raw",
            "data/processed", 
            "data/embeddings",
            "data/chromadb",
            "logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        
        # Create .gitkeep files for empty directories
        gitkeep_dirs = ["data/raw", "data/processed", "data/embeddings"]
        for directory in gitkeep_dirs:
            gitkeep_path = Path(directory) / ".gitkeep"
            gitkeep_path.touch()
        
        # Initialize RAG system (this will create ChromaDB collections)
        logger.info("Initializing RAG system...")
        rag_system = RAGSystem()
        await rag_system.initialize()
        
        logger.info("Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(setup_database())
    sys.exit(0 if success else 1)
