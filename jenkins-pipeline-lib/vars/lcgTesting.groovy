/*
*   Main testing functions
*/

def bma(List targetEnvs) {

    def steps = targetEnvs.collectEntries {
        [("${it.envName}"): bmaTransformIntoStep(it)]
    }
    parallel(steps)
}

def bmaTransformIntoStep(Map targetEnv) {

    def uiTestingJob = targetEnv.uiTestingJob
    def ref_voltron = targetEnv.ref_voltron
    def ref_jenkinsfile = targetEnv.ref_jenkinsfile
    def env_test_path = targetEnv.env_test_path
    def custom_marks = targetEnv.custom_marks
    def back_end = targetEnv.back_end
    def rootWebServerDir = targetEnv.rootWebServerDir
    def testingTimeout = targetEnv.testingTimeout ?: 600

    return {

        timeout(time: testingTimeout, unit: 'SECONDS') {
            build job: uiTestingJob,
                    parameters: [
                            string(name: "ref_voltron", value: ref_voltron),
                            string(name: "ref_jenkinsfile", value: ref_jenkinsfile),
                            string(name: "env_test_path", value: env_test_path),
                            string(name: "custom_marks", value: custom_marks),
                            string(name: "back_end", value: back_end),
                            string(name: "target_host", value: rootWebServerDir)
                    ]
        }
    }
}
