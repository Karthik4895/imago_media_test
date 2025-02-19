pipeline {
    agent any
    triggers {
        githubPush()  // This triggers the pipeline when changes are pushed
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Karthik4895/imago_media_test.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t imago_media_test .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh 'docker tag imago_media_test karthik4895/imago_media_test:latest'
                    sh 'docker push karthik4895/imago_media_test:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
            }
        }
    }
}
