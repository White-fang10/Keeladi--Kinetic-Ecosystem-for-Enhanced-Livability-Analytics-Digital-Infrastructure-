import logging
from app.db.session import engine
from app.db.base_class import Base

# Import all models to ensure they are registered with Base metadata
from app.models import *

logger = logging.getLogger(__name__)

def init_db() -> None:
    """Initialize the database by creating all tables based on SQLAlchemy models."""
    logger.info("Creating initial database tables (if they don't exist)...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization complete.")

if __name__ == "__main__":
    init_db()
