import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Numeric, create_engine
from sqlalchemy.orm import Mapped, mapped_column

engine = create_engine('postgresql+psycopg2://postgres:postgres@104.198.147.59:5432/postgres', echo=True)


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base() 

class User(Base):
    __tablename__ = 'user'
    id: Mapped[str] = mapped_column(String(30),primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    lat:Mapped[float] = mapped_column(Numeric(18, 15))
    lon:Mapped[float] = mapped_column(Numeric(10,6))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, lat={self.lat!r}, lon={self.lon!r})"

class Patrol(Base):
    __tablename__ = 'patrol'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)

    start_lat: Mapped[float] = mapped_column(Numeric(18, 15))
    start_lon: Mapped[float] = mapped_column(Numeric(10,6))
    end_lat: Mapped[float] = mapped_column(Numeric(18, 15))
    end_lon: Mapped[float] = mapped_column(Numeric(10,6))
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    memo: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"Patrol(user_id={self.user_id!r}, user_name={self.user_name!r}, start_lat={self.start_lat!r}, start_lon={self.start_lon!r}, end_lat={self.end_lat!r}, end_lon={self.end_lon!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, memo={self.memo!r}, is_active={self.is_active!r})"



User.metadata.create_all(engine)
Patrol.metadata.create_all(engine)