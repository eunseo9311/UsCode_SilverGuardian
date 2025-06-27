from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

from db import User, Patrol, Base, engine
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
    id: int
    name: str
    lat: float  # 위도
    lon: float  # 경도

# class Patrol(BaseModel):
#     id: int
#     user_id: int
#     user_name: str
#     start_lat: float  # 순찰 시작 위도
#     start_lon: float  # 순찰 시작 경도
#     end_lat: Optional[float] = None  # 순찰 종료 위도
#     end_lon: Optional[float] = None  # 순찰 종료 경도
#     start_time: datetime  # 순찰 시작 시간
#     end_time: Optional[datetime] = None  # 순찰 종료 시간
#     memo: Optional[str] = None  # 메모
#     is_active: bool = True  # 순찰 중인지 여부

users = {}
patrols = {}  # 순찰 데이터 저장
patrol_counter = 1  # 순찰 ID 자동 생성용


@app.get("/")
def read_root():
    return {"message": "Hello from uscode-silverguardian!"}

# @app.post("/users")
# def create_user(user: User):
#     if user.id in users:
#         return {"error": "User already exists"}
#     users[user.id] = user
#     return user

# @app.get("/users")
# def read_users():
#     return list(users.values())

@app.get("/users/qr/{uuid}")
def create_user_qr(uuid: str, lat: float, lon: float, db: Session = Depends(get_db))-> UserSchema:
    user = db.execute(select(User).where(User.id == uuid)).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=404, detail="User already exists")
    user = User(id=uuid, name="정해지지 않음", lat=lat, lon=lon)
    db.add(user)
    db.commit()
    return user

# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     if user_id not in users:
#         return {"error": "User not found"}
#     return users[user_id]

# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: User):
#     if user_id not in users:
#         return {"error": "User not found"}
#     users[user_id] = user
#     return user

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     if user_id not in users:
#         return {"error": "User not found"}
#     del users[user_id]
#     return {"result": "User deleted"}

# # 순찰 관련 API들
# @app.post("/patrols/start", response_model=Patrol, response_model_exclude_none=True)
# def start_patrol(patrol_data: Patrol):
#     """순찰 시작"""
#     global patrol_counter
    
#     user_id = patrol_data.user_id
#     start_lat = patrol_data.start_lat
#     start_lon = patrol_data.start_lon
#     user = users[user_id]
    
#     # 이미 순찰 중인지 확인
#     for patrol in patrols.values():
#         if patrol.user_id == user_id and patrol.is_active:
#             return {"error": "User is already on patrol"}
    
#     patrol = Patrol(
#         id=patrol_counter,
#         user_id=user_id,
#         user_name=user.name,
#         start_lat=start_lat,
#         start_lon=start_lon,
#         start_time=datetime.now(),
#         is_active=True
#     )
    
#     patrols[patrol_counter] = patrol
#     patrol_counter += 1
    
#     return patrol

# @app.get("/patrols/active")
# def get_active_patrols():
#     """순찰 중인 유저들 목록"""
#     active_patrols = [patrol for patrol in patrols.values() if patrol.is_active]
#     return active_patrols

# @app.get("/patrols")
# def get_all_patrols():
#     """모든 순찰 기록"""
#     return list(patrols.values())

# @app.get("/patrols/{patrol_id}")
# def get_patrol(patrol_id: int):
#     """특정 순찰 기록 조회"""
#     if patrol_id not in patrols:
#         return {"error": "Patrol not found"}
#     return patrols[patrol_id]

# @app.put("/patrols/{patrol_id}/end")
# def end_patrol(patrol_id: int, end_data: dict):
#     """순찰 종료"""
#     if patrol_id not in patrols:
#         return {"error": "Patrol not found"}
    
#     patrol = patrols[patrol_id]
#     if not patrol.is_active:
#         return {"error": "Patrol already ended"}
    
#     patrol.end_lat = end_data.get("end_lat")
#     patrol.end_lon = end_data.get("end_lon")
#     patrol.end_time = datetime.now()
#     patrol.is_active = False
    
#     return patrol

# @app.put("/patrols/{patrol_id}/memo")
# def update_patrol_memo(patrol_id: int, memo_data: dict):
#     """순찰 메모 업데이트"""
#     if patrol_id not in patrols:
#         return {"error": "Patrol not found"}
    
#     patrol = patrols[patrol_id]
#     patrol.memo = memo_data.get("memo")
    
#     return patrol

# @app.get("/patrols/user/{user_id}")
# def get_user_patrols(user_id: int):
#     """특정 유저의 순찰 기록"""
#     user_patrols = [patrol for patrol in patrols.values() if patrol.user_id == user_id]
#     return user_patrols
