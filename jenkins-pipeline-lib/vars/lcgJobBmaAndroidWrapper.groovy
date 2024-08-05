#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    def primaryAgentLabel = arguments.primaryAgentLabel ?: "dev-slave"
    def secondaryAgentLabel = arguments.secondaryAgentLabel ?: "lad-dev-slave"
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceBmaAndroidWrapper")
    def targetEnvs = arguments.targetEnvs ?: [lcgCommonFunctions.getConstantsParameters("s3Symphony.BmaAndroidWrapper")]
    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def logNumToKeep = (arguments.logNumToKeep ?: 20).toString()

    def typeJob = "notMultiBranch"
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def skipCheckout = true

    if (env.BRANCH_NAME) {
        branchName = BRANCH_NAME
        typeJob = "multiBranch"
        skipCheckout = false
    }
    if (env.CHANGE_TARGET) {
        branchName = env.GIT_COMMIT
        typeJob = "multiBranchPR"
        skipCheckout = false
    }
    service["branchName"] = branchName

    println "Branch name: ${branchName}"
    println "Type job: ${typeJob}"
    println "Skip default checkout: ${skipCheckout}"

    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["switchSonarCloudPipelineFailed"] = switchSonarCloudPipelineFailed
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir

    // Set specific variables for PR (pull request)
    if (typeJob == "multiBranchPR") {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.branch"] = CHANGE_BRANCH
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.key"] = CHANGE_ID
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.base"] = CHANGE_TARGET
    } else {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName
    }

    // Build brands list
    def brands = ["coral", "ladbrokes"]

    // Switch on/off Quality Gate
    def switchQualityGate = true
    if (params.containsKey("quality_gate")) {
        if (!params.quality_gate) {
            switchQualityGate = false
        }
    }
    println "Check Quality Gate: " + switchQualityGate

    // Switch on/off clean up workspace in post build action
    def switchPostCleanUpWs = true
    if (params.containsKey("clean_ws")) {
        if (!params.clean_ws) {
            switchPostCleanUpWs = false
        }
    }

    // Switch on/off deploy
    def switchDeploy = false
    if (params.containsKey("deploy")) {
        if (params.deploy) {
            switchDeploy = true
        }
    }
    // Deploy branches list
    def deployBranches = ["develop"]
    if (!(branchName in deployBranches && switchDeploy)) {
        switchDeploy = false
    }
    println "Deploy: ${switchDeploy} Branches: ${deployBranches}"

    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def repositoriesList = []

    if (typeJob  == "notMultiBranch") {
        repositoriesList = [service, appBuild]
    } else {
        repositoriesList = [appBuild]
    }
    println "Repositories list: " + repositoriesList

    pipeline {
        agent {
            node {
                label primaryAgentLabel
            }
        }
        triggers {
            bitbucketPush()
        }
        options {
            skipDefaultCheckout(skipCheckout)
            checkoutToSubdirectory(relativeTargetDir)
            timestamps()
            buildDiscarder(logRotator(numToKeepStr: logNumToKeep))
        }
        parameters {
            booleanParam(name: 'clean_ws', defaultValue: true, description: 'Clean up workspace in post build action')
        }
        stages {
            stage("Abort older running build") {
                when { expression { return typeJob in ["multiBranch", "multiBranchPR"] } }
                steps {
                    script {
                        lcgCommonHudsonFunctions.abortPreviousBuilds()
                    }
                }
            }
            stage("Sanity workspace") {
                when { expression { return typeJob == "notMultiBranch" } }
                steps {
                    deleteDir()
                }
            }
            stage('Getting SCM sources') {
                steps {
                    script {
                        sh "ls -la"
                        sh "pwd"
                        currentBuild.description = "Branch: ${branchName}, Brand: ${brands.join(', ')}"
                        lcgScmGitParallel(repositoriesList, false)
                        sh "ls -la"
                    }
                }
            }
            stage("Pre build tasks") {
                steps {
                    script {
                        sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/"
                    }
                }
            }
            stage("Prepare sources") {
                steps {
                    script {
                        stash includes: "${relativeTargetDir}/**", name: "artifactSources"
                        sh "ls -la sources"
                    }
                }
            }
            stage("Test and Build") {
                parallel {
                    stage("Unit tests and Jacoco Test Coverage") {
                        steps {
                            script {
                                lcgAwsEcrLogin()
                                containerBuild1 = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerBuild1)
                                lcgAgentDockerExecService(service, containerBuild1, "make test")
                            }
                        }
                        post {
                            always {
                                script {
                                    lcgAgentDockerRm(containerBuild1)
                                }
                            }
                            success {
                                junit "${relativeTargetDir}/app/build/test-results/**/*.xml"
                                jacoco(
                                        execPattern: "${relativeTargetDir}/app/build/reports/tests/*.exec",
                                        classPattern: "${relativeTargetDir}/app/build/reports/tests/**/classes",
                                        sourcePattern: "${relativeTargetDir}/app/src/main/java"
                                )
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
                    stage("Kotlin code style check") {
                        agent { label primaryAgentLabel }
                        steps {
                            script {
                                cleanWs()
                                unstash name: "artifactSources"

                                lcgAwsEcrLogin()
                                containerBuild2 = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerBuild2)
                                lcgAgentDockerExecService(service, containerBuild2, "make check_kotlin")
                            }
                        }
                        post {
                            always {
                                script {
                                    lcgAgentDockerRm(containerBuild2)
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
                    stage("Lint") {
                        agent { label primaryAgentLabel }
                        steps {
                            script {
                                cleanWs()
                                unstash name: "artifactSources"

                                lcgAwsEcrLogin()
                                containerBuild3 = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerBuild3)
                                lcgAgentDockerExecService(service, containerBuild3, "make lint")
                            }
                        }
                        post {
                            always {
                                script {
                                    lcgAgentDockerRm(containerBuild3)
                                }
                            }
                            success {
                                androidLint canComputeNew: false, defaultEncoding: '', healthy: '', pattern: "${relativeTargetDir}/app/build/reports/*", unHealthy: ''
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
                    stage("Build Coral") {
                        when { expression { return "coral" in brands } }
                        agent { label primaryAgentLabel }
                        steps {
                            script {
                                cleanWs()
                                unstash name: "artifactSources"

                                lcgAwsEcrLogin()
                                containerBuild4 = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerBuild4)
                                lcgAgentDockerExecService(service, containerBuild4, "ASSEMBLE=assembleCoral make build_app")
                                stash includes: "${relativeTargetDir}/app/build/**", name: "artifactCoral"
                            }
                        }
                        post {
                            always {
                                script {
                                    lcgAgentDockerRm(containerBuild4)
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
                    stage("Build Ladbrokes") {
                        when { expression { return "ladbrokes" in brands } }
                        agent { label secondaryAgentLabel }
                        steps {
                            script {
                                cleanWs()
                                unstash name: "artifactSources"

                                lcgAwsEcrLogin()
                                containerBuild5 = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerBuild5)
                                lcgAgentDockerExecService(service, containerBuild5, "ASSEMBLE=assembleLadbrokes make build_app")
                                stash includes: "${relativeTargetDir}/app/build/**", name: "artifactLadbrokes"
                            }
                        }
                        post {
                            always {
                                script {
                                    lcgAgentDockerRm(containerBuild5)
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
            }
            stage("Unstash artifacts") {
                steps {
                    script {
                        unstash name: "artifactSources"
                        unstash name: "artifactCoral"
                        unstash name: "artifactLadbrokes"
                        sh "ls -la ./sources"
                        sh "find sources/"
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
