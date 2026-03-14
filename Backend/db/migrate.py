from .db import Base,sync_engine,async_engine
from models.user import Student

Base.metadata.drop_all(bind=sync_engine)
Base.metadata.create_all(bind=sync_engine)
print("Database Migrated")

