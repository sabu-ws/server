from config import *

from app import logger as log
from app.models import Extensions

from pathlib import Path
from magika import Magika
import os


def control(content, list_ext_valid):
    m = Magika()
    res = m.identify_bytes(content)
    log.info(str(res))
    if res.output.mime_type in list_ext_valid and res.output.score >= scoring:
        return True
    else:
        return False
