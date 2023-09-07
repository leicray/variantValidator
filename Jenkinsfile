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
            }
        }
        stage("Build and Run VVTA PostgreSQL") {
            steps {
                script {
                    def dockerfile = './db_dockerfiles/vvta/Dockerfile'
                    def vvtaContainer = docker.build("postgres-vvta-${CONTAINER_SUFFIX}", "-f ${dockerfile} ./db_dockerfiles/vvta")
                    vvtaContainer.run("-p 5432:5432 -d")
                    sh 'echo Building and running VVTA PostgreSQL'
                }
            }
        }
        stage("Build and Run Validator MySQL") {
            steps {
                script {
                    def dockerfile = './db_dockerfiles/vdb/Dockerfile'
                    def validatorContainer = docker.build("mysql-validator-${CONTAINER_SUFFIX}", "-f ${dockerfile} ./db_dockerfiles/vdb")
                    validatorContainer.run("-p 3306:3306 -d")
                    sh 'echo Building and running Validator MySQL'
                }
            }
        }
        stage("Build and Run SeqRepo") {
            steps {
                script {
                    def dockerfile = './db_dockerfiles/vvsr/Dockerfile'
                    def seqRepoContainer = docker.build("sqlite-seqrepo-${CONTAINER_SUFFIX}", "-f ${dockerfile} ./db_dockerfiles/vvsr")
                    seqRepoContainer.run()
                    sh 'echo Building and running SeqRepo'
                }
            }
        }
        stage("Build and Run VariantValidator") {
            steps {
                script {
                    def dockerfile = './Dockerfile'
                    def variantValidatorContainer = docker.build("variantvalidator-${CONTAINER_SUFFIX}", "-f ${dockerfile} .")
                    variantValidatorContainer.run("-d")
                    sh 'echo Building and running VariantValidator'
                }
            }
        }
        stage("Run Pytest and Codecov") {
            steps {
                // Run pytest and codecov in the variantvalidator container
                sh 'docker ps'
                sh 'docker exec variantvalidator-${CONTAINER_SUFFIX} pytest --cov-report=term --cov=VariantValidator/'
                sh 'docker exec variantvalidator-${CONTAINER_SUFFIX} codecov'
            }
        }
        stage("Cleanup Docker") {
            steps {
                sh 'docker stop postgres-vvta-${CONTAINER_SUFFIX}'
                sh 'docker rm postgres-vvta-${CONTAINER_SUFFIX}'
                sh 'docker stop mysql-validator-${CONTAINER_SUFFIX}'
                sh 'docker rm mysql-validator-${CONTAINER_SUFFIX}'
                sh 'docker stop sqlite-seqrepo-${CONTAINER_SUFFIX}'
                sh 'docker rm sqlite-seqrepo-${CONTAINER_SUFFIX}'
                sh 'docker stop variantvalidator-${CONTAINER_SUFFIX}'
                sh 'docker rm variantvalidator-${CONTAINER_SUFFIX}'
            }
        }
    }
}
