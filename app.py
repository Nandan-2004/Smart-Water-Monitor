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
    data = {'timestamp': timestamp, 'flow_rate': flow_rate}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
