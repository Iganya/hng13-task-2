from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

# MYSQL_USER = os.getenv("MYSQL_USER")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# MYSQL_HOST = os.getenv("MYSQL_HOST")
# MYSQL_PORT = os.getenv("MYSQL_PORT")
# MYSQL_DB = os.getenv("MYSQL_DB")

# DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
# DB_URL = f"mysql+pymysql://user:QiPHEWAwmLoTxdCcUNVXVxonSNbeKsBu@mysql.railway.internal:3306/railway"

DB_URL = os.getenv('DATABASE_URL')
print(DB_URL)
if not DB_URL:
    DB_URL = "mysql+pymysql://root:QiPHEWAwmLoTxdCcUNVXVxonSNbeKsBu@yamanote.proxy.rlwy.net:38872/railway"


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()