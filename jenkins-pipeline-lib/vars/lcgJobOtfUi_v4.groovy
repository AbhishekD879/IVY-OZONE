def call(Map param) {

    def agentLabel    = param["agentLabel"]
    def entityService = param["entityService"]
    def entityDeploy  = param["entityDeploy"]

    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(entityService)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(entityService))) : ""
    def relativeTargetDir   = lcgCommonFunctions.getGitTargetDirectory(entityService)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(entityService)
    def cloudFlareApiTokenId = param.cloudFlareApiTokenId ?: lcgCommonFunctions.getCloudFlareApiTokenId(entityService, "cloudFlareApiTokenId")


    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"]  = "./" + relativeTargetDir
    commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"]     = branchName

    // Switch Quality Gate
    def switchQualityGate = true
    if (params.containsKey("quality_gate")) {
        if (!params.quality_gate) {
            switchQualityGate = false
        }
    }
    println "Check Quality Gate: " +  switchQualityGate

    // Add service info into target deploy environments
    lcgDeployAws.prepareEnvsList(entityDeploy, entityService)

    /*
     *  Add other common repositories need to deploy and build
     *  NEEDS: add autodetect deploiyng to Akamai then add oxygen_playbook and ansible_inventories repositories
    */
    def appBuild                      = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild     = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def repositoriesList              = [entityService, appBuild]

    lcgCommonFunctions.prettyPrinter(entityService, "entityService")
    pipeline {
        agent {
            node {
                label agentLabel
            }
        }
        options {
            skipDefaultCheckout true
            timestamps()
            disableConcurrentBuilds()
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
            stage ("Start Docker Build Container") {
                steps {
                    script {
                        lcgAwsEcrLogin()
                        containerBuild = lcgAgentDockerRun(entityService)
                        lcgAgentDockerBootstrap(containerBuild)
                    }
                }
            }
            stage ("Pre build tasks") {
                steps {
                    script {
                        sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/"
                        lcgCommonFunctions.setNexusServerProperties(entityService)
                    }
                }
            }
            stage ("NPM install") {
                steps {
                    script {
                        lcgAgentDockerExecService(entityService, containerBuild, "make npm_install_local")
                    }
                }
            }
            stage ("Code Analysis") {
                when { expression { return switchQualityGate}}
                steps {
                    script {
                        lcgCodeQuality.sonarCloudPull(commonSonarGate)
                    }
                }
            }
            stage ("Test and Build") {
                parallel {
                    /*
                    stage ("Run Lint") {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, "make lint")
                            }
                        }
                    }
                    */
                    stage('NPM Build') {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, "ENV_PROFILE=${env_profile} make build_app")
                            }
                        }
                    }
                }
            }
            stage ("Deploy") {
                steps {
                    script {
                        lcgDeploy.deploy(entityDeploy)
                    }
                }
            }
            stage ("Post deploy") {
                steps {
                    script {
                        withCredentials([string(credentialsId: cloudFlareApiTokenId, variable: 'API_TOKEN')]) {
                            lcgDeploy.post(entityDeploy)
                        }
                    }
                }
            }
        }
        post {
            always {
                script {
                    if (binding.hasVariable('containerBuild')) {
                        lcgAgentDockerRm(containerBuild)
                    }
                    sh "rm -fr ${relativeTargetDir}_*"
                }
            }
            aborted {
                    script {
                        lcgNotify.notifyAborted(["blueOcean": true])
                    }
            }
            failure {
                    script {
                        lcgNotify.notifyFailed(["blueOcean": true])
                    }
            }
        }
    }
}
