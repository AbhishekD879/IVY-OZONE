/**
 * Check Akamai deploy
 *
 * @param deployEnv List deploy env
 * @param repList List reposities
 * @return boolean if Akamai deploy true else false
 */

def checkAkamaiDeploy(List deployEnvs, List repList) {

    def akamaiDeploy = false

    deployEnvs.each {
        if ((it["envTypeDeploy"]).contains("akamai")) {
            akamaiDeploy = true
            def ansiblePlaybooks = lcgCommonFunctions.getConstantsParameters(it["ansiblePlaybooks"])
            ansiblePlaybooks["branchName"] = params[lcgCommonFunctions.getJobGitRefParameter(ansiblePlaybooks)] ?: lcgCommonFunctions.getGitDefaultBranch(ansiblePlaybooks)
            def ansibleInventories = lcgCommonFunctions.getConstantsParameters(it["ansibleInventories"])
            ansibleInventories["branchName"] = params[lcgCommonFunctions.getJobGitRefParameter(ansibleInventories)] ?: lcgCommonFunctions.getGitDefaultBranch(ansibleInventories)
            def relativePlaybooksDir = lcgCommonFunctions.getGitTargetDirectory(ansiblePlaybooks)
            def relativeInventoriesDir = lcgCommonFunctions.getGitTargetDirectory(ansibleInventories)
            def additionalParameters = [relativePlaybooksDir: relativePlaybooksDir, relativeInventoriesDir: relativeInventoriesDir]
            repList.addAll([ansiblePlaybooks, ansibleInventories])
            it << additionalParameters
        }
    }
    return akamaiDeploy
}

/**
 * Akamai direct deploy (without Jump host) using rsync
 */
def directRsync(Map parameters) {

    println "lcgDeployAkamai.akamaiRsync: Env config to deploy: " + parameters

    def brand = parameters.brand ?: ""
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]
    def rsyncHost = parameters.rsyncHost
    def targetRoot = [parameters.codeAkamaiHost, parameters.pathAkamaiHost, parameters.rootWebServerDir].findAll { it.length() > 0 }.join("/")
    def relativeSourceDir = parameters.relativeSourceDir
    def rsyncFilter = (parameters.rsyncFilter == null) ? "" : "--filter=\\'${parameters.rsyncFilter}\\'"
    def rsyncVerbose = parameters.rsyncVerbose ?: "v"
    def rsyncParams = parameters.rsyncParams ?: "ah"

    // --filter is not working
    // Got error: Unknown filter rule: `'protect'
    // rsync -${rsyncParams}${rsyncVerbose} --delete ${rsyncFilter} ${relativeSourceDir}/${sourceDir}/* ${rsyncHost}:/${targetRoot}/

    sh """\
    rsync -${rsyncParams}${rsyncVerbose} --delete ${relativeSourceDir}/${sourceDir}/* ${rsyncHost}:/${targetRoot}/
    """
}

/**
 * Akamai purge cache
 */

def purgeCache(Map parameters) {

    def envLevel = parameters.envLevel
    def relativePlaybooksDir = parameters.relativePlaybooksDir
    def relativeInventoriesDir = parameters.relativeInventoriesDir
    def codeCP = parameters.codeCP
    def prePurgeCacheTimeout = parameters.prePurgeCacheTimeout ?: 0

    stage("Purge Akamai cache") {
        sh """\
        set -ex
        sleep ${prePurgeCacheTimeout}
        export PYTHONPATH=/usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages
        ansible-playbook -i ./${relativeInventoriesDir}/global/ -i ./${relativeInventoriesDir}/${envLevel}/ ./${relativePlaybooksDir}/akamai-purge.yml --extra-vars akamai_purge_cp_code='${codeCP}'
        """
    }
}

/**
 * Akamai direct deploy (without Jump host) in parallel using rsync
 *
 *  ../sources
 *      ./dist
 *      ./brand             [coral, ladbrokes]
 *          ./desktop       This level syncing to Akamai
 *          ./mobile
 *          ./....
 *
 */
