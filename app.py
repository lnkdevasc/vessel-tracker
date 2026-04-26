import os
from flask import Flask
import redis

app = Flask(__name__)

# We grab the "injected" password from the environment
db_pass = os.getenv("DB_PASSWORD_FOR_PYTHON")

# Now we connect using that password
db = redis.Redis(
    host='vessel-db', 
    port=6379, 
    password=db_pass, 
    decode_responses=True
)

@app.route("/")
def status():
    try:
        visits = db.incr('hits')
        return {
            "vessel": "Surabaya Express",
            "status": "Underway",
            "total_checks": int(visits)
        }
    except redis.exceptions.AuthenticationError:
        return {"error": "Unauthorized access to Logbook!"}, 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=False)