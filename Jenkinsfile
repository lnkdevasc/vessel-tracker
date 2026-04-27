pipeline {
    agent any

    stages {
        stage('Step 1: Build') {
            steps {
                echo 'Building the Docker Image from our Dockerfile...'
                // This command tells Docker to follow the "recipe" we wrote
                sh 'docker build -t vessel-tracker:v1 .'
            }
        }

        stage('Step 2: Security Scan') {
            steps {
                echo 'Scanning the image for vulnerabilities...'
                // This runs Trivy against the image we just built
                // --exit-code 1 means "Fail the build if you find a HIGH or CRITICAL vulnerability"
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL vessel-tracker:v1'
            }
        }

        stage('Step 3: Deploy') {
            environment {
                // This pulls the secret from Jenkins' encrypted database
                DB_PASS_FOR_BUILD = credentials('REDIS_PWD') 
            }
            steps {
                echo 'Launching the Port Infrastructure...'
                // -f specifies the file, up -d starts everything in background
                // --build ensures it uses our freshly built image from Step 2
                sh 'docker-compose down || true'
                sh 'DB_PASS=${DB_PASS_FOR_BUILD} docker-compose up -d --build'
            }
        }
    }
}