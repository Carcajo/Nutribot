from sqlalchemy import Integer, String, Text, ARRAY, Float
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50))
    target = mapped_column(Text, nullable=True)

    async def save(self, db_session: AsyncSession):
        db_session.add(self)
        await db_session.commit()


class AdviceVector(Base):
    __tablename__ = "advice_vectors"

    id = mapped_column(Integer, primary_key=True)
    embedding = mapped_column(ARRAY(Float), nullable=False)
    text = mapped_column(Text, nullable=False)
