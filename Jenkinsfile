pipeline {
    agent any 

    stages {
        stage('Step 1: Cleanup') {
            steps {
                echo 'Removing old versions of the Vessel Tracker...'
                // This stops the app if it is already running so we can update it
                sh 'docker stop port-app || true'
                sh 'docker rm port-app || true'
            }
        }

        stage('Step 2: Build') {
            steps {
                echo 'Building the Docker Image from our Dockerfile...'
                // This command tells Docker to follow the "recipe" we wrote
                sh 'docker build -t vessel-tracker:v1 .'
            }
        }

        stage('Step 2.5: Security Scan') {
            steps {
                echo 'Scanning the image for vulnerabilities...'
                // This runs Trivy against the image we just built
                // --exit-code 1 means "Fail the build if you find a HIGH or CRITICAL vulnerability"
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL vessel-tracker:v1'
            }
        }

        stage('Step 3: Deploy (Fleet Mode)') {
            steps {
                echo 'Launching the Port Infrastructure...'
                // -f specifies the file, up -d starts everything in background
                // --build ensures it uses our freshly built image from Step 2
                sh 'docker-compose down' // Clean up old fleet first
                sh 'docker-compose up -d --build'
            }
        }
    }
}