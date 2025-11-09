from app.ai.content_generator import ContentGeneratorFactory
from app.database.session import Session
from app.database import crud
from app.core.constants import JOB_STATUS
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ContentGenerationTask:
    def __init__(self):
        pass
    
    def generate_for_job(self, job_id: str) -> bool:
        db = Session()
        
        try:
            job = crud.get_job_by_id(db, job_id)
            if not job:
                logger.error(f"Job {job_id} not found")
                return False
            
            crud.update_job_status(db, job_id, JOB_STATUS['IN_PROGRESS'])
            
            generator = ContentGeneratorFactory.get_generator(job.category)
            
            generated_text = generator.generate(
                job_description=f"{job.title}\n\n{job.description}",
                max_tokens=512
            )
            
            crud.create_generated_content(
                db,
                job_id=job.job_id,
                content_type=job.category,
                text=generated_text
            )
            
            crud.update_job_status(db, job_id, JOB_STATUS['COMPLETED'])
            
            logger.info(f"Successfully generated content for job {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating content for job {job_id}: {e}")
            crud.update_job_status(db, job_id, JOB_STATUS['FAILED'])
            return False
        
        finally:
            db.close()
    
    def process_pending_jobs(self, limit: int = 5) -> int:
        db = Session()
        
        try:
            pending_jobs = crud.get_jobs_by_status(db, JOB_STATUS['PENDING'])
            
            processed = 0
            for job in pending_jobs[:limit]:
                if self.generate_for_job(job.job_id):
                    processed += 1
            
            logger.info(f"Processed {processed} pending jobs")
            return processed
            
        finally:
            db.close()
