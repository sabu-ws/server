import os
from dotenv import dotenv_values

DOT_ENV = dotenv_values(".env")

# SABU version
SABU_VERSION = "2.3.0"

# SABU licence
SABU_LICENCE = "0"

# SABU path
ROOT_PATH = "/sabu/"
SERVER_PATH = "/sabu/server"
DATA_PATH = DOT_ENV["DATA_PATH"]
SCRIPT_PATH = "/sabu/server/core/scripts/"
CONFIG_PATH = os.path.join(SERVER_PATH, "config")
LOG_PATH = os.path.join(SERVER_PATH, "logs")


# reverse proxy
NB_REVERSE_PROXY = 1


# Upload content
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024


# Database content
DB_HOST = DOT_ENV["POSTGRES_HOST"]
DB_NAME = DOT_ENV["POSTGRES_DB"]
DB_USERNAME = DOT_ENV["POSTGRES_USER"]
DB_PASSWORD = DOT_ENV["POSTGRES_PASSWORD"]

# Redis content
REDIS_HOST = DOT_ENV["REDIS_HOST"]
REDIS_PORT = DOT_ENV["REDIS_PORT"]
REDIS_PASSWORD = DOT_ENV["REDIS_PASSWORD"]
REDIS_DB_CACHE = DOT_ENV["REDIS_DB_CACHE"]
REDIS_DB_CELERY = DOT_ENV["REDIS_DB_CELERY"]

# Scoring verification
scoring = 0.9