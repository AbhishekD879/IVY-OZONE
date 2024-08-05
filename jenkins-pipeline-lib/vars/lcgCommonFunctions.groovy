import static groovy.json.JsonOutput.*
import java.security.MessageDigest;

/**
 * Get string job parameter for Git repository
 *
 * @param repository Git repository Map parameter
 * @return job string parameter name
 *
 * Example:
 * url = "git@bitbucket.org:symphonydevelopers/application-build.git"
 * result: ref_application_build
 */
def getJobGitRefParameter(Map repository) {
    String url = repository['url']
    String gitParam = 'ref_' + url.split('/').last().replace('-', '_').replaceAll('.git', '')
    return gitParam.trim()
}

/**
 * Get branch default for Git repository
 *
 * @param repository Git repository Map parameter
 * @return branch default
 */
def getGitDefaultBranch(Map repository) {
    String branchDefault = repository.branchDefault ?: repository.branch_default
    return branchDefault ? branchDefault.trim() : ""
}

/**
 * Get target directory for Git repository
 *
 * @param repository Git repository Map parameter
 * @return target directory
 */
def getGitTargetDirectory(Map repository) {

    def targetDirectory = repository.relativeTargetDir ?: ""
    return targetDirectory.trim()
}

/**
 * Get service dir in application build
 *
 * @param repository Git repository Map parameter
 * @return target directory
 */
def getServiceAppDir(Map repository) {

    def targetDirectory = repository.applicationBuildDir ?: ""
    return targetDirectory.trim()
}

/**
 * Get build image for service
 *
 * @param repository Git repository Map parameter
 * @return build image
 */
def getServiceBuildImage(Map repository) {
    String buildImage = repository.buildImage ?: repository.build_image
    return buildImage.trim()
}

/**
 * Get runtime image for service
 *
 * @param repository Git repository Map parameter
 * @return runtime image
 */
def getServiceRuntimeImage(Map repository) {
    String runtimeImage = repository.runtimeImage
    return runtimeImage.trim()
}

/**
 * Get Sonar Cloud Pipeline Failed key
 *
 * @param service Service Map parameter
 * @return switchSonarCloudPipelineFailed
 */
def getServiceSonarCloudPipelineFailed(Map service) {
    def switchSonarCloudPipelineFailed = service['switchSonarCloudPipelineFailed']
    return switchSonarCloudPipelineFailed
}

/**
 * Get Sonar Cloud Project Key
 *
 * @param service Service Map parameter
 * @return project key in Sonar Cloud
 */
def getServiceProjectKeySonarCloud(Map service) {
    def projectKeySonarCloud = service.projectKeySonarCloud
    return projectKeySonarCloud
}

/**
 * Get on/off Sonar Scanner in Docker
 *
 * @param service Service Map parameter
 * @return key to on/off Sonar Scanner in Docker
 */
def getServiceSonarScannerDockerSkip(Map service) {
    def sonarScannerDockerSkip = service.sonarScannerDockerSkip
    return sonarScannerDockerSkip
}

/**
 * Get on/off Sonar Scanner in Gradle project
 *
 * @param service Service Map parameter
 * @return key to on/off Sonar Scanner in Gradle project
 */
def getServiceSonarScannerGradleSkip(Map service) {
    def sonarScannerGradleSkip = service.sonarScannerGradleSkip
    return sonarScannerGradleSkip
}

/**
 * Get Service Docker Image tag max length
 *
 * @return tag max length
 */
def getServiceImageTagLength() {
    Integer serviceImageTagLength = this.getConstantsParameters("common.serviceImageTagLength")
    return serviceImageTagLength
}

/**
 * Get ECR
 *
 * @return ECR url
 */
def getDefaultEcr() {
    String defaultEcr = this.getConstantsParameters("common.defaultEcr")
    return defaultEcr
}

def getDefaultSonarToken() {
    String defaultSonarToken = this.getConstantsParameters("common.defaultSonarToken")
    return defaultSonarToken
}

def getDefaultForifyEndpoint() {
    String getDefaultForifyEndpoint = this.getConstantsParameters("common.fortify360ServerAddOn")
    return getDefaultForifyEndpoint
}

/**
 * Get Nexus server for service
 * @param service Map Service parameters
 * @return Map Nexus Server parameters
 */
