from flask import Flask, render_template, jsonify
import random
import time
import threading

app = Flask(__name__)

# Store data globally for demo purposes
latest_data = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'flow_rate': round(random.uniform(0.0, 100.0), 2)
}

def update_data():
    """Function to update the latest data every minute."""
    global latest_data
    latest_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    latest_data['flow_rate'] = round(random.uniform(0.0, 100.0), 2)
    
    # Schedule the function to run again after 60 seconds (1 minute)
    threading.Timer(60, update_data).start()

# Start the first update
update_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    """API endpoint to fetch the latest data."""
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
