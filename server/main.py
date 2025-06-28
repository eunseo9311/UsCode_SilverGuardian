from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic.config import ConfigDict
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from db import User, Patrol, PatrolUser, engine
from sqlalchemy.orm import sessionmaker

from ai import region_state

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


class PatrolUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str


class PatrolCreateSchema(BaseModel):
    name: str
    start_lat: float  # 순찰 시작 위도
    start_lon: float  # 순찰 시작 경도
    users: list[str]  # 유저 ID 리스트


class PatrolSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    start_lat: float  # 순찰 시작 위도
    start_lon: float  # 순찰 시작 경도
    end_lat: Optional[float] = None  # 순찰 종료 위도
    end_lon: Optional[float] = None  # 순찰 종료 경도
    start_time: datetime  # 순찰 시작 시간
    end_time: Optional[datetime] = None  # 순찰 종료 시간
    memo: Optional[str] = None  # 메모
    active: bool = True  # 순찰 중인지 여부
    users: List[PatrolUserSchema]  # 참여 유저들


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello from uscode-silverguardian!"}


@app.get("/vworld")
async def vworld() -> dict:
    return {"message": await region_state()}


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

    # 삭제 전에 유저 정보 저장
    user_data = UserSchema.model_validate(user)

    db.delete(user)
    db.commit()

    return user_data


# Patrol CRUD 기능


# 순찰 생성 Create
@app.post("/patrols/start")
def start_patrol(
    patrol_data: PatrolCreateSchema, db: Session = Depends(get_db)
) -> PatrolSchema:
    # 1. 유저들 존재 확인
    for user_info in patrol_data.users:
        user = db.execute(select(User).where(User.id == user_info)).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_info} not found")

    # 2. 유저들 중복 순찰 확인
    for user_info in patrol_data.users:
        active_patrol = db.execute(
            select(PatrolUser)
            .join(Patrol)
            .where(PatrolUser.user_id == user_info, Patrol.active)
        ).scalar_one_or_none()
        if active_patrol:
            raise HTTPException(
                status_code=400, detail=f"User {user_info} is already on patrol"
            )

    # 3. 순찰 생성
    patrol = Patrol(
        name=patrol_data.name,
        start_lat=patrol_data.start_lat,
        start_lon=patrol_data.start_lon,
        start_time=datetime.now(),
        active=True,
    )
    db.add(patrol)
    db.flush()  # ID 생성

    # 4. 유저들 할당
    for user_info in patrol_data.users:
        patrol_user = PatrolUser(
            patrol_id=patrol.id,
            user_id=user_info,
            joined_at=datetime.now(),
            active=True,
        )
        db.add(patrol_user)

    db.commit()
    db.refresh(patrol)

    # 5. 응답 데이터 구성
    patrol_users = (
        db.execute(select(PatrolUser).where(PatrolUser.patrol_id == patrol.id))
        .scalars()
        .all()
    )

    users_data = [PatrolUserSchema(user_id=pu.user_id) for pu in patrol_users]

    return PatrolSchema(
        id=patrol.id,
        name=patrol.name,
        start_lat=patrol.start_lat,
        start_lon=patrol.start_lon,
        end_lat=patrol.end_lat,
        end_lon=patrol.end_lon,
        start_time=patrol.start_time,
        end_time=patrol.end_time,
        memo=patrol.memo,
        active=patrol.active,
        users=users_data,
    )


# 순찰 조회 Read
@app.get("/patrols")
def read_patrols(db: Session = Depends(get_db)) -> list[PatrolSchema]:
    patrols = db.execute(select(Patrol)).scalars().all()
    result = []

    for patrol in patrols:
        # 각 순찰의 유저 정보 조회
        patrol_users = (
            db.execute(select(PatrolUser).where(PatrolUser.patrol_id == patrol.id))
            .scalars()
            .all()
        )

        users_data = [PatrolUserSchema(user_id=pu.user_id) for pu in patrol_users]

        result.append(
            PatrolSchema(
                id=patrol.id,
                name=patrol.name,
                start_lat=patrol.start_lat,
                start_lon=patrol.start_lon,
                end_lat=patrol.end_lat,
                end_lon=patrol.end_lon,
                start_time=patrol.start_time,
                end_time=patrol.end_time,
                memo=patrol.memo,
                active=patrol.active,
                users=users_data,
            )
        )

    return result


# 순찰 중 유저 목록
@app.get("/patrols/active")
def get_active_patrols(db: Session = Depends(get_db)) -> list[PatrolSchema]:
    active_patrols = db.execute(select(Patrol).where(Patrol.active)).scalars().all()
    result = []

    for patrol in active_patrols:
        # 각 순찰의 유저 정보 조회
        patrol_users = (
            db.execute(select(PatrolUser).where(PatrolUser.patrol_id == patrol.id))
            .scalars()
            .all()
        )

        users_data = [PatrolUserSchema(user_id=pu.user_id) for pu in patrol_users]

        result.append(
            PatrolSchema(
                id=patrol.id,
                name=patrol.name,
                start_lat=patrol.start_lat,
                start_lon=patrol.start_lon,
                end_lat=patrol.end_lat,
                end_lon=patrol.end_lon,
                start_time=patrol.start_time,
                end_time=patrol.end_time,
                memo=patrol.memo,
                active=patrol.active,
                users=users_data,
            )
        )

    return result


