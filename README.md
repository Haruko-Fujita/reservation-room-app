## 会議室予約アプリ
- Python
- Framework: back_FastAPI/front_streamlit
- ORM: SQLAlchemy
- DB: sqlite

### 選定理由
- Python の習得: データ分析に興味あるため
- シェアリングサービスに使われる予約機能の基礎を学ぶ
- FastAPI: 少ないコード量で実装できるため理解しやすい。Djangoは多機能すぎるため除外。
### 実装のポイント
- バリデーションチェック: back_予約重複チェック、front_入力値のチェック
- DBデータをリスト化: front_ユーザーや会議室選択時にDBマスタを利用
- Datetime型の使用: APIの値受け渡し時のFrameworkの関係や型の理解