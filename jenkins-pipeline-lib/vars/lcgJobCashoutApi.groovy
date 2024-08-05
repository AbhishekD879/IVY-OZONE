#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    // Service to build
    def service = lcgCommonFunctions.getConstantsParameters("services.serviceCashoutApi")

    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    // def projectKeySonarCloud = lcgCommonFunctions.getServiceProjectKeySonarCloud(service)
    def sonarScannerDockerSkip = lcgCommonFunctions.getServiceSonarScannerDockerSkip(service)

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["switchSonarCloudPipelineFailed"] = switchSonarCloudPipelineFailed
    commonSonarGate["sonarScannerDockerSkip"] = sonarScannerDockerSkip
    // commonSonarGate["parametersSonarCloud"]["-Dsonar.projectKey"] = projectKeySonarCloud
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.java.binaries"] = "./build/classes"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sources"] = "."

    arguments.service = service
    arguments.commonSonarGate = commonSonarGate

    def deployJobs = { jobArguments ->

        def jobs = [:]
        def branchName = jobArguments.branchName
        def imageTag = jobArguments.imageTag
        def deploymentTimeout = jobArguments.deploymentTimeout

        return {

            if (branchName == "develop") {
                jobs.put("Deploy to Coral dev0", {
                    timeout(time: deploymentTimeout, unit: 'SECONDS') {
                        build job: "CASHOUT-DEV0-FRAMEWORK-Deployment",
                                parameters: [
                                        string(name: "Commit_oxygen_playbook", value: "master"),
                                        string(name: "Commit_ansible_inventories", value: "master"),
                                        string(name: "Container_tag", value: imageTag),
                                ]
                    }
                } )

                jobs.put("Deploy to Ladbrokes dev0", {
                    timeout(time: deploymentTimeout, unit: 'SECONDS') {
                        build job: "CASHOUT-DEV0-LADBROKES-Deployment",
                                parameters: [
                                        string(name: "Commit_oxygen_playbook", value: "master"),
                                        string(name: "Commit_lad_ansible_inventories", value: "master"),
                                        string(name: "Container_tag", value: imageTag),
                                ]
                    }
                } )
            }

        parallel(jobs)
        }
    }

    lcgJobApiGeneric(arguments, deployJobs)
}
