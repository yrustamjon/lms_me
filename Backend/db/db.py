from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DATABASE_URL = 'postgres:rust1234@localhost:5432/lms'

sync_engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_URL}",
    echo=True
)


async_engine = create_async_engine(
    f"postgresql+asyncpg://{DATABASE_URL}", 
    echo=True
)

Sync_Session=scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False, 
        bind=sync_engine,
        )
    )



Async_Session=async_sessionmaker(
    autocommit=False,
    autoflush=False, 
    bind=async_engine,
    )

Base=declarative_base()