def getServiceNexusServer(Map service) {
    String keyNexusServer = service["nexusServer"]
    Map nexusServer = this.getConstantsParameters("common.${keyNexusServer}")
    return nexusServer
}

/**
 * Get Nexus credendials Id for service
 * @param service Map Service parameters
 * @return Nexus Credentials Id
 */
def getServiceNexusCredentialsId(Map service) {
    def nexusCredentialsId = service["nexusCredentialsId"]
    return nexusCredentialsId
}

def getFastlaneCredId(Map service, String id) {
    def jenkinsCredId = service[id]
    return jenkinsCredId.trim()
}

def getFastlaneCommand(Map service, String command) {
    def fastlaneCommand = service[command]
    return fastlaneCommand.trim()
}

def getIosNativeGitUsernamePassword(Map service, String id) {
    def jenkinsCredId = service[id]
    return jenkinsCredId.trim()
}

def getCloudFlareApiTokenId(Map service, String id) {
    def cloudFlareCredId = service[id]
    return cloudFlareCredId.trim()
}

/**
 * Get auto deploy branches list
 * @param service Map Service parameters
 * @return branches list
 */
def getServiceAutoDeployBranchesList(Map service) {
    List autoDeployBranchesList = service.autoDeployBranchesList
    return autoDeployBranchesList
}

/**
 * Produce shell cd command
 *
 * @param dir Directory name
 * @return cd command or empty if var dir is empty
 */
def commandCdDir(String argDirName) {
    def dirName = argDirName.trim()
    if (dirName.length() > 0) {
        dirName = "cd " + dirName
        return dirName
    }
    return ""
}

/**
 * Wrapper that add changing working directory to sh command
 *
 * @param entityService Map service parameters
 * @param command sh command
 *
 * parameter -w does not work for agent docker therefore use wrapper
 *
 * https://github.com/jenkinsci/docker-workflow-plugin/pull/123
 * https://github.com/jenkinsci/docker-plugin/issues/561
 */

def commandShInDir(Map entityService, String command) {
    def fullCommand = this.commandShInDirMain(entityService, command)
    sh fullCommand
}

def commandShInDirMain(Map entityService, String command) {
    def cdCommand = this.commandCdDir(this.getGitTargetDirectory(entityService))
    def fullCommand = command
    if (cdCommand.length() > 0) {
        fullCommand = cdCommand + " && " + fullCommand
    }
    return fullCommand
}

/**
 * Wrapper add changing working directory and sudo to sh command
 *
 * @param entityService Map service parameters
 * @param command sh command
 *
 * parameter -w does not work for agent docker therefore use wrapper
 *
 * https://github.com/jenkinsci/docker-workflow-plugin/pull/123
 * https://github.com/jenkinsci/docker-plugin/issues/561
 */

def commandSudoShInDir(Map entityService, String command, String userName = "jenkins") {
    def envVars = this.getBuildEnvVars(entityService)
    def shCommand = this.commandSudoShInDirMain(entityService, command, userName)
    def fullCommand = ([envVars, shCommand]).join(" && ")
    sh fullCommand
}

def commandSudoShInDirDockerStyle(Map entityService, String command, String userName = "jenkins") {
    def fullCommand = this.commandSudoShInDirMain(entityService, command, userName)
    return fullCommand
}

def commandSudoShInDirMain(Map entityService, String command, String userName = "jenkins") {
    def cdCommand = this.commandCdDir(this.getGitTargetDirectory(entityService))
    def fullCommand = "sudo -E -H -u ${userName} sh -c \'${command}\'"

    if (cdCommand.length() > 0) {
        fullCommand = "${cdCommand} && ${fullCommand}"
        return fullCommand
    }
    return fullCommand
}

/**
 * Environments variables for building artifact
 *
 * @param entityService Map service parameters
 * @return String of export vars
 */

def getBuildEnvVars(Map entityService, prefix = "export", delimiter = "&&") {
    if (delimiter.trim().length() == 0) {
        delimiter = " "
    } else {
        delimiter = " " + delimiter.trim() + " "
    }
    def buildEnvVars = entityService["buildEnvVars"]
    def exportVarsCommand = {
        it.collect { prefix.trim() + " " + /$it.key=$it.value/ } join delimiter
    }
    return exportVarsCommand(buildEnvVars)
}

