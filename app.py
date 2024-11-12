from flask import Flask, render_template, jsonify
import random
import time
from datetime import datetime
from threading import Thread
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Store data globally for demo purposes
latest_data = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'flow_rate': round(random.uniform(0.0, 100.0), 2)
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    """API endpoint to fetch latest data."""
    return jsonify(latest_data)

# Simulate data updates in a background task
def update_data():
    global latest_data
    while True:
        latest_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'flow_rate': round(random.uniform(0.0, 100.0), 2)
        }
        time.sleep(60)  # Update every 60 seconds

# Start data update task
Thread(target=update_data, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
