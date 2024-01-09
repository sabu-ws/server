import os
from dotenv import dotenv_values

DOT_ENV = dotenv_values(".env")

# SABU version
SABU_VERSION = "0.2.5"

# SABU licence
SABU_LICENCE = "1"

# SABU path
ROOT_PATH = "/mnt/usb/"
SERVER_PATH = "/sabu/server/"
# SCRIPT_PATH = os.path.join(SERVER_PATH, "scripts")
SCRIPT_PATH = "/sabu/server/core/scripts/"
CONFIG_PATH = os.path.join(SERVER_PATH, "config")
LOG_PATH = os.path.join(SERVER_PATH, "logs")


# reverse proxy
NB_REVERSE_PROXY = 1


# Upload content
MAX_CONTENT_LENGTH = 500 * 1024 * 1024


# Database content
DB_HOST = DOT_ENV["POSTGRES_HOST"]
DB_NAME = DOT_ENV["POSTGRES_DB"]
DB_USERNAME = DOT_ENV["POSTGRES_USER"]
DB_PASSWORD = DOT_ENV["POSTGRES_PASSWORD"]
