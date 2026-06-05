'''
Created on 2026/05/07

@author: i-furuya02
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://{role名}:{パスワード}@{DBサーバーのIPアドレス}:{PostgreSQLのポート番号}/{DB名}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
