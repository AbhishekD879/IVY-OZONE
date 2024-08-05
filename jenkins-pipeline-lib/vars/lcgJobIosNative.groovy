#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    // Service to build
    def service = lcgCommonFunctions.getConstantsParameters("services.serviceIos")

    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def projectKeySonarCloud = lcgCommonFunctions.getServiceProjectKeySonarCloud(service)
    def sonarScannerDockerSkip = lcgCommonFunctions.getServiceSonarScannerDockerSkip(service)

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloudIos")
    commonSonarGate["sonarScannerDockerSkip"] = sonarScannerDockerSkip
    commonSonarGate["switchSonarCloudPipelineFailed"] = switchSonarCloudPipelineFailed
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectKey"] = projectKeySonarCloud

    arguments.service = service
    arguments.commonSonarGate = commonSonarGate

    lcgJobNativeGeneric(arguments)
}
