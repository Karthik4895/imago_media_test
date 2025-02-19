pipeline {
    agent any
    triggers{
        githubPush()
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Karthik4895/imago_media_test.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t imago_media .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh 'docker tag imago_media karthik4895/imago_media:latest'
                    sh 'docker push karthik4895/imago_media:latest'
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
