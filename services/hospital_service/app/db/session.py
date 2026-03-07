from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from services.hospital_service.app.core.config import settings

engine_kwargs = {
    "echo": False,
    "future": True,
}

if "sqlite" not in settings.DATABASE_URL:
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20
    })

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db_session():
    """
    Dependency for getting an async database session in FastAPI routes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
