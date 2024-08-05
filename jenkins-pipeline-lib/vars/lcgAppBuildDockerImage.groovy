def call(String serviceName) {

    lcgAwsEcrLogin()

    stage ("Docker pull") {
        sh "cd ./scripts/${serviceName}/ && make pull"
    }
    /*
    stage ("Build artifact") {
        sh "cd ./scripts/${serviceName}/ && make build_artifact"
    }
    stage ("Build application") {
        sh "cd ./scripts/${serviceName}/ && make build_application"
    }
    stage ("Push application") {
        sh "cd ./scripts/${serviceName}/ && make push"
    }
    */
}
