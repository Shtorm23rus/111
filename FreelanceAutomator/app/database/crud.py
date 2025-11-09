from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database.models import Job, GeneratedContent, Proposal, UserSettings
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_job(db: Session, job_data: Dict[str, Any]) -> Job:
    job = Job(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    logger.info(f"Created job: {job.job_id}")
    return job

def get_job_by_id(db: Session, job_id: str) -> Optional[Job]:
    return db.query(Job).filter(Job.job_id == job_id).first()

def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[Job]:
    return db.query(Job).offset(skip).limit(limit).all()

def get_jobs_by_status(db: Session, status: str) -> List[Job]:
    return db.query(Job).filter(Job.status == status).all()

def update_job_status(db: Session, job_id: str, status: str) -> Optional[Job]:
    job = get_job_by_id(db, job_id)
    if job:
        job.status = status
        db.commit()
        db.refresh(job)
        logger.info(f"Updated job {job_id} status to {status}")
    return job

def create_generated_content(db: Session, job_id: str, content_type: str, text: str) -> GeneratedContent:
    content = GeneratedContent(
        job_id=job_id,
        content_type=content_type,
        generated_text=text
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    logger.info(f"Created generated content for job: {job_id}")
    return content

def get_content_by_job_id(db: Session, job_id: str) -> List[GeneratedContent]:
    return db.query(GeneratedContent).filter(GeneratedContent.job_id == job_id).all()

def delete_job(db: Session, job_id: str) -> bool:
    job = get_job_by_id(db, job_id)
    if job:
        db.delete(job)
        db.commit()
        logger.info(f"Deleted job: {job_id}")
        return True
    return False

def create_proposal(db: Session, job_id: str, proposal_text: str, proposal_type: str = "standard") -> Proposal:
    proposal = Proposal(
        job_id=job_id,
        proposal_text=proposal_text,
        proposal_type=proposal_type
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    logger.info(f"Created proposal for job: {job_id}")
    return proposal

def get_proposals_by_job_id(db: Session, job_id: str) -> List[Proposal]:
    return db.query(Proposal).filter(Proposal.job_id == job_id).all()

def get_proposal_by_id(db: Session, proposal_id: int) -> Optional[Proposal]:
    return db.query(Proposal).filter(Proposal.id == proposal_id).first()

def update_proposal(db: Session, proposal_id: int, proposal_text: str) -> Optional[Proposal]:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal:
        proposal.proposal_text = proposal_text
        db.commit()
        db.refresh(proposal)
        logger.info(f"Updated proposal {proposal_id}")
    return proposal

def delete_proposal(db: Session, proposal_id: int) -> bool:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal:
        db.delete(proposal)
        db.commit()
        logger.info(f"Deleted proposal: {proposal_id}")
        return True
    return False

def get_setting(db: Session, key: str) -> Optional[str]:
    setting = db.query(UserSettings).filter(UserSettings.key == key).first()
    return setting.value if setting else None

def set_setting(db: Session, key: str, value: str) -> UserSettings:
    setting = db.query(UserSettings).filter(UserSettings.key == key).first()
    if setting:
        setting.value = value
    else:
        setting = UserSettings(key=key, value=value)
        db.add(setting)
    db.commit()
    db.refresh(setting)
    logger.info(f"Set setting {key}")
    return setting
