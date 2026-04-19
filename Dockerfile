# 1. Use a lightweight Python base (Good for security)
FROM python:3.9-slim

# 2. Set the 'home' directory inside the container
WORKDIR /app

# 3. Create a requirements file directly inside the container
# (We are doing this to keep it simple for now)
RUN echo "flask==3.0.0" > requirements.txt

# 4. Install the library
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# 5. Create the app.py file directly inside the container
# (This ensures the container has the code it needs)
RUN echo 'from flask import Flask\napp = Flask(__name__)\n@app.route("/")\ndef status(): return {"vessel": "Ever Given", "status": "Docked"}\nif __name__ == "__main__": app.run(host="0.0.0.0", port=5000)' > app.py

# 6. Open port 5000
EXPOSE 5000

# 7. Start the app
CMD ["python", "app.py"]