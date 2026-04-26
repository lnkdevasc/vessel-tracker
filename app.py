from flask import Flask, render_template, redirect, url_for
import redis
import os

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host='vessel-db', 
    port=6379, 
    password=os.getenv("DB_PASSWORD"), 
    decode_responses=True
)

@app.route('/')
def index():
    # Increment and get the count
    hits = r.incr('hits')
    
    # We pass more complex 'telemetry' data to the template
    # These values will map to our static design
    vessel_data = {
        "ship_name": "Surabaya Express",
        "status": "Active",
        "location": "Madura Strait",
        # Telemetry to match the reference look
        "cpu_telemetry": 32.8,
        "mem_telemetry": 58.9,
        "disk_telemetry": 52
    }
    
    return render_template('index.html', vessel=vessel_data, count=hits)

@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)