import streamlit as st
import datetime
import requests
import json
import pandas as pd

# frontend
page = st.sidebar.selectbox("chose a page", ["users", "rooms", "bookings"])

if page == "bookings":
    st.title("予約登録")
    # ユーザー一覧取得
    url_users = "http://127.0.0.1:8000/users"
    res = requests.get(url_users)
    users = res.json()  # [0:{"user_name":"user1" "user_id":1} 1:{}...]
    # st.json(users) # test

    # ユーザー名をキー、ユーザーIDをバリュー # {"user1":1 "user2":2...}
    users_dict = {}
    for user in users:
        users_dict[user["user_name"]] = user["user_id"]
    # st.write(users_dict) # test

    # 会議室一覧取得
    url_rooms = "http://127.0.0.1:8000/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()  # [0:{"room_name":"room1" "room_id":1} 1:{}...]
    # st.json(rooms)  # test

    # 会議室名をキー、会議室IDをバリュー {"room1":{"room_id":1" capacity":1}...}
    rooms_dict = {}
    for room in rooms:
        rooms_dict[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"],
        }
    # st.write(rooms_dict)  # test

    st.write("### 会議室一覧")
    df_rooms = pd.DataFrame(rooms)  # json型からデータフレーム型に変換
    df_rooms.columns = ["会議室名", "定員", "会議室ID"]  # カラム名(room_name/capacity/id)表記を変更
    st.table(df_rooms)  # 表で表示

    with st.form(key="booking"):
        user_name: str = st.selectbox("予約者名", users_dict.keys())
        room_name: str = st.selectbox("会議室名", rooms_dict.keys())
        # booking_id: int = random.randint(0, 10)
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)  # step=1刻み
        date = st.date_input("日付", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻: ", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻: ", value=datetime.time(hour=20, minute=0))
        # stremlitの仕様で15分刻み、時間制限は付けられない

        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        user_id: int = users_dict[user_name]
        room_id: int = rooms_dict[room_name]["room_id"]
        capacity: int = rooms_dict[room_name]["capacity"]

        data = {
            # "booking_id": booking_id,
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
            ).isoformat(),  # FastAPIはdatetimeをstring型しか受け付けない
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat(),
        }

        # 定員より多い予約人数の場合
        if booked_num > capacity:
            st.error(f"{room_name}の定員は、{capacity}名です。{capacity}名以下の予約人数のみ受け付けております。")
        # 予約人数が定員以下の場合、会議室予約
        if booked_num <= capacity:
            url = "http://127.0.0.1:8000/bookings"
            res = requests.post(url, data=json.dumps(data))

            if res.status_code == 200:
                st.success("予約完了しました")
                st.write(res.status_code)
                st.json(res.json())



elif page == "users":
    st.title("user登録")

    with st.form(key="user"):
        # user_id: int = random.randint(0, 10) # test
        user_name: str = st.text_input("user名", max_chars=12)
        data = {
            # "user_id": user_id, # test
            "user_name": user_name
        }
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        # st.write("## 送信データ") # test
        # st.json(data) # test

        # st.write("## レスポンス結果") # test
        url = "http://127.0.0.1:8000/users"
        res = requests.post(url, data=json.dumps(data))
        # st.write(res.status_code) # test
        if res.status_code == 200:
            st.success("登録完了")
            st.json(res.json())


elif page == "rooms":
    st.title("会議室登録")

    with st.form(key="room"):
        room_name: str = st.text_input("room名", max_chars=12)
        capacity: int = st.number_input("定員", step=1)  # step=1刻み
        data = {"room_name": room_name, "capacity": capacity}
        submit_button = st.form_submit_button(label="登録")

    if submit_button:
        url = "http://127.0.0.1:8000/rooms"
        res = requests.post(url, data=json.dumps(data))
        if res.status_code == 200:
            st.success("登録完了")
            st.json(res.json())
