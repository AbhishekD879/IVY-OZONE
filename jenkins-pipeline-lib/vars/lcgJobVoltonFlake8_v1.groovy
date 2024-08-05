def call(Map param) {

    def verbosity = (param.verbosity == null) ? 1 : (param.verbosity).count("v")
    env.VERBOSITY = verbosity

    def agentLabel = param["agentLabel"]
    def entityService = param["entityService"]
    def logNumToKeep = (param.logNumToKeep ?: 20).toString()
    def nexusCredentialsId = entityService.nexusCredentialsId

    def targetBranch = ""
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(entityService)

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sources"] = "./voltron/"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.coverage.exclusions"] = "**/**"

    // Set specific variables for PR and/or multibranch
    if (env.CHANGE_TARGET) {
        // PR
        println "CHANGE_TARGET exists"
        targetBranch = CHANGE_TARGET
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.branch"] = CHANGE_BRANCH
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.key"] = CHANGE_ID
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.base"] = CHANGE_TARGET
    } else {
        // Multibranch
        println "CHANGE_TARGET does not exists"
        targetBranch = BRANCH_NAME
        commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = BRANCH_NAME
    }

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Switch Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true
    println "Check Quality Gate: ${switchQualityGate}"

    pipeline {
        agent {
            node {
                label agentLabel
            }
        }
        options {
            skipDefaultCheckout false
            checkoutToSubdirectory(relativeTargetDir)
            timestamps()
            disableConcurrentBuilds()
            buildDiscarder(logRotator(numToKeepStr: logNumToKeep))
        }
        environment {
            VERBOSITY = "${verbosity}"
        }
        stages {
            stage("List env vars") {
                steps {
                    script {
                        sh "printenv"
                    }
                }
            }
            stage("Start Docker Test Container") {
                steps {
                    script {
                        lcgAwsEcrLogin()
                        withCredentials([usernamePassword(credentialsId: nexusCredentialsId,
                                usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                            containerBuild = lcgAgentDockerRun(entityService)
                            lcgAgentDockerBootstrap(containerBuild)
                        }
                    }
                }
            }
            stage("Install packages") {
                steps {
                    script {
                        lcgAgentDockerExecService(entityService, containerBuild, """virtualenv -p python3 venv &&
                                            . venv/bin/activate && 
                                            pip3 install -r requirements.txt &&
                                            pip freeze 
                                            """)
                    }
                }
            }
            stage("Run Tests") {
                parallel {
                    stage("Run Flake8") {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, """. venv/bin/activate &&
                                git branch -a &&
                                flake8 \\\$(git diff-index --name-only remotes/upstream/${targetBranch} | grep .py || echo none.py) --statistics
                                """)
                            }
                        }
                    }
                    stage("Run pytest collect regression Coral") {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, ". venv/bin/activate && py.test --collect-only tests/ --hostname sports.coral.co.uk")
                            }
                        }
                    }
                    stage("Run pytest collect regression Ladbrokes") {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, ". venv/bin/activate && py.test --collect-only tests/ --hostname sports.ladbrokes.com")
                            }
                        }
                    }
                    stage("Run pytest collect sanity Coral") {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, ". venv/bin/activate && py.test --collect-only tests_sanity/ --hostname sports.coral.co.uk")
                            }
                        }
                    }
                    stage("Run pytest collect sanity Ladbrokes") {
                        steps {
                            script {
                                lcgAgentDockerExecService(entityService, containerBuild, ". venv/bin/activate && py.test --collect-only tests_sanity/ --hostname sports.ladbrokes.com")
                            }
                        }
                    }
                    stage("Code Analysis") {
                        when { expression { return switchQualityGate } }
                        steps {
                            script {
                                lcgCodeQuality.sonarCloudPull(commonSonarGate)
                                sh "cat report-task.txt"
                            }
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
                }
            }
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
