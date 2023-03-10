
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas
from fastapi import HTTPException

# DBのCRUD操作を関数化、再利用できるようにする
# sqlAlchemyを使っているため、SQL文ではなくpythonで書ける

# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
    # db.query(models.User).all() でもok
    # queryでDBを検索、データを取得する


# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()

# ユーザー登録
def create_user(db: Session, user: schemas.User): # FastAPI側でreq.paramを受け取るため、型はschemas
    db_user = models.User(user_name=user.user_name) # DBにparamを追加するため、型はmodels(sqlAlchemy)
    db.add(db_user) # DBに値を追加（登録手前、git addに似てる）
    db.commit() # DBに値追加を反映
    db.refresh(db_user) # インスタンスをDBに値が追加された状態に更新する
    return db_user

# 会議室登録
def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
    # バリデーションチェック
    # queryでDBから予約済みデータ(models.Booking)をリスト型(.all())で取得
    # POSTパラメータ(booking)と重複するデータをfilter
    db_booked = db.query(models.Booking).\
        filter(models.Booking.room_id == booking.room_id).\
        filter(models.Booking.end_datetime > booking.start_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).\
        all()
        # room_idが一致
        # 予約済み終了時間 > POST_param 開始時間
        # 予約済み開始時間 < POST_param 終了時間

    # 重複するデータがなければデータを追加
    if len(db_booked) == 0:
        db_booking = models.Booking(
            user_id = booking.user_id,
            room_id = booking.room_id,
            booked_num = booking.booked_num,
            start_datetime = booking.start_datetime,
            end_datetime = booking.end_datetime
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    else:
        raise HTTPException(status_code=404, detail="Already booked") # FastAPIでerrorレスポンス
