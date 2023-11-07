from app import socketio
from app import app
import eventlet

if __name__ == '__main__':

	eventlet.monkey_patch()
	cert_file="/sabu/ssl/sabu.crt"
	key_file="/sabu/ssl/private/saby.key"

	socketio.run(app,"127.0.0.1", 8888, certfile=cert_file, keyfile=key_file, debug=True)
