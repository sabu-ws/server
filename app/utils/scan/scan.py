# from celery import shared_task
from app import scanner 
from celery import group
import time

@scanner.task
def hello():
	time.sleep(5)
	return 'hello world'

@scanner.task
def hello2():
	time.sleep(7)
	return 'hello world 2'