from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.config import ConfigDict
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from db import User, Patrol, engine
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    lat: float  # 위도
    lon: float  # 경도


class PatrolSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    user_name: str
    start_lat: float  # 순찰 시작 위도
    start_lon: float  # 순찰 시작 경도
    end_lat: Optional[float] = None  # 순찰 종료 위도
    end_lon: Optional[float] = None  # 순찰 종료 경도
    start_time: datetime  # 순찰 시작 시간
    end_time: Optional[datetime] = None  # 순찰 종료 시간
    memo: Optional[str] = None  # 메모
    active: bool = True  # 순찰 중인지 여부


users = {}
patrols = {}  # 순찰 데이터 저장
patrol_counter = 1  # 순찰 ID 자동 생성용


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello from uscode-silverguardian!"}


# User CRUD 기능


# 유저 생성 Create
@app.get("/users/qr/{uuid}")
def create_user_qr(
    uuid: str, lat: float, lon: float, db: Session = Depends(get_db)
) -> UserSchema:
    user = db.execute(select(User).where(User.id == uuid)).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(id=uuid, name="정해지지 않음", lat=lat, lon=lon)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserSchema.model_validate(user)


# 유저 조회 Read
@app.get("/users")
def read_users(db: Session = Depends(get_db)) -> list[UserSchema]:
    users = db.execute(select(User)).scalars().all()  # 모든 유저 조회
    return [UserSchema.model_validate(user) for user in users]


# 특정 유저 조회 Read
@app.get("/users/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db)) -> UserSchema:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.model_validate(user)


# 유저 수정 Update
@app.put("/users/{user_id}")
def update_user(
    user_id: str, user: UserSchema, db: Session = Depends(get_db)
) -> UserSchema:
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user.model_dump().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return UserSchema.model_validate(db_user)


# 유저 삭제 Delete
@app.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)) -> UserSchema:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return UserSchema.model_validate(user)


# Patrol CRUD 기능


# 순찰 생성 Create
@app.post("/patrols/start")
def start_patrol(
    patrol_data: PatrolSchema, db: Session = Depends(get_db)
) -> PatrolSchema:
    # 유저 존재 확인
    user = db.execute(
        select(User).where(User.id == patrol_data.user_id)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 유저 순찰 중 확인
    active_patrol = db.execute(
        select(Patrol).where(
            Patrol.user_id == patrol_data.user_id, Patrol.active.is_(True)
        )
    ).scalar_one_or_none()
    if active_patrol:
        raise HTTPException(status_code=400, detail="User is already on patrol")

    patrol = Patrol(
        user_id=patrol_data.user_id,
        user_name=user.name,  # Get user name from database
        start_lat=patrol_data.start_lat,
        start_lon=patrol_data.start_lon,
        start_time=datetime.now(),
        active=True,
    )

    db.add(patrol)
    db.commit()
    db.refresh(patrol)
    return PatrolSchema.model_validate(patrol)


# 순찰 조회 Read
@app.get("/patrols")
def read_patrols(db: Session = Depends(get_db)) -> list[PatrolSchema]:
    patrols = db.execute(select(Patrol)).scalars().all()
    return [PatrolSchema.model_validate(patrol) for patrol in patrols]


# 순찰 중 유저 목록
@app.get("/patrols/active")
def get_active_patrols(db: Session = Depends(get_db)) -> list[PatrolSchema]:
    active_patrols = (
        db.execute(select(Patrol).where(Patrol.active.is_(True))).scalars().all()
    )
    return [PatrolSchema.model_validate(patrol) for patrol in active_patrols]


# 특정 순찰 조회 Read
@app.get("/patrols/{patrol_id}")
def read_patrol(patrol_id: int, db: Session = Depends(get_db)) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")
    return PatrolSchema.model_validate(patrol)


# 순찰 종료 Update
@app.put("/patrols/{patrol_id}/end")
def end_patrol(
    patrol_id: int, end_lat: float, end_lon: float, db: Session = Depends(get_db)
) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")

    patrol.end_lat = end_lat
    patrol.end_lon = end_lon
    patrol.end_time = datetime.now()
    patrol.active = False

    db.commit()
    db.refresh(patrol)
    return PatrolSchema.model_validate(patrol)


# 순찰 메모 업데이트 Update
@app.put("/patrols/{patrol_id}/memo")
def update_patrol_memo(
    patrol_id: int, memo: str, db: Session = Depends(get_db)
) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")
    patrol.memo = memo

    db.commit()
    db.refresh(patrol)
    return PatrolSchema.model_validate(patrol)


# 특정 유저 순찰 메모 조회 Read
@app.get("/patrols/user/{user_id}/memo")
def get_user_patrol_memo(user_id: str, db: Session = Depends(get_db)) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.user_id == user_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")
    return PatrolSchema.model_validate(patrol)


# 순찰 삭제 Delete
@app.delete("/patrols/{patrol_id}")
def delete_patrol(patrol_id: int, db: Session = Depends(get_db)) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")

    db.delete(patrol)
    db.commit()
    db.refresh(patrol)
    return PatrolSchema.model_validate(patrol)
