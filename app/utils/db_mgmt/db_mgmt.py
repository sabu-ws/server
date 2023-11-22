from config import *

from sqlalchemy import URL


def database_allowed():
    if str(DB_PROTOCOLE) in ["sqlite"]:
        return URL.create(
            DB_PROTOCOLE,
            database=DB_NAME,
        )
    elif str(DB_PROTOCOLE) in ["postgresql","postgresql+psycopg2","postgresql+pg8000","mysql","mysql+mysqldb","mysql+pymysql","oracle","oracle+cx_oracle","mssql+pyodbc","mssql+pymssql"]:
        return URL.create(
            DB_PROTOCOLE,
            username=DB_USERNAME,
            password=str(DB_PASSWORD),
            host=DB_HOST,
            database=DB_NAME,
        )