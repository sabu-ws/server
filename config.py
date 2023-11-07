import os

# SABU path
ROOT_PATH = "/mnt/usb/"
MASTER_PATH = "/sabu"
SCRIPT_PATH = os.path.join(MASTER_PATH,"scripts")
CONFIG_PATH = os.path.join(MASTER_PATH,"config")
LOG_PATH = os.path.join(MASTER_PATH,"logs")


# database
db_name = "database.db"


# reverse proxy
NB_REVERSE_PROXY=1


# Upload content
MAX_CONTENT_LENGTH = 500*1024*1024