def directRsyncParallel(Map parameters) {

    println "lcgDeployAkamai.directRsyncParallel: Env config to deploy: " + parameters

    def brand = parameters.brand ?: ""
    def envName = parameters.envName
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]
    def rsyncHost = parameters.rsyncHost
    def targetRoot = [parameters.codeAkamaiHost, parameters.pathAkamaiHost, parameters.rootWebServerDir].findAll { it.length() > 0 }.join("/")
    def relativeSourceDir = parameters.relativeSourceDir
    def rsyncFilter = (parameters.rsyncFilter == null) ? "" : "--filter=\\'${parameters.rsyncFilter}\\'"
    def rsyncVerbose = parameters.rsyncVerbose ?: "v"
    def rsyncParams = parameters.rsyncParams ?: "ah"
    def rsyncRetry = parameters.rsyncRetry ?: 10
    def rsyncSleep = parameters.rsyncSleep ?: 30

    def targetDir = relativeSourceDir + "/" + sourceDir + "/"
    def subfolders = sh(returnStdout: true, script: """
        find ${targetDir}* -maxdepth 0 -type d
        """
    ).trim()

    def rsyncDirs = subfolders.split('\n')
    println "lcgDeployAkamai.directRsyncParallel() Rsync list subfolders: ${rsyncDirs}"
    println "lcgDeployAkamai.directRsyncParallel() Rsync retry: ${rsyncRetry} sleep: ${rsyncSleep} seconds"

    def steps = rsyncDirs.collectEntries {
        // [(brand.capitalize() + " " + it.split("/").last()): transformIntoStep(it, rsyncParams, rsyncVerbose, rsyncHost, targetRoot, rsyncRetry, rsyncSleep)]
        [(envName.capitalize() + " " + it.split("/").last()): transformIntoStep(it, rsyncParams, rsyncVerbose, rsyncHost, targetRoot, rsyncRetry, rsyncSleep)]
    }
    parallel(steps)
}

def transformIntoStep(inputString, rsyncParams, rsyncVerbose, rsyncHost, targetRoot, rsyncRetry, rsyncSleep) {
    return {
        def targetPlatform = inputString.split("/").last()
        def retryDelay = false

        retry(rsyncRetry) {
            if (retryDelay) {
                sleep time: rsyncSleep, unit: 'SECONDS'
            } else {
                retryDelay = true
            }
            sh "rsync -${rsyncParams}${rsyncVerbose} --delete ${inputString}/* ${rsyncHost}:/${targetRoot}/${targetPlatform}/"
        }
    }
}

/**
 * Akamai direct deploy (without Jump host) using Aspera
 */
def directAspera(Map parameters) {

    def brand = parameters.brand ?: ""
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]
    def targetRoot = [parameters.codeAkamaiHost, parameters.pathAkamaiHost, parameters.rootWebServerDir].findAll { it.length() > 0 }.join("/")
    def relativeSourceDir = parameters.relativeSourceDir
    def rsyncHost = parameters.rsyncHost
    def rsyncRetry = parameters.rsyncRetry ?: 10
    def rsyncSleep = parameters.rsyncSleep ?: 30
    def asperaHost = parameters.asperaHost
    def asperaRetry = parameters.asperaRetry ?: 10
    def asperaSleep = parameters.asperaRetry ?: 30
    def asperaUser = parameters.asperaUser
    def asperaSshKey = parameters.asperaSshKey

    println "lcgDeployAkamai.directAspera(): Env config to deploy: ${parameters}"
    println "lcgDeployAkamai.directAspera(): Aspera host: ${asperaHost} retry: ${asperaRetry} sleep: ${asperaSleep} seconds"
    println "lcgDeployAkamai.directAspera(): Rsync host: ${rsyncHost} retry: ${rsyncRetry} sleep: ${rsyncSleep} seconds"

    def retryDelay = false

    retry(asperaRetry) {
        if (retryDelay) {
            sleep time: asperaSleep, unit: 'SECONDS'
        } else {
            retryDelay = true
        }
        sh """
        ascp -v -d -i ${asperaSshKey} --overwrite=always --mode=send --user=${asperaUser} --host=${asperaHost} ${relativeSourceDir}/${sourceDir}/* /${targetRoot}/
        """
    }

    retryDelay = false

    retry(rsyncRetry) {
        if (retryDelay) {
            sleep time: rsyncSleep, unit: 'SECONDS'
        } else {
            retryDelay = true
        }
        sh """
        rsync --recursive --delete --ignore-existing --existing --verbose ${relativeSourceDir}/${sourceDir}/ ${rsyncHost}:/${targetRoot}/
        """
    }

}

