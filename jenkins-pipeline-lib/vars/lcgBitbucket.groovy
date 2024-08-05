/**
 * Bitbucket API
 *
 * Set Butbucket API build status
 *
 * Jenkins credentialsId = "BitBucketMBS"
 *
 * Using examples
 * def dataBitbucket = [userBitbucketApi: "BitBucketMBS"]
 *
 * Set as first step in pipeline:
 * lcgBitbucket.setBuildStatusInProgress(dataBitbucket)
 *
 * Set as post build actions
 *
 * post {
 *          success {
 *              script {
 *                  lcgtBitbucket.setBuildStatusSuccessful(dataBitbucket)
 *             }
 *          }
 *          aborted {
 *              script {
 *                  lcgtBitbucket.StatusStopped(dataBbucket)
 *             }
 *          }
 *          failure {
 *              script {
 *                  lcgtBitbucket.setBuildStatusFailed(dataBitbucket)
 *              }
 *          }
 * }
 */

def setBuildStatusInProgress(Map arguments) {
    arguments.buildState = "INPROGRESS"
    arguments.buildDescription = "Symphony: The build is in progress..."
    this.setBuildStatus(arguments)
}

def setBuildStatusSuccessful(Map arguments) {
    arguments.buildState = "SUCCESSFUL"
    arguments.buildDescription = "Symphony: ${currentBuild.description}"
    this.setBuildStatus(arguments)
}

def setBuildStatusFailed(Map arguments) {
    arguments.buildState = "FAILED"
    arguments.buildDescription = "Symphony: ${currentBuild.description}"
    this.setBuildStatus(arguments)
}

def setBuildStatusStopped(Map arguments) {
    arguments.buildState = "STOPPED"
    arguments.buildDescription = "Symphony: ${currentBuild.description}"
    this.setBuildStatus(arguments)
}

def setBuildStatus(Map arguments) {

    def buildCommit = env.GIT_COMMIT
    def gitUrl = env.GIT_URL
    def jobName = env.JOB_NAME
    def buildUrl = env.RUN_DISPLAY_URL
    def buildState = arguments.buildState
    def buildDescription = arguments.buildDescription
    def userBitbucketApi = arguments.userBitbucketApi
    def buildRepository = arguments.buildRepository ?: gitUrl.split('/').last().replaceAll('.git', '')
    def bitbucketWorkspace = arguments.bitbucketWorkspace ?: gitUrl.split('/').first().split(':').last()
    def buildName = currentBuild.fullDisplayName
    def buildKey = lcgCommonFunctions.generateMD5(jobName + buildCommit)

    if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
        lcgCommonFunctions.prettyPrinter(arguments, "lcgBitbucket.setBuildStatus:")
    }

    println("Bitbucket API: Notifying commit build result")

    withCredentials([usernamePassword(credentialsId: userBitbucketApi,
            usernameVariable: 'BITBUCKET_USER', passwordVariable: 'BITBUCKET_PASS')]) {
        sh """
        curl --request POST --user \${BITBUCKET_USER}:\${BITBUCKET_PASS} \\
        --header "Content-Type: application/json" \\
        "https://api.bitbucket.org/2.0/repositories/${bitbucketWorkspace}/${buildRepository}/commit/${buildCommit}/statuses/build/" \\
        --data '
        {"key": "${buildKey}",
        "url": "${buildUrl}",
        "state": "${buildState}",
        "description": "${buildDescription}",
        "name": "${buildName}"
        }'
        """
    }
    println("Bitbucket API: Build result notified")
}
