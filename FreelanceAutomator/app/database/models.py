from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.core.constants import JOB_STATUS
import enum

class JobStatusEnum(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    platform = Column(String, default="upwork")
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    budget = Column(Float, nullable=True)
    budget_type = Column(String, nullable=True)
    url = Column(String, nullable=True)
    complexity = Column(Integer, default=1)
    status = Column(String, default=JOB_STATUS['PENDING'])
    posted_date = Column(DateTime, nullable=True)
    skills_required = Column(Text, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    contents = relationship("GeneratedContent", back_populates="job", cascade="all, delete-orphan")
    proposals = relationship("Proposal", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job {self.job_id}: {self.title}>"

class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey('jobs.job_id'), index=True)
    content_type = Column(String)
    generated_text = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    
    job = relationship("Job", back_populates="contents")
    
    def __repr__(self):
        return f"<GeneratedContent for {self.job_id}>"

class Proposal(Base):
    __tablename__ = "proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey('jobs.job_id'), index=True)
    proposal_text = Column(Text)
    proposal_type = Column(String, default="standard")
    is_sent = Column(Integer, default=0)
    sent_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    job = relationship("Job", back_populates="proposals")
    
    def __repr__(self):
        return f"<Proposal for {self.job_id}>"

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserSettings {self.key}: {self.value}>"
