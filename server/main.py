from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from pydantic.config import ConfigDict
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from db import User, Patrol, PatrolUser, Notice, NoticeUser, engine
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


class PatrolUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str


class PatrolCreateSchema(BaseModel):
    name: str
    start_lat: float  # 순찰 시작 위도
    start_lon: float  # 순찰 시작 경도
    start_time: Optional[datetime] = None  # 순찰 시작 시간 (None이면 현재 시간)
    users: List[str]  # 유저 ID 리스트


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


class NoticeUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    confirmed: bool = False


class NoticeCreateSchema(BaseModel):
    title: str
    content: str
    location: str
    location_lat: float
    location_lon: float
    scheduled_time: datetime
    users: List[str]  # 유저 ID 리스트


class NoticeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    location: str
    location_lat: float
    location_lon: float
    scheduled_time: datetime
    active: bool = True
    assigned_users: List[NoticeUserSchema]  # 할당된 유저들


class NoticeSimpleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    location: str
    location_lat: float
    location_lon: float
    scheduled_time: datetime
    user_names: List[str]  # 참여 유저들 이름만


class PatrolNoticeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    start_lat: float  # 순찰 시작 위치 위도
    start_lon: float  # 순찰 시작 위치 경도
    start_time: datetime  # 순찰 시작 시간
    user_names: List[str]  # 함께 순찰하는 유저들 이름


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
        start_time=patrol_data.start_time or datetime.now(),
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


# Notice CRUD 기능


# 공지 생성 Create
@app.post("/notices/start")
def start_notice(
    notice_data: NoticeCreateSchema, db: Session = Depends(get_db)
) -> NoticeSchema:
    # 1. 유저들 존재 확인
    for user_info in notice_data.users:
        user = db.execute(select(User).where(User.id == user_info)).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_info} not found")

    # 2. 공지 생성
    notice = Notice(
        title=notice_data.title,
        content=notice_data.content,
        location=notice_data.location,
        location_lat=notice_data.location_lat,
        location_lon=notice_data.location_lon,
        scheduled_time=notice_data.scheduled_time,
        active=True,
    )
    db.add(notice)
    db.flush()  # ID 생성

    # 3. 유저들 할당
    for user_info in notice_data.users:
        notice_user = NoticeUser(
            notice_id=notice.id,
            user_id=user_info,
            confirmed=False,
        )
        db.add(notice_user)

    db.commit()
    db.refresh(notice)

    # 4. 응답 데이터 구성
    assigned_users = (
        db.execute(select(NoticeUser).where(NoticeUser.notice_id == notice.id))
        .scalars()
        .all()
    )

    users_data = [
        NoticeUserSchema(user_id=nu.user_id, confirmed=nu.confirmed)
        for nu in assigned_users
    ]

    return NoticeSchema(
        id=notice.id,
        title=notice.title,
        content=notice.content,
        location=notice.location,
        location_lat=notice.location_lat,
        location_lon=notice.location_lon,
        scheduled_time=notice.scheduled_time,
        active=notice.active,
        assigned_users=users_data,
    )


# 공지 조회 Read
@app.get("/notices")
def read_notices(db: Session = Depends(get_db)) -> list[NoticeSchema]:
    notices = db.execute(select(Notice)).scalars().all()
    result = []

    for notice in notices:
        # 각 공지의 유저 정보 조회
        assigned_users = (
            db.execute(select(NoticeUser).where(NoticeUser.notice_id == notice.id))
            .scalars()
            .all()
        )

        users_data = [
            NoticeUserSchema(user_id=nu.user_id, confirmed=nu.confirmed)
            for nu in assigned_users
        ]

        result.append(
            NoticeSchema(
                id=notice.id,
                title=notice.title,
                content=notice.content,
                location=notice.location,
                location_lat=notice.location_lat,
                location_lon=notice.location_lon,
                scheduled_time=notice.scheduled_time,
                active=notice.active,
                assigned_users=users_data,
            )
        )

    return result


