from sqlalchemy import Column, Integer, String, Text, ARRAY, Float
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50))
    target = mapped_column(Text, nullable=True)

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()


class AdviceVector(Base):
    __tablename__ = "advice_vectors"

    id = mapped_column(Integer, primary_key=True)
    embedding = mapped_column(ARRAY(Float), nullable=False)
    text = mapped_column(Text, nullable=False)