pipeline {
    agent {
        docker {
            image "docker"
        }
    }
    environment {
        CODECOV_TOKEN = "50dd5c2e-4259-4cfa-97a7-b4429e0d179e"
        CONTAINER_SUFFIX = "${BUILD_NUMBER}"
    }
    stages {
        stage("Clone Repository") {
            steps {
                checkout scm
                sh 'chmod a+r ./*'
            }
        }
        stage("Where am I") {
            steps {
                sh 'echo $HOME'
                sh 'pwd'
                sh 'ls -l'
            }
        }
        stage("Build VVTA PostgreSQL") {
            steps {
                script {
                    def postgresImage = docker.build("postgres-vvta-${CONTAINER_SUFFIX}", "./db_dockerfiles/vvta/Dockerfile")
                    sh "docker run --name postgres-vvta-${CONTAINER_SUFFIX} -p 5432:5432 -d postgres-vvta-${CONTAINER_SUFFIX}"
                }
            }
        }
        stage("Build Validator MySQL") {
            steps {
                script {
                    def mysqlImage = docker.build("mysql-validator-${CONTAINER_SUFFIX}", "./db_dockerfiles/vdb/Dockerfile")
                    sh "docker run --name mysql-validator-${CONTAINER_SUFFIX} -p 3306:3306 -d mysql-validator-${CONTAINER_SUFFIX}"
                }
            }
        }
        stage("Build SeqRepo") {
            steps {
                script {
                    def seqrepoImage = docker.build("sqlite-seqrepo-${CONTAINER_SUFFIX}", "./db_dockerfiles/vvsr/Dockerfile")
                }
            }
        }
        stage("Build VariantValidator") {
            steps {
                script {
                    def variantvalidatorImage = docker.build("variantvalidator-${CONTAINER_SUFFIX}", "./Dockerfile")
                    sh "docker run --name variantvalidator-${CONTAINER_SUFFIX} -p 5432:5432 -p 3306:3306 -d variantvalidator-${CONTAINER_SUFFIX}"
                }
            }
        }
        stage("Run Pytest and Codecov") {
            steps {
                // Run pytest and codecov in the variantvalidator container
                sh 'docker ps'
                // sh 'docker exec variantvalidator-${CONTAINER_SUFFIX} pytest --cov-report=term --cov=VariantValidator/'
                // sh 'docker exec variantvalidator-${CONTAINER_SUFFIX} codecov'
            }
        }
        stage("Cleanup Docker") {
            steps {
                sh 'docker stop postgres-vvta-${CONTAINER_SUFFIX}'
                sh 'docker rm postgres-vvta-${CONTAINER_SUFFIX}'
                sh 'docker stop mysql-validator-${CONTAINER_SUFFIX}'
                sh 'docker rm mysql-validator-${CONTAINER_SUFFIX}'
                sh 'docker rmi postgres-vvta-${CONTAINER_SUFFIX}'
                sh 'docker rmi mysql-validator-${CONTAINER_SUFFIX}'
                sh 'docker stop variantvalidator-${CONTAINER_SUFFIX}'
                sh 'docker rm variantvalidator-${CONTAINER_SUFFIX}'
                sh 'docker rmi variantvalidator-${CONTAINER_SUFFIX}'
            }
        }
    }
}
