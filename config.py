import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # 預設使用 PostgreSQL (同 ref 範例)，若設置 DATABASE_URL 則以環境變數為主
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:shi2xiu1@localhost/final-hw'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
