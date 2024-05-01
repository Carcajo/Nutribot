from sqlalchemy import Integer, String, Text, ARRAY, Float, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, mapped_column
import asyncpg
from config import Settings

settings = Settings()


async def get_db_pool():
    pool = await asyncpg.create_pool(settings.DATABASE_URL)
    return pool

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50))
    target = mapped_column(Text, nullable=True)

    async def save(self, session: AsyncSession):
        async with session.begin():
            session.add(self)
        await session.commit()

    @classmethod
    async def get(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
            select(cls).where(cls.id == user_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, user_id: int, **kwargs):
        query = select(cls).where(cls.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one()
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        await session.commit()


class AdviceVector(Base):
    __tablename__ = "advice_vectors"

    id = mapped_column(Integer, primary_key=True)
    embedding = mapped_column(ARRAY(Float), nullable=False)
    text = mapped_column(Text, nullable=False)

    async def save(self, session: AsyncSession):
        async with session.begin():
            session.add(self)
        await session.commit()