# 특정 공지 조회 Read
@app.get("/notices/{notice_id}")
def read_notice(notice_id: int, db: Session = Depends(get_db)) -> NoticeSchema:
    notice = db.execute(
        select(Notice).where(Notice.id == notice_id)
    ).scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # 공지의 유저 정보 조회
    assigned_users = (
        db.execute(select(NoticeUser).where(NoticeUser.notice_id == notice.id))
        .scalars()
        .all()
    )

    users_data = [
        NoticeUserSchema(user_id=nu.user_id, confirmed=nu.confirmed)
        for nu in assigned_users
    ]

    return NoticeSchema(
        id=notice.id,
        title=notice.title,
        content=notice.content,
        location=notice.location,
        location_lat=notice.location_lat,
        location_lon=notice.location_lon,
        scheduled_time=notice.scheduled_time,
        active=notice.active,
        assigned_users=users_data,
    )


# 공지 종료 Update
@app.put("/notices/{notice_id}/end")
def end_notice(notice_id: int, db: Session = Depends(get_db)) -> NoticeSchema:
    notice = db.execute(
        select(Notice).where(Notice.id == notice_id)
    ).scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    notice.active = False

    db.commit()
    db.refresh(notice)

    # 업데이트된 공지 정보 반환
    return read_notice(notice_id, db)


# 공지 메모 업데이트 Update
@app.put("/notices/{notice_id}/memo")
def update_notice_memo(
    notice_id: int, memo: str, db: Session = Depends(get_db)
) -> NoticeSchema:
    notice = db.execute(
        select(Notice).where(Notice.id == notice_id)
    ).scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    notice.memo = memo

    db.commit()
    db.refresh(notice)

    # 업데이트된 공지 정보 반환
    return read_notice(notice_id, db)


# 특정 유저의 활성 공지 조회
@app.get("/notices/user/{user_id}/active")
def get_user_active_notice(user_id: str, db: Session = Depends(get_db)) -> NoticeSchema:
    # 유저가 할당된 활성 공지 조회
    notice_user = db.execute(
        select(NoticeUser)
        .join(Notice)
        .where(NoticeUser.user_id == user_id, Notice.active)
    ).scalar_one_or_none()

    if not notice_user:
        raise HTTPException(status_code=404, detail="User not in active notice")

    # 공지 정보 반환
    return read_notice(notice_user.notice_id, db)


# 특정 유저의 간단한 공지 조회 (순찰 시간 이전까지)
@app.get("/notices/user/{user_id}/simple")
def get_user_simple_notice(
    user_id: str, db: Session = Depends(get_db)
) -> NoticeSimpleSchema:
    # 유저가 할당된 활성 공지 조회 (순찰 시간 이전까지만)
    current_time = datetime.now()

    notice_user = db.execute(
        select(NoticeUser)
        .join(Notice)
        .where(
            NoticeUser.user_id == user_id,
            Notice.active,
            Notice.scheduled_time > current_time,  # 순찰 시간 이전까지만
        )
    ).scalar_one_or_none()

    if not notice_user:
        raise HTTPException(status_code=404, detail="No active notice found for user")

    notice = notice_user.notice

    # 참여 유저들의 이름 조회
    assigned_users = (
        db.execute(
            select(NoticeUser).join(User).where(NoticeUser.notice_id == notice.id)
        )
        .scalars()
        .all()
    )

    user_names = [nu.user.name for nu in assigned_users]

    return NoticeSimpleSchema(
        id=notice.id,
        location=notice.location,
        location_lat=notice.location_lat,
        location_lon=notice.location_lon,
        scheduled_time=notice.scheduled_time,
        user_names=user_names,
    )


