
from flask import Flask, jsonify, render_template
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    # Generate a new flow rate and timestamp each time this endpoint is called
    flow_rate = round(random.uniform(0.5, 100.0), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Define usage thresholds for fine and reward
    high_usage_threshold = 80.0
    low_usage_threshold = 10.0
    
    # Fine and reward logic
    fine = 0
    reward = 0
    
    if flow_rate > high_usage_threshold:
        fine = round((flow_rate - high_usage_threshold) * 2, 2)  # Example fine calculation
    elif flow_rate < low_usage_threshold:
        reward = round(low_usage_threshold - flow_rate, 2)  # Example reward calculation
    
    # Prepare the data to be sent
    data = {
        'timestamp': timestamp,
        'flow_rate': flow_rate,
        'fine': fine,
        'reward': reward
    }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
