from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import AsyncGenerator
from app.config.settings import settings


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,   # connects the session factory to your Database Engine.
    class_=AsyncSession,   # creates asynchronous sessions
    expire_on_commit=False,   # prevents cleaning the data from variables after commit
)

async def get_async_session()-> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:   # open a new session
        try:
            yield session  # pause the funtion
        except Exception as e:
            await session.rollback()  # undo the changes made during the transaction
            raise e
        finally:
            await session.close()  # close the session to free up resources
