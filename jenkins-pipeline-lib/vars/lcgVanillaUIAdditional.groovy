/*
*   Addinitional Vanilla functions
*/

def startNetContainer(Map jobParams, List targetEnvs) {

    def steps = targetEnvs.collectEntries {
        [("${it.envName}"): netContainerTransformIntoStep(jobParams, it)]
    }
    parallel(steps)
}

def netContainerTransformIntoStep(Map jobParams, Map targetEnv) {

    def jobName = jobParams.jobName ?: "IIS-UI-DEV0-FRAMEWORK-Deployment"
    def commitAnsibleInventories = jobParams.commitAnsibleInventories
    def commitOxygenPlaybook = jobParams.commitOxygenPlaybook
    def containerTag = jobParams.containerTag
    def urlWebServerDev = targetEnv.urlWebServerDev
    def iisPort = targetEnv.iisPort
    def iisPortHealthcheck = targetEnv.iisPortHealthcheck ?: ""
    def testingTimeout = targetEnv.testingTimeout ?: 1800

    return {

        timeout(time: testingTimeout, unit: 'SECONDS') {
            build job: jobName,
                    parameters: [
                            string(name: "Commit_ansible_inventories", value: commitAnsibleInventories),
                            string(name: "Commit_oxygen_playbook", value: commitOxygenPlaybook),
                            string(name: "Container_tag", value: containerTag),
                            string(name: "env_Name", value: urlWebServerDev),
                            string(name: "env_Port", value: iisPort),
                            string(name: "env_Port_Health", value: iisPortHealthcheck)
                    ]
        }
    }
}
