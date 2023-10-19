from app import socketio
from app import app
import eventlet

if __name__ == '__main__':
	# eventlet.monkey_patch()
	certfile = "/sabu/nginx/certificates/sabu-gui.crt"
	keyfile = "/sabu/nginx/certificates/sabu-gui.key"
	# socketio.run(app,"127.0.0.1",8888,debug=True,keyfile=keyfile,certfile=certfile)
	socketio.run(app,"127.0.0.1",8888,debug=True)
