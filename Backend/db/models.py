from .db import Base
from .manager import SyncModelManager


class ManagerDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        return self.manager(owner)


class BaseModel(Base):
    __abstract__ = True
    objects = ManagerDescriptor(SyncModelManager)



