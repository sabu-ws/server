from functools import wraps


def read_and_forward_pty_output(fd=None, pid=None, room_id=None):
	status = psutil.Process(pid).status()
	"""
	read data on pty master from the pty slave, and emit to the web terminal visitor
	"""
	max_read_bytes = 1024 * 20
	while True:
		# using flask default web server, or uwsgi production web server
		# when the child process is terminated, it will not disappear from linux process list
		# and keep staying as a zombie process until the parent exits.
		try:
			child_process = psutil.Process(pid)
		except psutil.NoSuchProcess as err:
			return
		if child_process.status() not in ('running', 'sleeping'):
			return
		if fd:
			timeout_sec = 0
			(data_ready, _, _) = select.select([fd], [], [], timeout_sec)

			if data_ready:
				try:
					output = os.read(fd, max_read_bytes).decode()
				except Exception as err:
					output = """
					***AQUI WEB TERM ERR***
					{}
					***********************
				""".format(err)
				socketio.emit("pty-output", {"output": output}, namespace="/pty",room=room_id)