# 특정 순찰 조회 Read
@app.get("/patrols/{patrol_id}")
def read_patrol(patrol_id: int, db: Session = Depends(get_db)) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")

    # 순찰의 유저 정보 조회
    patrol_users = (
        db.execute(select(PatrolUser).where(PatrolUser.patrol_id == patrol.id))
        .scalars()
        .all()
    )

    users_data = [PatrolUserSchema(user_id=pu.user_id) for pu in patrol_users]

    return PatrolSchema(
        id=patrol.id,
        name=patrol.name,
        start_lat=patrol.start_lat,
        start_lon=patrol.start_lon,
        end_lat=patrol.end_lat,
        end_lon=patrol.end_lon,
        start_time=patrol.start_time,
        end_time=patrol.end_time,
        memo=patrol.memo,
        active=patrol.active,
        users=users_data,
    )


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

    # 업데이트된 순찰 정보 반환
    return read_patrol(patrol_id, db)


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

    # 업데이트된 순찰 정보 반환
    return read_patrol(patrol_id, db)


# 특정 유저의 활성 순찰 조회
@app.get("/patrols/user/{user_id}/active")
def get_user_active_patrol(user_id: str, db: Session = Depends(get_db)) -> PatrolSchema:
    # 유저가 참여 중인 활성 순찰 조회
    patrol_user = db.execute(
        select(PatrolUser)
        .join(Patrol)
        .where(PatrolUser.user_id == user_id, Patrol.active)
    ).scalar_one_or_none()

    if not patrol_user:
        raise HTTPException(status_code=404, detail="User not in active patrol")

    # 순찰 정보 반환
    return read_patrol(patrol_user.patrol_id, db)


# 순찰 삭제 Delete
@app.delete("/patrols/{patrol_id}")
def delete_patrol(patrol_id: int, db: Session = Depends(get_db)) -> PatrolSchema:
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")

    # 삭제 전에 순찰 정보 저장
    deleted_patrol = PatrolSchema(
        id=patrol.id,
        name=patrol.name,
        start_lat=patrol.start_lat,
        start_lon=patrol.start_lon,
        end_lat=patrol.end_lat,
        end_lon=patrol.end_lon,
        start_time=patrol.start_time,
        end_time=patrol.end_time,
        memo=patrol.memo,
        active=patrol.active,
        users=[],  # 삭제되었으므로 빈 리스트
    )

    # 순찰 삭제 시 관련된 PatrolUser도 함께 삭제됨 (CASCADE)
    db.delete(patrol)
    db.commit()

    return deleted_patrol


# 순찰에 유저 추가
@app.post("/patrols/{patrol_id}/users")
def add_user_to_patrol(
    patrol_id: int, user_id: str, db: Session = Depends(get_db)
) -> PatrolSchema:
    # 순찰 존재 확인
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")

    # 유저 존재 확인
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 이미 참여 중인지 확인
    existing = db.execute(
        select(PatrolUser).where(
            PatrolUser.patrol_id == patrol_id, PatrolUser.user_id == user_id
        )
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="User already in patrol")

    # 유저 추가
    patrol_user = PatrolUser(
        patrol_id=patrol_id, user_id=user_id, joined_at=datetime.now(), active=True
    )
    db.add(patrol_user)
    db.commit()

    # 업데이트된 순찰 정보 반환
    return read_patrol(patrol_id, db)


# 순찰에서 유저 제거
@app.delete("/patrols/{patrol_id}/users/{user_id}")
def remove_user_from_patrol(
    patrol_id: int, user_id: str, db: Session = Depends(get_db)
) -> PatrolSchema:
    patrol_user = db.execute(
        select(PatrolUser).where(
            PatrolUser.patrol_id == patrol_id, PatrolUser.user_id == user_id
        )
    ).scalar_one_or_none()

    if not patrol_user:
        raise HTTPException(status_code=404, detail="User not in patrol")

    db.delete(patrol_user)
    db.commit()

    # 업데이트된 순찰 정보 반환
    return read_patrol(patrol_id, db)


# 순찰의 유저 목록 조회
@app.get("/patrols/{patrol_id}/users")
def get_patrol_users(
    patrol_id: int, db: Session = Depends(get_db)
) -> list[PatrolUserSchema]:
    # 순찰 존재 확인
    patrol = db.execute(
        select(Patrol).where(Patrol.id == patrol_id)
    ).scalar_one_or_none()
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")

    # 순찰의 유저들 조회
    patrol_users = (
        db.execute(select(PatrolUser).where(PatrolUser.patrol_id == patrol_id))
        .scalars()
        .all()
    )

    return [PatrolUserSchema(user_id=pu.user_id) for pu in patrol_users]
