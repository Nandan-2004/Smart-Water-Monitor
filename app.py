from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the ESP32 or frontend

# Global variable to store the latest data
latest_data = {}

# Route for the homepage (optional)
@app.route('/')
def index():
    return render_template('index.html')  # Ensure 'index.html' exists in 'templates/' folder

# Route to receive data from ESP32
@app.route('/post_data', methods=['POST'])
def post_data():
    try:
        # Read data sent by the ESP32 (as JSON)
        data = request.get_json()

        # Extract flow rate from the ESP32 data
        flow_rate = data.get('flow_rate', 0)  # Default to 0 if not provided
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Define thresholds
        high_usage_threshold = 80.0  # Fine if flow rate exceeds this
        low_usage_threshold = 10.0  # Reward if flow rate is below this

        # Calculate fine and reward
        fine = 0
        reward = 0
        if flow_rate > high_usage_threshold:
            fine = round((flow_rate - high_usage_threshold) * 10, 2)
        elif flow_rate < low_usage_threshold:
            reward = round((low_usage_threshold - flow_rate), 2)

        # Prepare response data
        response_data = {
            'timestamp': timestamp,
            'flow_rate': flow_rate,
            'fine': fine,
            'reward': reward
        }

        # Update the latest data
        latest_data = response_data

        return jsonify(response_data), 200  # Return data with HTTP 200 status
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to get the latest data
@app.route('/get_data', methods=['GET'])
def get_data():
    if latest_data:
        return jsonify(latest_data), 200
    else:
        return jsonify({'error': 'No data available'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
