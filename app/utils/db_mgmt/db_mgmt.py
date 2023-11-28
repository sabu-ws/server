from config import *


from sqlalchemy import URL
from flask import current_app

import os

def database_allowed(root_path=None):
    if str(DB_PROTOCOLE) in ["sqlite"]:
        # print(app.root_path)
        if not os.path.exists(os.path.join(os.path.dirname(root_path),"instance")):
            os.makedirs(os.path.join(os.path.dirname(root_path),"instance"))
        db_path = os.path.join(SERVER_PATH,"instance",DB_NAME)
        return URL.create(
            DB_PROTOCOLE,
            database=db_path,
        )
    elif str(DB_PROTOCOLE) in ["postgresql","postgresql+psycopg2","postgresql+pg8000","mysql","mysql+mysqldb","mysql+pymysql","oracle","oracle+cx_oracle","mssql+pyodbc","mssql+pymssql"]:
        return URL.create(
            DB_PROTOCOLE,
            username=DB_USERNAME,
            password=str(DB_PASSWORD),
            host=DB_HOST,
            database=DB_NAME,
        )