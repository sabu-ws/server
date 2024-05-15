from config import *
from sqlalchemy import URL

import os


def database_allowed():
    SQLALCHEMY_URL = f"postgresql+psycopg2://{str(DB_USERNAME)}:{str(DB_PASSWORD)}@{str(DB_HOST)}/{str(DB_NAME)}"
    return SQLALCHEMY_URL
