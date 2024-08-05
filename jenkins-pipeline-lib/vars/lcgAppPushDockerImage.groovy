def call(String serviceName) {

    lcgAwsEcrLogin()

    //stage ("Push application") {
        //sh "cd ./scripts/${serviceName}/ && make push"
        sh "echo pushing App"
    //}

}
