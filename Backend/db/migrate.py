from .db import Base,sync_engine,async_engine
import models.user

Base.metadata.create_all(bind=sync_engine)

print("Database Migrated")

