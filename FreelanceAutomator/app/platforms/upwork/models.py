from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UpworkJob(BaseModel):
    job_id: str
    title: str
    description: str
    category: Optional[str] = None
    budget: Optional[float] = None
    budget_type: Optional[str] = None
    posted_date: Optional[datetime] = None
    url: Optional[str] = None
    skills_required: Optional[List[str]] = Field(default_factory=list)
    complexity: Optional[int] = 1
    platform: str = "upwork"
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "12345",
                "title": "Write product review",
                "description": "Need someone to write a detailed review",
                "budget": 50.0,
                "platform": "upwork"
            }
        }
