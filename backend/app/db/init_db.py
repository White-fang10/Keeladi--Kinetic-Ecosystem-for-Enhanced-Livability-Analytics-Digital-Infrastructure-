from app.db.base_class import Base
from app.models import *  # noqa: Ensure all models are imported before create_all


def init_db():
    """Create all database tables."""
    from app.db.session import engine
    Base.metadata.create_all(bind=engine)
