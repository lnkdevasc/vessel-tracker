import logging
from flask import Flask, render_template, redirect, url_for, jsonify
import redis
import os

app = Flask(__name__)

# --- NEW: Setup Logging to a file ---
logging.basicConfig(
    filename='/app/vessel.log', 
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

r = redis.Redis(
    host='vessel-db', 
    port=6379, 
    password=os.getenv("DB_PASSWORD"), 
    decode_responses=True
)

@app.route('/')
def index():
    hits = r.incr('hits')
    app.logger.info(f"Dashboard accessed. Total hits: {hits}")
    
    vessel_data = {
        "ship_name": "Surabaya Express",
        "status": "Active",
        "location": "Madura Strait",
        "cpu_telemetry": 32.8,
        "mem_telemetry": 58.9,
        "disk_telemetry": 52
    }
    return render_template('index.html', vessel=vessel_data, count=hits)

# --- NEW: Monitoring Route ---
@app.route('/logs')
def get_logs():
    try:
        with open('/app/vessel.log', 'r') as f:
            # Get the last 10 lines of logs
            lines = f.readlines()
            return jsonify(lines[-10:])
    except Exception as e:
        return jsonify([f"Error reading logs: {str(e)}"])

@app.route('/refresh')
def refresh():
    app.logger.warning("Manual refresh triggered by user.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)