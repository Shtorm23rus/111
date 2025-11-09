from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.job_scraper import JobScraper
from app.tasks.content_generator import ContentGenerationTask
from app.core.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.job_scraper = JobScraper()
        self.content_generator = ContentGenerationTask()
    
    def scrape_jobs_task(self):
        logger.info("Running scheduled job scraping")
        result = self.job_scraper.run()
        logger.info(f"Scraping result: {result}")
    
    def generate_content_task(self):
        logger.info("Running scheduled content generation")
        processed = self.content_generator.process_pending_jobs(limit=5)
        logger.info(f"Generated content for {processed} jobs")
    
    def start(self):
        self.scheduler.add_job(
            self.scrape_jobs_task,
            'interval',
            minutes=Config.SCHEDULER_INTERVAL_MINUTES,
            id='scrape_jobs'
        )
        
        self.scheduler.add_job(
            self.generate_content_task,
            'interval',
            minutes=10,
            id='generate_content'
        )
        
        self.scheduler.start()
        logger.info("Task scheduler started successfully")
    
    def stop(self):
        self.scheduler.shutdown()
        logger.info("Task scheduler stopped")
