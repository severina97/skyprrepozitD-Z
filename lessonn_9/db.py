from sqlalchemy import create_engine
from config import username, password, host, port, database

db = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)
