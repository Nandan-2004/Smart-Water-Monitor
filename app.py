from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
from datetime import datetime
from threading import Thread
import os  # Import os to get the PORT environment variable

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

# Emit data every few seconds
def emit_data():
    while True:
        # Example data to emit
        data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'flow_rate': round(random.uniform(0.0, 100.0), 2)  # Example flow rate value
        }
        print("Emitting data:", data)  # Server log for debugging
        socketio.emit('new_data', data)
        time.sleep(60)  # Adjust frequency as needed

recent_readings = [
    {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "flow_rate": round(random.uniform(0.0, 100.0), 2)}
    for _ in range(10)  # Generating 10 random readings
]

# Run emit_data in a background thread
thread = Thread(target=emit_data)
thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
