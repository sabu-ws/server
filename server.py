from app import socketio
from app import app
import eventlet

if __name__ == '__main__':
	# eventlet.monkey_patch()
	socketio.run(app,"0.0.0.0",8888,debug=True)