# 공지 삭제 Delete
@app.delete("/notices/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db)) -> NoticeSchema:
    notice = db.execute(
        select(Notice).where(Notice.id == notice_id)
    ).scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # 삭제 전에 공지 정보 저장
    deleted_notice = NoticeSchema(
        id=notice.id,
        title=notice.title,
        content=notice.content,
        location=notice.location,
        location_lat=notice.location_lat,
        location_lon=notice.location_lon,
        scheduled_time=notice.scheduled_time,
        active=notice.active,
        assigned_users=[],  # 삭제되었으므로 빈 리스트
    )

    # 공지 삭제 시 관련된 NoticeUser도 함께 삭제됨 (CASCADE)
    db.delete(notice)
    db.commit()

    return deleted_notice


# 공지에 유저 추가
@app.post("/notices/{notice_id}/users")
def add_user_to_notice(
    notice_id: int, user_id: str, db: Session = Depends(get_db)
) -> NoticeSchema:
    # 공지 존재 확인
    notice = db.execute(
        select(Notice).where(Notice.id == notice_id)
    ).scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # 유저 존재 확인
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 이미 할당된지 확인
    existing = db.execute(
        select(NoticeUser).where(
            NoticeUser.notice_id == notice_id, NoticeUser.user_id == user_id
        )
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="User already assigned to notice")

    # 유저 추가
    notice_user = NoticeUser(notice_id=notice_id, user_id=user_id, confirmed=False)
    db.add(notice_user)
    db.commit()

    # 업데이트된 공지 정보 반환
    return read_notice(notice_id, db)


# 공지에서 유저 제거
@app.delete("/notices/{notice_id}/users/{user_id}")
def remove_user_from_notice(
    notice_id: int, user_id: str, db: Session = Depends(get_db)
) -> NoticeSchema:
    notice_user = db.execute(
        select(NoticeUser).where(
            NoticeUser.notice_id == notice_id, NoticeUser.user_id == user_id
        )
    ).scalar_one_or_none()

    if not notice_user:
        raise HTTPException(status_code=404, detail="User not assigned to notice")

    db.delete(notice_user)
    db.commit()

    # 업데이트된 공지 정보 반환
    return read_notice(notice_id, db)


# 공지의 유저 목록 조회
@app.get("/notices/{notice_id}/users")
def get_notice_users(
    notice_id: int, db: Session = Depends(get_db)
) -> list[NoticeUserSchema]:
    # 공지 존재 확인
    notice = db.execute(
        select(Notice).where(Notice.id == notice_id)
    ).scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # 공지의 유저들 조회
    assigned_users = (
        db.execute(select(NoticeUser).where(NoticeUser.notice_id == notice_id))
        .scalars()
        .all()
    )

    return [
        NoticeUserSchema(user_id=nu.user_id, confirmed=nu.confirmed)
        for nu in assigned_users
    ]


# 특정 유저의 가장 가까운 미래 순찰 조회 (공지용)
@app.get("/patrols/user/{user_id}/next")
def get_user_next_patrol(
    user_id: str, db: Session = Depends(get_db)
) -> PatrolNoticeSchema:
    # 유저 존재 확인
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_time = datetime.now()

    # 유저가 참여하는 가장 가까운 미래 순찰 조회
    next_patrol_user = db.execute(
        select(PatrolUser)
        .join(Patrol)
        .where(
            PatrolUser.user_id == user_id,
            Patrol.start_time > current_time,  # 미래 순찰만
            Patrol.active,  # 활성 순찰만
        )
        .order_by(Patrol.start_time.asc())  # 가장 가까운 순서로 정렬
    ).scalar_one_or_none()

    if not next_patrol_user:
        raise HTTPException(status_code=404, detail="No future patrol found for user")

    patrol = next_patrol_user.patrol

    # 함께 순찰하는 유저들의 이름 조회
    patrol_users = (
        db.execute(
            select(PatrolUser).join(User).where(PatrolUser.patrol_id == patrol.id)
        )
        .scalars()
        .all()
    )

    user_names = [pu.user.name for pu in patrol_users]

    return PatrolNoticeSchema(
        id=patrol.id,
        name=patrol.name,
        start_lat=patrol.start_lat,
        start_lon=patrol.start_lon,
        start_time=patrol.start_time,
        user_names=user_names,
    )
