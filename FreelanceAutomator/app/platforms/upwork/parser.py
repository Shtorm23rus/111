import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import re

from app.platforms.base_platform import BasePlatform
from app.platforms.upwork.models import UpworkJob
from app.core.constants import UPWORK_RSS_FEEDS
from app.core.exceptions import JobParsingError
from app.utils.logger import get_logger
from app.utils.helpers import extract_price_from_text, clean_text

logger = get_logger(__name__)

class UpworkParser(BasePlatform):
    def __init__(self):
        super().__init__("Upwork")
        self.base_url = "https://www.upwork.com"
    
    def fetch_jobs(self, category: str = "reviews", max_jobs: int = 20) -> List[Dict[str, Any]]:
        logger.info(f"Fetching jobs from Upwork category: {category}")
        
        rss_url = UPWORK_RSS_FEEDS.get(category, UPWORK_RSS_FEEDS['reviews'])
        
        try:
            feed = feedparser.parse(rss_url)
            
            jobs = []
            for entry in feed.entries[:max_jobs]:
                try:
                    job = self.parse_job(entry)
                    jobs.append(job)
                except Exception as e:
                    logger.warning(f"Failed to parse job entry: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(jobs)} jobs from Upwork")
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching jobs from Upwork: {e}")
            raise JobParsingError(f"Failed to fetch jobs: {e}")
    
    def parse_job(self, entry: Any) -> Dict[str, Any]:
        try:
            job_id = self._generate_job_id(entry.link)
            
            title = clean_text(entry.title) if hasattr(entry, 'title') else ""
            
            description = ""
            if hasattr(entry, 'summary'):
                soup = BeautifulSoup(entry.summary, 'html.parser')
                description = clean_text(soup.get_text())
            
            budget = self._extract_budget(description)
            
            posted_date = None
            if hasattr(entry, 'published_parsed'):
                posted_date = datetime(*entry.published_parsed[:6])
            
            job_url = entry.link if hasattr(entry, 'link') else ""
            
            skills = []
            if hasattr(entry, 'tags'):
                skills = [tag.term for tag in entry.tags]
            
            job_data = {
                'job_id': job_id,
                'title': title,
                'description': description,
                'category': self._extract_category(title, description),
                'budget': budget,
                'budget_type': 'fixed' if budget else 'hourly',
                'posted_date': posted_date,
                'url': job_url,
                'skills_required': ', '.join(skills) if skills else None,
                'complexity': self._estimate_complexity(title, description),
                'platform': 'upwork'
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job: {e}")
            raise JobParsingError(f"Failed to parse job: {e}")
    
    def _generate_job_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:16]
    
    def _extract_budget(self, text: str) -> Optional[float]:
        return extract_price_from_text(text)
    
    def _extract_category(self, title: str, description: str) -> str:
        text = (title + ' ' + description).lower()
        
        if any(word in text for word in ['review', 'отзыв']):
            return 'review'
        elif any(word in text for word in ['comment', 'комментарий']):
            return 'comment'
        elif any(word in text for word in ['feedback', 'обратная связь']):
            return 'feedback'
        elif any(word in text for word in ['post', 'пост', 'article', 'статья']):
            return 'post'
        else:
            return 'writing'
    
    def _estimate_complexity(self, title: str, description: str) -> int:
        text = (title + ' ' + description).lower()
        
        easy_keywords = ['simple', 'quick', 'easy', 'short', 'brief']
        hard_keywords = ['complex', 'detailed', 'extensive', 'professional', 'expert']
        
        if any(word in text for word in easy_keywords):
            return 1
        elif any(word in text for word in hard_keywords):
            return 3
        else:
            return 2
