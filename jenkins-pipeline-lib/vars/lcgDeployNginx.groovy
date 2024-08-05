/*
*  Deploying by rsync direct host
*
 */
def directRsync(Map parameters) {

    println "lcgDeployNginx.directRsync: Env config to deploy: ${parameters}"

    def brand = parameters.brand
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]

    def hostWebServerDev = parameters.hostWebServerDev
    def userWebServerDev = parameters.userWebServerDev ?: ""
    def pathWebServerDev = parameters.pathWebServerDev
    def urlWebServerDev = parameters.urlWebServerDev
    def deploymentKey = parameters.deploymentKey ?: ""
    def relativeSourceDir = parameters.relativeSourceDir ?: ""
    def verbose = parameters.verbose ?: "v"
    def rsyncInlineParams = parameters.rsyncInlineParams ?: "--delete"
    def webServerDev = [userWebServerDev, hostWebServerDev].findAll{ it.length() > 0 }.join("@")

    if (deploymentKey) {
        sshagent(credentials: [deploymentKey]) {
            sh "rsync -a${verbose}h ${rsyncInlineParams} ${relativeSourceDir}/${sourceDir}/* ${webServerDev}:${pathWebServerDev}/${urlWebServerDev}/"
        }
    } else {
        sh "rsync -a${verbose}h ${rsyncInlineParams} ${relativeSourceDir}/${sourceDir}/* ${webServerDev}:${pathWebServerDev}/${urlWebServerDev}/"
    }

}

def directRsyncParallel(Map parameters) {

    println "lcgDeployNginx.directRsyncParallel: Env config to deploy: ${parameters}"

    def brand = parameters.brand
    def envName = parameters.envName
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]

    def hostWebServerDev = parameters.hostWebServerDev
    def userWebServerDev = parameters.userWebServerDev ?: ""
    def pathWebServerDev = parameters.pathWebServerDev
    def urlWebServerDev = parameters.urlWebServerDev
    def deploymentKey = parameters.deploymentKey
    def relativeSourceDir = parameters.relativeSourceDir
    def verbose = parameters.verbose ?: "v"
    def rsyncInlineParams = parameters.rsyncInlineParams ?: "--delete"
    def rsyncRetry = parameters.rsyncRetry ?: 10
    def rsyncSleep = parameters.rsyncSleep ?: 30
    def webServerDev = [userWebServerDev, hostWebServerDev].findAll{ it.length() > 0 }.join("@")

    def targetDir = relativeSourceDir + "/" + sourceDir + "/"
    def subfolders = sh(returnStdout: true, script: """
        find ${targetDir}* -maxdepth 0 -type d
        """
    ).trim()

    def rsyncDirs = subfolders.split('\n')
    println "lcgDeployNginx.directRsyncParallel Rsync list subfolders: ${rsyncDirs}"
    println "lcgDeployNginx.directRsyncParallel Rsync retry: ${rsyncRetry} sleep: ${rsyncSleep} seconds"

    def steps = rsyncDirs.collectEntries {
        [(brand.capitalize() + " " + envName + " " + it.split("/").last()): transformIntoStepRsyncParallel(it, deploymentKey, rsyncInlineParams,
                verbose, webServerDev, pathWebServerDev, urlWebServerDev,
                relativeSourceDir, sourceDir, rsyncRetry, rsyncSleep)]
    }
    parallel(steps)
}

def transformIntoStepRsyncParallel(inputString, deploymentKey, rsyncInlineParams,
                                   verbose, webServerDev, pathWebServerDev, urlWebServerDev,
                                   relativeSourceDir, sourceDir, rsyncRetry, rsyncSleep) {
    return {
        def targetPlatform = inputString.split("/").last()
        def retryDelay = false

        retry(rsyncRetry) {
            if (retryDelay) {
                sleep time: rsyncSleep, unit: 'SECONDS'
            } else {
                retryDelay = true
            }
            sshagent(credentials: [deploymentKey]) {
                sh "rsync -a${verbose}h ${rsyncInlineParams} ${relativeSourceDir}/${sourceDir}/${targetPlatform}/* ${webServerDev}:${pathWebServerDev}/${urlWebServerDev}/"
            }
        }
    }
}

/*
*  Deploying by rsync through jump Jenkins node
*
 */
def jumpNodeRsync(Map parameters) {

    println "lcgDeployNginx.jumpNodeRsync: Env config to deploy: ${parameters}"

    def brand = parameters.brand
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]

    def hostWebServerDev = parameters.hostWebServerDev
    def userWebServerDev = parameters.userWebServerDev ?: ""
    def pathWebServerDev = parameters.pathWebServerDev
    def urlWebServerDev = parameters.urlWebServerDev
    def deploymentKey = parameters.deploymentKey
    def relativeSourceDir = parameters.relativeSourceDir
    def verbose = parameters.verbose ?: "v"
    def rsyncInlineParams = parameters.rsyncInlineParams ?: "--delete"
    def jumpNodeLabel = parameters.jumpNodeLabel
    def webServerDev = [userWebServerDev, hostWebServerDev].findAll{ it.length() > 0 }.join("@")

    stash includes: "${relativeSourceDir}/${sourceDir}/**", name: "artifactDist"

    node(jumpNodeLabel) {
        stage("Deploy") {
            deleteDir()
            unstash name: "artifactDist"
            sshagent(credentials: [deploymentKey]) {
                sh "rsync -a${verbose}h ${rsyncInlineParams} ${relativeSourceDir}/${sourceDir}/* ${webServerDev}:${pathWebServerDev}/${urlWebServerDev}/"
            }
        }
    }
}


/*
*  Discovery host in AWS infrastructure and deploy by rsync
*
 */
def getHostIp(Map parameters) {

    def tag = parameters.tag ?: "nginx-ui"
    def hostEnvironment = parameters.hostEnvironment ?: "dev0"
    def ecosystem = parameters.ecosystem ?: "dev"
    def region = parameters.region ?: "eu-west-2"

    def hostWebServerDev = sh(returnStdout: true, script: """
        aws ec2 describe-instances --filters "Name=tag:sName,Values=${tag}"  "Name=tag:Environment,Values=${hostEnvironment}" \
        "Name=tag:Ecosystem,Values=${ecosystem}" --region ${region} --query 'Reservations[].Instances[].PrivateIpAddress' | \
        jq -r .[0]
    """
    ).trim()
    return hostWebServerDev
}

def directRsyncAwsDiscoveryHost(Map parameters) {

    def hostWebServerDev = this.getHostIp(parameters)
    parameters.hostWebServerDev = hostWebServerDev
    this.directRsync(parameters)
}

def directRsyncParallelAwsDiscoveryHost(Map parameters) {

    def hostWebServerDev = this.getHostIp(parameters)
    parameters.hostWebServerDev = hostWebServerDev
    this.directRsyncParallel(parameters)
}

