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

        # Use global to update the global latest_data variable
        global latest_data
        latest_data = response_data

        return jsonify(response_data), 200  # Return data with HTTP 200 status
    except Exception as e:
        return jsonify({'error': str(e)}), 400
