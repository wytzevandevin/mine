from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Create engine with MySQL-specific settings
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,   # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 