from flask import Flask, render_template, jsonify
import random
import time
from datetime import datetime

app = Flask(__name__)

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

# Use an external cron job or scheduling mechanism to update data

if __name__ == '__main__':
    app.run(host='0.0.0.0')  # Simplified, no need to manually set the port for Vercel
