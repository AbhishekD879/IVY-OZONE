def call(Map arguments) {

    def service = arguments.service
    def targetEnvs = arguments.targetEnvs ?: []
    def primaryAgentLabel = arguments.primaryAgentLabel
    def switchDeploy = (arguments.switchDeploy != null) ? arguments.switchDeploy : false
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))
    def relativeTargetDir = ""
    def repositoriesList = [service]

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectKey"] = "VANILLA"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectName"] = "VANILLA"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sources"] = "Frontend.Oxygen.Host/Client/coralsports/src/"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sourceEncoding"] = "UTF-8"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.language"] = "ts"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName

    // Brand
    def brand = params.brand
    def brandCapitalize = brand.capitalize()
    println "Brand: ${brand}"

    def sourceDir = "./"
    def relativeSourceDir = "./dist_${brand}"

    // Add sourceDir and relativeTargetDir to targetEnv
    targetEnvs.each {
        it.sourceDir = sourceDir
        it.relativeSourceDir = relativeSourceDir
    }

    // BMA branch
    def bmaBranch = params.ref_bma ?: "develop"
    println "BMA branch ${bmaBranch}"


    // Set env profile
    def envProfile = params.env_profile
    println "Env profile: ${envProfile}"

    // Switch Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true
    println "Check Quality Gate: ${switchQualityGate}"

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true
    println "Post clean up workspace: ${switchPostCleanUpWs}"

    println "Deploy: ${switchDeploy}"
    println "Target env: ${targetEnvs}"

    pipeline {
        agent {
            node {
                label primaryAgentLabel
            }
        }
        options {
            skipDefaultCheckout true
            timestamps()
            disableConcurrentBuilds()
        }
        stages {
            stage("Sanity workspace") {
                steps {
                    deleteDir()
                }
            }
            stage("Get and Unzip") {
                steps {
                    sh """
                        aws s3 cp s3://oxygen-coralsports-prod/bma/${ref_bma}.zip ./${ref_bma}.zip
                        unzip ./${ref_bma}.zip
                        mkdir ${relativeSourceDir}
                        mv ${brand}* ${relativeSourceDir}
                    """
                }
            }
            stage("Set profiles") {
                steps {
                    dir(relativeSourceDir) {
                        sh """
                            for DIR in \$(ls); do
                                cp \${DIR}/profile.${envProfile}.js \${DIR}/profile.js
                                PROFILE=\$(cat \${DIR}/profile.${envProfile}.js | sed -e 's/window.oxygenEnvConfig=//g' | jq -r .)
                                BUILDINFO=\$(cat \${DIR}/buildInfo.json  | jq ". += {\"environment\":\${PROFILE}}")
                                echo "\${BUILDINFO}" > \${DIR}/buildInfo.json
                            done
                        """
                    }
                }
            }
            stage("Deploy") {
                when { expression { return switchDeploy } }
                steps {
                    script {
                        lcgDeploy.deploy(targetEnvs)
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
