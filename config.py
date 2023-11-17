import os

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
DB_PROTOCOLE = "sqlite"
DB_NAME = "database.db"
DB_USERNAME = ""
DB_PASSWORD = ""
DB_HOST = ""