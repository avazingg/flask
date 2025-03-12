pipeline {
    agent any

    environment {
        ALLURE_RESULTS_DIR = 'allure-results'
    }

    stages {
        stage('Build and Start Services') {
            steps {
                script {
                    MY_APP_DIR='/var/lib/docker/volumes/jenkins-data-flask/_data/workspace/$JOB_NAME'
                    // Собираем и поднимаем web и db сервисы в фоне
                    sh 'MY_APP_DIR docker compose up --build web db -d'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Запускаем тесты. Сервис "test" описан в docker-compose.yml
                    sh'mkdir -p $ALLURE_RESULTS_DIR'
                    sh "MY_APP_DIR docker compose run --rm  -e TEST_PATH=tests/ -e TEST_ARGS='--alluredir=$ALLURE_RESULTS_DIR' test"
                }
            }
        }
    }

    post {
        always {
            script {
                def resultsExist = sh(returnStatus: true, script: '''
                [ -d $ALLURE_RESULTS_DIR ] && [ "$(ls -A $ALLURE_RESULTS_DIR)" ]
                ''') == 0

                if (resultsExist) {
                    echo 'Allure results found. Generating report...'
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: '$ALLURE_RESULTS_DIR']]
                    ])
                } else {
                    echo 'No Allure results found. Tests might not have run.'
                }
            }
        }
        cleanup {
            echo 'Cleaning up...'
            sh '''
            docker compose down
            rm -rf allure.zip $ALLURE_RESULTS_DIR
            '''
            deleteDir()
        }
    }
}
