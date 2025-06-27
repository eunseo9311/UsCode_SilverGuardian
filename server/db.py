import datetime
<<<<<<< HEAD
from sqlalchemy import Boolean, DateTime, Numeric, create_engine
from sqlalchemy.orm import Mapped, mapped_column

=======
import os
from typing import Optional
from sqlalchemy import Boolean, DateTime, Numeric, create_engine
from sqlalchemy.orm import Mapped, mapped_column

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv('DB_URL')
engine = create_engine(DATABASE_URL, echo=True)
>>>>>>> 629f63ffee469f13c7555c0c2ca131bf53b1a30b

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@104.198.147.59:5432/postgres", echo=True
)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(String(30), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    lat: Mapped[float] = mapped_column(Numeric(18, 15))
    lon: Mapped[float] = mapped_column(Numeric(10, 6))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, lat={self.lat!r}, lon={self.lon!r})"


class Patrol(Base):
    __tablename__ = "patrol"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    start_lat: Mapped[float] = mapped_column(Numeric(18, 15))
    start_lon: Mapped[float] = mapped_column(Numeric(10, 6))
    end_lat: Mapped[float] = mapped_column(Numeric(18, 15))
    end_lon: Mapped[float] = mapped_column(Numeric(10, 6))
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    memo: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"Patrol(start_lat={self.start_lat!r}, start_lon={self.start_lon!r}, end_lat={self.end_lat!r}, end_lon={self.end_lon!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, memo={self.memo!r}, is_active={self.is_active!r})"

User.metadata.create_all(engine)
Patrol.metadata.create_all(engine)
