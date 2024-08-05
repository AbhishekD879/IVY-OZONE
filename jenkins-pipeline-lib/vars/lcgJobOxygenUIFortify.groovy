def call(String agentLabel, Map service) {

    env.VERBOSITY = 3
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def repositoriesList = [service]

    // Fortify
    def switchFortifyScan = null
    if (params.containsKey("fortify_scan")) {
        switchFortifyScan = params.fortify_scan
    }
    println "Fortify Scan: ${switchFortifyScan}"

    // Switch on/off clean up workspace in post build action
    def switchPostCleanUpWs = true
    if (params.containsKey("clean_ws")) {
        if (!params.clean_ws) {
            switchPostCleanUpWs = false
        }
    }
    println "Post clean up workspace: " + switchPostCleanUpWs

    pipeline {
        agent {
            node {
                label agentLabel
            }
        }
        options {
            skipDefaultCheckout true
            timestamps()
        }
        stages {
            stage ("Sanity workspace") {
                steps {
                    deleteDir()
                }
            }
            stage ('Getting SCM sources') {
                steps {
                    script {
                        currentBuild.description = "Branch: ${branchName}"
                        lcgScmGitParallel(repositoriesList)
                    }
                }
            }
            stage ("Fortify simple scan") {
                when { expression { return switchFortifyScan == "fortify_simple_scan" } }
                steps {
                    script {
                        lcgAwsEcrLogin()
                        lcgCodeQualityFortify(lcgCommonFunctions.getConstantsParameters("common.fortify"), relativeTargetDir)
                    }
                }
            }
            stage ("Fortify upload reports ") {
                when { expression { return switchFortifyScan == "fortify_scan_upload_reports" } }
                steps {
                    script {
                        lcgAwsEcrLogin()
                        lcgCodeQualityFortify(lcgCommonFunctions.getConstantsParameters("common.fortify"), relativeTargetDir, "upload_reports")
                    }
                }
            }
        }
        post {
            cleanup {
                script {
                    if (switchPostCleanUpWs) {
                        cleanWs()
                    }
                }
            }
        }
    }
}
