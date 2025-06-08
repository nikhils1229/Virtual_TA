from typing import Optional, List
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """Request model for question endpoint"""
    question: str
    image: Optional[str] = None  # Base64 encoded image

class LinkReference(BaseModel):
    """Model for reference links"""
    url: str
    text: str

class TAResponse(BaseModel):
    """Response model for TA answers"""
    answer: str
    links: List[LinkReference]

class DiscoursePost(BaseModel):
    """Model for Discourse posts"""
    id: int
    title: str
    content: str
    url: str
    created_at: str
    category: str
    tags: List[str] = []
