from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  # sqliteはDBサーバーがなく、ファイルで管理する

# engineをインスタンス化
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # sqliteの設定
)
# sessionはdbに接続、切断する役割、一連の流れを定義、インスタンス化
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# DBの型クラスを継承
Base = declarative_base()
