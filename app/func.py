# from app import scheduler
# from functools import wraps

# @scheduler.task('cron', id='do_job_2', second=30)
# def job2():
# 	app.logger.info('Job 2 executeddddd')
# 	with scheduler.app.app_context():
# 		app.logger.info('Job 2 executed')