from magika import Magika
import os

from app import logger as log

def control(path):
    m = Magika()
    res = m.identify_bytes(b"# Example\nThis is an example of markdown!")
    log.info(str(res.output.ct_label))