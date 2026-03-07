from .db import Sync_Session, Async_Session
from sqlalchemy import select

class SyncModelManager:
    def __init__(self, model):
        self.model = model
    
    @property
    def session(self):
        return Sync_Session()
    
    def create(self, **kwargs):
        with self.session as session:
            obj = self.model(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
    
    def get(self, **kwargs):
        with self.session as session:
            return session.query(self.model).filter_by(**kwargs).first()

    def all(self):
        with self.session as session:
            return session.query(self.model).all()