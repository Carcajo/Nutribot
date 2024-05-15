from typing import Optional
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from . import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    goal = Column(String)
    openai_thread_id = Column(String)


    def __repr__(self):
        return f"<User(id={self.id}, goal={self.goal})>"


    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        result = await session.execute(
                select(cls).where(cls.id == user_id)
                )
        return result.scalar_one_or_none()


    @classmethod
    async def user_exists_by_id(cls, session: AsyncSession, user_id: int) -> bool:
        result = await session.execute(
                select(cls.id).where(cls.id == user_id)
                )
        return result.scalar_one_or_none() is not None
