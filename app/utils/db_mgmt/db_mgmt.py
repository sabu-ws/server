from config import *


from sqlalchemy import URL

import os


def database_allowed(root_path=None):
    if str(DB_PROTOCOLE) == "sqlite":
        if not os.path.exists(os.path.join(os.path.dirname(root_path), "instance")):
            os.makedirs(os.path.join(os.path.dirname(root_path), "instance"))
        db_path = os.path.join(SERVER_PATH, "instance", DB_NAME)
        return URL.create(
            DB_PROTOCOLE,
            database=db_path,
        )
    elif str(DB_PROTOCOLE) == "postgresql+psycopg2":
        SQLALCHEMY_URL = f"postgresql+psycopg2://{str(DB_USERNAME)}:{str(DB_PASSWORD)}@127.0.0.1:5432/{str(DB_NAME)}"
        return SQLALCHEMY_URL

    else:
        return None
