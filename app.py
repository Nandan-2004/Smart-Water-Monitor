@app.route('/get_data')
def get_data():
    try:
        # Fetch data from the ESP32 (IoT device)
        response = requests.get(ESP32_URL)
        data = response.json()

        # Extract flow rate and timestamp
        flow_rate = data['flow_rate']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fine and reward logic
        fine_rate = 5.0
        reward_amount = 2
        high_usage_threshold = 80.0
        low_usage_threshold = 10.0

        fine = 0
        reward = 0

        if flow_rate > high_usage_threshold:
            fine = (flow_rate - high_usage_threshold) * fine_rate
        elif flow_rate < low_usage_threshold:
            reward = reward_amount

        data = {'timestamp': timestamp, 'flow_rate': flow_rate, 'fine': fine, 'reward': reward}
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Unable to fetch data from IoT device"}), 500
