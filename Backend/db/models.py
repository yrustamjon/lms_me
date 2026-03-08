from .db import Base,Sync_Session, Async_Session
from .manager import SyncModelManager


class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        return self.manager(owner)


class BaseModel(Base):
    @property
    def session(self):
        return Sync_Session()
    __abstract__ = True
    objects = ManagerDescriptor(SyncModelManager)

    def save(self):
        with self.session as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    def delete(self):
        with self.session as session:
            session.delete(self)
            session.commit()
            return True
  
            

