from flask import Flask, jsonify, render_template, request
import requests  # To fetch data from ESP32
from datetime import datetime

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
        response = requests.get(192.168.107.97,timeout=5)  # Adjust timeout as needed
        response.raise_for_status()  # Raise exception for HTTP errors
        
        esp_data = response.json()  # Assuming ESP32 sends JSON data

        # Extract data from ESP32 response
        flow_rate = esp_data.get('flow_rate', 0)  # Replace 'flow_rate' with the correct key
        timestamp = esp_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Define usage thresholds for fine and reward
        high_usage_threshold = 15  # Example threshold
        low_usage_threshold = 2

        # Fine and reward logic
        fine = 0
        reward = 0

        if flow_rate > high_usage_threshold:
            fine = round((flow_rate - high_usage_threshold) * 2, 2)  # Example fine calculation
        elif flow_rate < low_usage_threshold:
            reward = round(low_usage_threshold - flow_rate, 2)  # Example reward calculation

        # Prepare the response data
        data = {
            'timestamp': timestamp,
            'flow_rate': flow_rate,
            'fine': fine,
            'reward': reward
        }

    except (requests.RequestException, ValueError) as e:
        # Handle exceptions (e.g., ESP32 not reachable, invalid JSON)
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
