from flask import Flask, jsonify, render_template, request
import requests  # To fetch data from ESP32
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# ESP32 endpoint URL (replace with the correct IP or hostname of the ESP32 device)
ESP32_URL = "http://192.168.107.97/sensor_data"  # Example: http://192.168.1.10/sensor_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Fetch data from the ESP32
        response = requests.get(ESP32_URL, timeout=5)
        response.raise_for_status()  # Raise exception for HTTP errors

        esp_data = response.json()  # Assuming ESP32 sends JSON data
        flow_rate = float(esp_data.get('flow_rate', 0))  # Replace with actual key
        timestamp = esp_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Usage thresholds
        high_usage_threshold = 15
        low_usage_threshold = 2

        # Calculate fine and reward
        fine = round(max(0, (flow_rate - high_usage_threshold) * 2), 2)
        reward = round(max(0, (low_usage_threshold - flow_rate) * 3), 2)

        # Response data
        data = {
            'timestamp': timestamp,
            'flow_rate': flow_rate,
            'fine': fine,
            'reward': reward
        }

    except (requests.RequestException, ValueError) as e:
        # Handle exceptions
        data = {
            'error': str(e),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'flow_rate': 0,
            'fine': 0,
            'reward': 0
        }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
