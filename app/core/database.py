from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create sync database engine for backwards compatibility
engine = create_engine(settings.DATABASE_URL)

# Create async database engine for improved performance
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,  # Set to True for SQL query logging in development
    pool_size=20,  # Connection pool size
    max_overflow=0,  # Additional connections beyond pool_size
    pool_pre_ping=True,  # Validate connections before use
)

# Create session local class (sync)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create async session local class
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=async_engine,
)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get sync database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
