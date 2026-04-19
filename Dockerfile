# Use the ultra-secure, small Alpine base
FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Install system dependencies needed for some Python packages
# (Alpine is so small it doesn't even come with 'gcc' or 'musl-dev' by default)
RUN apk add --no-cache gcc musl-dev linux-headers

# Create requirements
RUN echo "flask==3.0.0" > requirements.txt

# Install Python packages with progress bar off
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# Create the app.py with the single-threaded fix
RUN echo 'from flask import Flask\napp = Flask(__name__)\n@app.route("/")\ndef status(): return {"vessel": "Surabaya Express", "status": "Underway"}\nif __name__ == "__main__": app.run(host="0.0.0.0", port=5000, threaded=False)' > app.py

# Expose the port
EXPOSE 5000

# Run using the production-style command if you want, 
# but for now let's keep it simple to verify the scan
CMD ["python", "app.py"]