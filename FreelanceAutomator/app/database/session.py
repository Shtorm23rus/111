from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

engine = create_engine(Config.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

Base = declarative_base()

def init_db():
    import app.database.models
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
