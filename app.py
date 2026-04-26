from flask import Flask, render_template, redirect, url_for
import redis
import os

app = Flask(__name__)

# Standard connection to Redis
r = redis.Redis(
    host='vessel-db', 
    port=6379, 
    password=os.getenv("DB_PASSWORD_FOR_PYTHON"), 
    decode_responses=True
)

@app.route('/')
def index():
    # Increment the counter
    hits = r.incr('hits')
    
    vessel_data = {
        "ship_name": "Surabaya Express",
        "status": "Active",
        "location": "Madura Strait"
    }
    
    return render_template('index.html', vessel=vessel_data, count=hits)

@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Keeping it simple and lightweight
    app.run(host='0.0.0.0', port=5000)