def getBuildEnvVarsDockerStyle(Map entityService) {
    def exportVarsCommand = this.getBuildEnvVars(entityService, "-e", " ")
    return exportVarsCommand
}

/**
 * Clone sources directory
 *
 * @param entityService Map service parameters
 * @param prefixCloneName String prefix for new directory
 */

def getCloneSourceDir(Map service, String prefixCloneName) {
    def targetDir = this.getGitTargetDirectory(service)
    def targetDirClone = targetDir + "_" + prefixCloneName
    return targetDirClone
}

def cpSourceDirToCloneDir(Map service, String prefixCloneName) {
    def targetDir = this.getGitTargetDirectory(service)
    def targetDirClone = this.getCloneSourceDir(service, prefixCloneName)
    sh "cp -r ${targetDir} ${targetDirClone}"
}

def mvCloneDirToSourceDir(service, prefixCloneName, sourceDir, destinationDir) {
    def targetDir = this.getGitTargetDirectory(service)
    def targetDirClone = this.getCloneSourceDir(service, prefixCloneName)
    sh "test -d ${targetDir}/${destinationDir} || mkdir -p ${targetDir}/${destinationDir}"
    sh "mv -vf ${targetDirClone}/${sourceDir} ${targetDir}/${destinationDir}"
}

/**
 * Get Git branch name
 *
 * @param entityService Map service parameters
 * @return String Git branch name
 */

def getGitBranchName(Map service) {
    def targetDir = this.getGitTargetDirectory(service)
    def branchName = sh(returnStdout: true, script: """
        cd ${targetDir}
        branch=\$(git branch | grep \\* | cut -d ' ' -f2)
        echo \${branch##*/}
    """
    ).trim()
    return branchName
}

/**
 * Get Git ID commit
 *
 * @param service Map service parameters
 * @return String Git ID commit
 */

def getGitIdCommit(Map service) {
    def targetDir = this.getGitTargetDirectory(service)
    def IdCommit = sh(returnStdout: true, script: """
        cd ${targetDir}
        branch=\$(git name-rev --name-only HEAD)
        ID_COMMIT=\$(git log -1 | grep ^commit | awk '{print \$2}' | cut -c -24)
        echo \${ID_COMMIT}
    """
    ).trim()
    return IdCommit
}

/**
 * Get parameters for Dev|Akamai environment
 *
 * @param envName String environment name
 * @return Map environment parameters
 */

// DEPRECATED
def getDeployDevEnvParameters(String envName, String brand = "coral") {

    def envDefault = [:]

    if (brand == "coral") {
        envDefault = (lcgCommonConstants("envDevDefault")).clone()
    }

    if (brand == "ladbrokes") {
        envDefault = (lcgCommonConstants("envDevLadbrokesDefault")).clone()
    }

    envDefault << lcgCommonConstants(envName)
    return envDefault
}

// DEPRECATED
def getDepoyAkamaiEnvParameters(String envName) {
    def envDefault = (lcgCommonConstants("envAkamaiDefault")).clone()
    envDefault << lcgCommonConstants(envName)
    return envDefault
}

/**
 * Get parameters from constants
 * @param key String Example: services.serviceBma, level1.level2.serviceTest
 * @return Map environment parameters
 */

def getConstantsParameters(String key) {
    def constants = lcgCommonConstants()
    def result = this.getConstantsParametersEngine(key, constants)

    if (this.getVerbosityLevel() >= 3) {
        this.prettyPrinter(result, "lcgCommonFunctions.getConstantsParameters: ${key}")
    }
    return result
}

def getConstantsParametersEngine(String key, Map constants) {

    def currentLevel = constants
    def keys = key.split("\\.")
    def keyDefault = "default"
    def result = [:]
    def targetKey = keys.last()
    def rootKey = keys.last()
    if (keys.length > 1) {
        rootKey = keys[-2]
    }

    try {
        keys.each {
            if (currentLevel.containsKey(it)) {
                currentLevel = currentLevel.get(it).clone()

                if (it == rootKey) {
                    // get default parameters if it exists
                    if (currentLevel.containsKey(keyDefault)) {
                        result << currentLevel.get(keyDefault)
                    }
                }

                // get target parameters
                if (it == targetKey) {
                    result << currentLevel
                }
            }
            else {
                throw new Exception("return from closure")
            }
        }
    }  catch (Exception e) {
        result = currentLevel.get(targetKey)
    }

    return result
}

