import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from urllib.parse import urljoin
import re

from .models import DiscoursePost
from .utils import setup_logging

logger = setup_logging()

class DiscourseScraper:
    """
    Scraper for TDS Discourse forum posts
    """
    
    def __init__(self, base_url: str = "https://discourse.onlinedegree.iitm.ac.in"):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def scrape_posts(self, start_date: str, end_date: str, category_id: int = None) -> List[DiscoursePost]:
        """
        Scrape Discourse posts within date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format  
            category_id: Optional category ID to filter posts
            
        Returns:
            List of DiscoursePost objects
        """
        posts = []
        
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            try:
                # Get all topics first
                topics = await self._get_topics(category_id)
                logger.info(f"Found {len(topics)} topics to scrape")
                
                # Filter topics by date range
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                
                filtered_topics = []
                for topic in topics:
                    topic_date = datetime.strptime(topic["created_at"][:10], "%Y-%m-%d")
        
