from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

Base = declarative_base()

# 환경 변수에서 데이터베이스 URL 가져오기
from sqlalchemy import create_engine  # noqa: E402

# SQLite 데이터베이스 생성
engine = create_engine("sqlite:///./silverguardian.db", echo=True)


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    lat: Mapped[float] = mapped_column(Float)  # 위도
    lon: Mapped[float] = mapped_column(Float)  # 경도

    # 관계 설정
    patrol_users: Mapped[list["PatrolUser"]] = relationship(
        "PatrolUser", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, lat={self.lat!r}, lon={self.lon!r})"


class Patrol(Base):
    __tablename__ = "patrol"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    start_lat: Mapped[float] = mapped_column(Float)  # 순찰 시작 위도
    start_lon: Mapped[float] = mapped_column(Float)  # 순찰 시작 경도
    end_lat: Mapped[float] = mapped_column(Float, nullable=True)  # 순찰 종료 위도
    end_lon: Mapped[float] = mapped_column(Float, nullable=True)  # 순찰 종료 경도
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime)  # 순찰 시작 시간
    end_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True
    )  # 순찰 종료 시간
    memo: Mapped[str] = mapped_column(String(500), nullable=True)  # 메모
    active: Mapped[bool] = mapped_column(Boolean, default=True)  # 순찰 중인지 여부

    # 관계 설정
    patrol_users: Mapped[list["PatrolUser"]] = relationship(
        "PatrolUser", back_populates="patrol", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Patrol(id={self.id!r}, name={self.name!r}, start_lat={self.start_lat!r}, start_lon={self.start_lon!r}, active={self.active!r})"


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
    patrol: Mapped["Patrol"] = relationship("Patrol", back_populates="patrol_users")
    user: Mapped["User"] = relationship("User", back_populates="patrol_users")

    def __repr__(self) -> str:
        return f"PatrolUser(patrol_id={self.patrol_id!r}, user_id={self.user_id!r}, joined_at={self.joined_at!r}, active={self.active!r})"


User.metadata.create_all(engine)
Patrol.metadata.create_all(engine)
PatrolUser.metadata.create_all(engine)
