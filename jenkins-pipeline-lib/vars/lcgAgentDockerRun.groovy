def call(Map parameters, String customImage = null) {

    def runtimeImage = (customImage == null) ? lcgCommonFunctions.getServiceBuildImage(parameters) : customImage
    def exportVarsCommand = lcgCommonFunctions.getBuildEnvVarsDockerStyle(parameters)
    def exportVarsFromFile = (parameters.buildEnvVarsFile == null) ? "" : "--env-file ${parameters.buildEnvVarsFile}"
    def entrypointParam = (parameters.overwrittenEntrypoint == null) ? "" : "--entrypoint ${parameters.overwrittenEntrypoint}"

    sh "docker pull ${runtimeImage}"

    def buildContainer = sh(returnStdout: true, script: """
        id=\$(id -u)
        userName=\$(whoami)
        image=${runtimeImage}
        workDir=\$(pwd)
        docker run -t -d ${exportVarsCommand} ${exportVarsFromFile} -v \${workDir}:/opt/workDir -w /opt/workDir ${entrypointParam} \${image} 
    """
    ).trim()

    return buildContainer
}