/**
 * Akamai direct deploy (without Jump host) in parallel using Aspera
 *
 *  ../sources
 *      ./dist
 *      ./brand             [coral, ladbrokes]
 *          ./desktop       This level syncing to Akamai
 *          ./mobile
 *          ./....
 *
 */
def directAsperaParallel(Map parameters) {

    def brand = parameters.brand ?: ""
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]
    def targetRoot = [parameters.codeAkamaiHost, parameters.pathAkamaiHost, parameters.rootWebServerDir].findAll { it.length() > 0 }.join("/")
    def relativeSourceDir = parameters.relativeSourceDir
    def rsyncHost = parameters.rsyncHost
    def rsyncRetry = parameters.rsyncRetry ?: 10
    def rsyncSleep = parameters.rsyncSleep ?: 30
    def asperaHost = parameters.asperaHost
    def asperaRetry = parameters.asperaRetry ?: 10
    def asperaSleep = parameters.asperaRetry ?: 30
    def asperaUser = parameters.asperaUser
    def asperaSshKey = parameters.asperaSshKey

    def targetDir = relativeSourceDir + "/" + sourceDir + "/"
    def subfolders = sh(returnStdout: true, script: """
        find ${targetDir}* -maxdepth 0 -type d
        """
    ).trim()

    def rsyncDirs = subfolders.split('\n')
    println "lcgDeployAkamai.directAsperaParallel(): Env config to deploy: ${parameters}"
    println "lcgDeployAkamai.directAsperaParallel(): Aspera list subfolders: ${rsyncDirs}"
    println "lcgDeployAkamai.directAsperaParallel(): Aspera host: ${asperaHost} retry: ${asperaRetry} sleep: ${asperaSleep} seconds"
    println "lcgDeployAkamai.directAsperaParallel(): Rsync host: ${rsyncHost} retry: ${rsyncRetry} sleep: ${rsyncSleep} seconds"

    def steps = rsyncDirs.collectEntries {
        [(brand.capitalize() + " " + it.split("/").last()): transformIntoStepDirectAsperaParallel(it, asperaHost, asperaRetry, asperaSleep, asperaUser, asperaSshKey, rsyncHost, rsyncRetry, rsyncSleep, targetRoot )]
    }
    parallel(steps)
}

def transformIntoStepDirectAsperaParallel(inputString, asperaHost, asperaRetry, asperaSleep, asperaUser, asperaSshKey, rsyncHost, rsyncRetry, rsyncSleep, targetRoot) {
    return {
        def destinationDir = inputString.split("/").last()

        def retryDelay = false

        retry(asperaRetry) {
            if (retryDelay) {
                sleep time: asperaSleep, unit: 'SECONDS'
            } else {
                retryDelay = true
            }
            sh """
            ascp -v -d -i ${asperaSshKey} --overwrite=always --mode=send --user=${asperaUser} --host=${asperaHost} ${inputString}/* /${targetRoot}/${destinationDir}/
            """
        }

        retryDelay = false

        retry(rsyncRetry) {
            if (retryDelay) {
                sleep time: rsyncSleep, unit: 'SECONDS'
            } else {
                retryDelay = true
            }
            sh """
            rsync --recursive --delete --ignore-existing --existing --verbose ${inputString}/ ${rsyncHost}:/${targetRoot}/${destinationDir}
            """
        }
    }
}

/**
 * Upload artifacts to S3 buckets
 *
 */

def uploadArtifact(Map parameters) {

    def brand = parameters.brand ?: ""
    def sourceDir = parameters.sourceDir ?: parameters["brands"][brand]["sourceDir"]
    def relativeSourceDir = parameters.relativeSourceDir
    def artifactS3Bucket = parameters.artifactS3Bucket
    def rootWebServerDir = parameters.rootWebServerDir

    sh """
    artifact_name=${brand}_\$(date +%F)_\$BUILD_NUMBER
    zip -r \${artifact_name}.zip ${relativeSourceDir}/${sourceDir}
    aws s3 cp \${artifact_name}.zip s3://${artifactS3Bucket}/${rootWebServerDir}/ --acl bucket-owner-full-control
    aws s3 cp s3://${artifactS3Bucket}/${rootWebServerDir}/\${artifact_name}.zip s3://${artifactS3Bucket}/${rootWebServerDir}/latest.zip --acl bucket-owner-full-control
    """
}
