from flask import Flask
import redis

app = Flask(__name__)
# 'vessel-db' is the hostname defined in docker-compose
db = redis.Redis(host='vessel-db', port=6379)

@app.route("/")
def status():
    # Increment the visit count in Redis
    visits = db.incr('hits')
    return {
        "vessel": "Surabaya Express",
        "status": "Underway",
        "total_checks": int(visits)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=False)