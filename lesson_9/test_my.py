from sqlalchemy import create_engine, text

# Подключение к MySQL
username = 'root'
password = 'mmqalzctzion'
host = 'localhost'
port = '3306'
database = 'domaska'

db_connection_string = "mysql+pymysql://root:mmqalzctzion@localhost:3306/domaska"
engine = create_engine(db_connection_string)

with engine.connect() as connection:
    result= connection.execute(text("SELECT * FROM company"))
    rows= result.mappings().all()
    print(rows)
