from flask import Flask, render_template, redirect, url_for
import redis
import os

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host='vessel-db', 
    port=6379, 
    password=os.getenv("DB_PASSWORD_FOR_PYTHON"), 
    decode_responses=True
)

@app.route('/')
def index():
    # Increment the counter in Redis
    hits = r.incr('hits')
    
    # Vessel Data (The stuff you want to "pop")
    vessel_info = {
        "ship_name": "Surabaya Express",
        "status": "Active",
        "location": "Madura Strait",
        "destination": "Port of Tanjung Perak"
    }
    
    return render_template('index.html', vessel=vessel_info, count=hits)

# A route for that "Refresh" button
@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)