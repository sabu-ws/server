from flask import session
import logging
import json

log_format = "%(levelname)s [%(asctime)s] %(name)s  %(message)s"
logging.basicConfig(format=log_format,level=logging.INFO,filename="/sabu/logs/server/sabu.log",filemode="a")
log = logging.getLogger("sabu.server.api")

class ApiWS:
    def __init__(self,app,redis,key_prefix="API_"):
        self.app = app
        self.redis = redis
        self.key_prefix = key_prefix
    
    def load_session(self,key,timeout=30):
        concat = self.key_prefix+key 
        log.info(concat)
        log.info(str(type(session)))
        self.redis.set(concat,"session",ex=timeout)

    def is_load(self):
        pass

    def unload_session(self):
        pass
    