from typing import List, Dict, Any
from app.platforms.upwork.parser import UpworkParser
from app.filters.complexity_filter import ComplexityFilter
from app.filters.category_filter import CategoryFilter
from app.filters.price_filter import PriceFilter
from app.database.session import Session
from app.database import crud
from app.core.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

class JobScraper:
    def __init__(self):
        self.upwork_parser = UpworkParser()
        
        self.filters = [
            ComplexityFilter(max_complexity=2),
            CategoryFilter(Config.TARGET_CATEGORIES),
            PriceFilter(min_price=Config.MIN_JOB_PRICE, max_price=Config.MAX_JOB_PRICE)
        ]
    
    def scrape_jobs(self, platform: str = "upwork", max_jobs: int = 20) -> List[Dict[str, Any]]:
        logger.info(f"Starting job scraping from {platform}")
        
        if platform == "upwork":
            jobs = self.upwork_parser.fetch_jobs(max_jobs=max_jobs)
        else:
            logger.warning(f"Platform {platform} not supported yet")
            return []
        
        for filter_func in self.filters:
            jobs = filter_func(jobs)
        
        logger.info(f"After filtering: {len(jobs)} jobs remain")
        return jobs
    
    def save_jobs_to_db(self, jobs: List[Dict[str, Any]]) -> int:
        db = Session()
        saved_count = 0
        
        try:
            for job_data in jobs:
                existing_job = crud.get_job_by_id(db, job_data['job_id'])
                
                if not existing_job:
                    crud.create_job(db, job_data)
                    saved_count += 1
                else:
                    logger.debug(f"Job {job_data['job_id']} already exists")
            
            logger.info(f"Saved {saved_count} new jobs to database")
            return saved_count
            
        finally:
            db.close()
    
    def run(self) -> Dict[str, Any]:
        try:
            jobs = self.scrape_jobs()
            saved_count = self.save_jobs_to_db(jobs)
            
            return {
                'status': 'success',
                'jobs_found': len(jobs),
                'jobs_saved': saved_count
            }
        except Exception as e:
            logger.error(f"Error in job scraping: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
