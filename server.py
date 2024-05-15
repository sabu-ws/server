from app import socketio
from app import app

if __name__ == "__main__":
    # For production
    # socketio.run(app,"127.0.0.1", 8888, debug=True, use_reloader=False)

    # For dev
    socketio.run(app, "127.0.0.1", 8888, debug=True, use_reloader=True)
