def call(Map arguments) {

    def service = arguments.service
    def targetEnvs = arguments.targetEnvs ?: []
    def primaryAgentLabel = arguments.primaryAgentLabel
    def switchDeploy = (arguments.switchDeploy != null) ? arguments.switchDeploy : false
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
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

    // Add sourceDir and relativeTargetDir to targetEnv
    targetEnvs.each {
        it.sourceDir = "build/Web/ClientDist"
        it.relativeSourceDir = "${relativeTargetDir}"
    }

    // BMA branch
    def bmaBranch = params.ref_bma ?: "develop"
    println "BMA branch ${bmaBranch}"

    // Brand
    def brand = params.brand
    def brandCapitalize = brand.capitalize()
    println "Brand: ${brand}"

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
            // disableConcurrentBuilds()
        }
        stages {
            stage("Sanity workspace") {
                steps {
                    deleteDir()
                }
            }
            stage('Getting SCM sources') {
                steps {
                    script {
                        currentBuild.description = "Branch: ${branchName} Branch BMA: ${bmaBranch} Brand: ${brand}"
                        lcgScmGitParallel(repositoriesList, false)
                    }
                }
            }
            stage("Pull submodules") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            sh """
                            git submodule update --init
                            git submodule foreach git checkout ${bmaBranch}
                            git submodule foreach git pull
                            """
                        }
                    }
                }
            }
            stage("Start Docker Build Container") {
                steps {
                    script {
                        lcgAwsEcrLogin()
                        containerBuild = lcgAgentDockerRun(service)
                        lcgAgentDockerBootstrap(containerBuild)
                    }
                }
            }
            stage("NPM install") {
                steps {
                    script {
                        lcgCommonFunctions.setNexusServerProperties(service)
                        lcgAgentDockerExecService(service, containerBuild, "npm install --pure-lockfile")
                    }
                }
            }
            stage("Build") {
               parallel {
                   stage("Build Mobile") {
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "1")
                                lcgAgentDockerExecServiceClone(service, "1", containerBuild, "npm run build${brandCapitalize}MobileLocal --env.environment=${envProfile}")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "1", "/build/Web/ClientDist/${brand}Mobile/*", "/build/Web/ClientDist/${brand}Mobile")
                            }
                        }
                   }
                   stage("Build Desktop") {
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "2")
                                lcgAgentDockerExecServiceClone(service, "2", containerBuild, "npm run build${brandCapitalize}DesktopLocal --env.environment=${envProfile}")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "2", "/build/Web/ClientDist/${brand}Desktop/*", "/build/Web/ClientDist/${brand}Desktop")
                            }
                        }
                    }
               }
            }
            stage("Code Analysis") {
                when { expression { return switchQualityGate } }
                steps {
                    script {
                        lcgCodeQuality.sonarCloudPull(commonSonarGate)
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
            always {
                script {
                    if (binding.hasVariable('containerBuild')) {
                        lcgAgentDockerRm(containerBuild)
                    }
                }
            }
        }
    }
}
