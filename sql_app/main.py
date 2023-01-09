from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# FastAPI

models.Base.metadata.create_all(bind=engine)
# modelsファイルからBaseを読み込み、DB engineを元にDBエンジンを作成

app = FastAPI()  # インスタンス化


def get_db():
    db = SessionLocal()  # session（DB接続の一連の流れ）を読み込む
    try:
        yield db
    finally:
        db.close()


# ルーティング

# Read
@app.get("/users", response_model=List[schemas.User])  # アクセスを受け取る
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):  # DBセッション確立
    users = crud.get_users(db, skip=skip, limit=limit)  # crudでDBからデータを取得したものが返る
    return users


@app.get("/rooms", response_model=List[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms


@app.get("/bookings", response_model=List[schemas.Booking])
async def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings


# Create
@app.post("/users", response_model=schemas.User)  # idを含むモデルをreturnする
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # user（:schema idを含まないcreateモデル）でparamを受け取る。
    return crud.create_user(db=db, user=user)  # 今回はDBに追加したデータを返す


@app.post("/rooms", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)


@app.post("/bookings", response_model=schemas.Booking)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)
