from config import *
from celery import Celery
from app import app

redis_client_scanner_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{int(REDIS_PORT)}/{int(REDIS_DB_CELERY)}"



scanner = Celery("sabu")
scanner.conf.update(
    broker_url = redis_client_scanner_url,
    result_backend = redis_client_scanner_url,
    broker_transport = 'redis',
    broker_connection_retry_on_startup = True,
)
class ContextTask(scanner.Task):
	def __call__(self, *args, **kwargs):
		with app.app_context():
			return self.run(*args, **kwargs)
scanner.Task = ContextTask