/**
 * Set Nexus Server parameters
 * @param key Map service
 */
def setNexusServerProperties(Map service) {

    def relativeTargetDir = this.getGitTargetDirectory(service)
    def nexusServer = this.getServiceNexusServer(service)
    def registry = nexusServer.registry
    def alwaysAuth = nexusServer.always_auth
    def _auth = nexusServer._auth
    def strictSsl = nexusServer.strict_ssl ?: "false"

    sh """
cat <<EOF > ${relativeTargetDir}/.npmrc
registry=${registry}
always-auth=${alwaysAuth}
_auth=${_auth}
strict-ssl=${strictSsl}
EOF
    """
}

/**
 * Pretty printer data structure
 */

def prettyPrinter(argument, String title = "") {

    if (title != "") {
        println title
    }

    println prettyPrint(toJson(argument))
}

/**
 * Get verbosity level based on environment variable
 */

def getVerbosityLevel() {
    int verbosity = env.VERBOSITY == null ? 1 : (env.VERBOSITY).toInteger()
    return verbosity
}

/**
 * Getting recipients list
 *
 */

def getEmailRecipientsList(Map targetEnv) {

    def emailRecipientsListDefault = this.getConstantsParameters("common.notificationsList")
    def recipientsList = (this.getUniqueListByKey(emailRecipientsListDefault.email, targetEnv.envLevel,
            "envLevel", "recipientsList")).join(",")
    return recipientsList
}

/**
 * Getting target environment for deploiyng
 *
 */

def getTargetEnvs(List branchesDepoyEnvs, List targetEnvs, String branchName) {

    def targetEnvsList = this.getUniqueListByKey(branchesDepoyEnvs, branchName, "branches",
            "targetEnvsList")

    targetEnvsList.each {
        targetEnvs.addAll(this.getConstantsParameters(it))
    }
    if (getVerbosityLevel() >= 3) {
        this.prettyPrinter(targetEnvsList, "lcgCommonFunctions.getTargetEnvs: targetEnvsList")
        this.prettyPrinter(targetEnvs, "lcgCommonFunctions.getTargetEnvs: targetEnvs")
    }
    def returnCode = targetEnvs.size() > 0 ? true : false
    return returnCode
}

def getUniqueListByKey(List sourcesList, String searchString, String sourceKey, String targetKey) {

    def targetList = []

    sourcesList.each {
        if (searchString in it[sourceKey]) {
            targetList.addAll(it[targetKey])
        }
    }
    targetList.unique()
    return targetList
}

/**
 * Clean string
 */

def cleanString(String argument) {

    if (argument != null) {
        // https://stackoverflow.com/questions/42960282/how-to-remove-u200b-zero-length-whitespace-unicode-character-from-string-in-j
        argument = argument.replaceAll("[\\p{Cf}]", "").trim()
    }
    return argument
}

/**
 * Generate MD5 for groovy older then 2.5
 */

def generateMD5(String originalString) {
    MessageDigest digest = MessageDigest.getInstance("MD5") ;
    digest.update(originalString.bytes);
    md5String = new BigInteger(1, digest.digest()).toString(16).padLeft(32, '0');
    return md5String
}

/**
 * Transform list to map
 *
 * stepsPerStage = 3
 * inputList = [1,2,3,4,5,6,8,9,10]
 * resultMap = [1:[1,2,3], 2:[4,5,6], 3:[7,8,9], 4:[10]
 */

def splitListPerStages(List elements, Integer stepsPerStage) {
    def elementsSize = elements.size()
    Integer stageCount = elementsSize / stepsPerStage
    if (elementsSize % stepsPerStage > 0 ) { stageCount++ }
    println("stageCount: $stageCount")

    if (stageCount < 1) { return [] }

    def splitMap = (0..(stageCount - 1)).collectEntries {
        def firstElement = it*stepsPerStage
        def lastElement = it * stepsPerStage + stepsPerStage - 1
        if (lastElement >= elementsSize ) { lastElement = elementsSize - 1 }
        [ (it + 1): elements[firstElement..lastElement] ]
    }
    return splitMap
}
