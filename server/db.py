import datetime
import os
from typing import Optional
from sqlalchemy import Boolean, DateTime, Numeric, create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = (
    os.getenv("DB_URL")
    or "postgresql+psycopg2://postgres:postgres@104.198.147.59:5432/postgres"
)
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    lat: Mapped[float] = mapped_column(Numeric(18, 15))
    lon: Mapped[float] = mapped_column(Numeric(10, 6))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, lat={self.lat!r}, lon={self.lon!r})"


class Patrol(Base):
    __tablename__ = "patrol"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))  # 순찰 이름
    start_lat: Mapped[float] = mapped_column(Numeric(18, 15))
    start_lon: Mapped[float] = mapped_column(Numeric(10, 6))
    end_lat: Mapped[Optional[float]] = mapped_column(Numeric(18, 15), nullable=True)
    end_lon: Mapped[Optional[float]] = mapped_column(Numeric(10, 6), nullable=True)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, nullable=True
    )
    memo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean)

    # 관계 설정
    users: Mapped[list["PatrolUser"]] = relationship(
        "PatrolUser", back_populates="patrol", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Patrol(id={self.id!r}, name={self.name!r}, start_lat={self.start_lat!r}, start_lon={self.start_lon!r}, end_lat={self.end_lat!r}, end_lon={self.end_lon!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, memo={self.memo!r}, active={self.active!r})"


class PatrolUser(Base):
    __tablename__ = "patrol_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patrol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("patrol.id", ondelete="CASCADE")
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user.id", ondelete="CASCADE")
    )
    joined_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 관계 설정
    patrol: Mapped["Patrol"] = relationship("Patrol", back_populates="users")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"PatrolUser(patrol_id={self.patrol_id!r}, user_id={self.user_id!r}, joined_at={self.joined_at!r}, active={self.active!r})"


class Notice(Base):
    __tablename__ = "notice"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))  # 공지 제목
    content: Mapped[str] = mapped_column(String(1000))  # 공지 내용
    location: Mapped[str] = mapped_column(String(200))  # 순찰 장소명
    location_lat: Mapped[float] = mapped_column(Float)  # 장소 위도
    location_lon: Mapped[float] = mapped_column(Float)  # 장소 경도
    scheduled_time: Mapped[datetime.datetime] = mapped_column(DateTime)  # 예정 시간
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)  # 활성 상태

    # 관계 설정
    assigned_users: Mapped[list["NoticeUser"]] = relationship(
        "NoticeUser", back_populates="notice", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Notice(id={self.id!r}, title={self.title!r}, location={self.location!r}, scheduled_time={self.scheduled_time!r}, active={self.active!r})"


class NoticeUser(Base):
    __tablename__ = "notice_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notice_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("notice.id", ondelete="CASCADE")
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("user.id", ondelete="CASCADE")
    )
    assigned_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)  # 유저 확인 여부

    # 관계 설정
    notice: Mapped["Notice"] = relationship("Notice", back_populates="assigned_users")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"NoticeUser(notice_id={self.notice_id!r}, user_id={self.user_id!r}, confirmed={self.confirmed!r})"


User.metadata.create_all(engine)
Patrol.metadata.create_all(engine)
PatrolUser.metadata.create_all(engine)
Notice.metadata.create_all(engine)
NoticeUser.metadata.create_all(engine)
