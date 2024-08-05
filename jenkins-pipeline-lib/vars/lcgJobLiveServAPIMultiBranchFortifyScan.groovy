#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    def primaryAgentLabel = arguments.primaryAgentLabel ?: "dev-slave"
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceLiveServAPI")
    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def serviceFortify = arguments.serviceFortify ?: lcgCommonFunctions.getConstantsParameters("common.fortify")

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

    // Set Sonar Cloud parameters
    //  - bash ./gradlew sonarqube
    //  -Dsonar.projectKey=LIVESERV-API
    //  -Dsonar.organization=coral-devops-support-bitbucket
    //  -Dsonar.host.url=https://sonarcloud.io
    //  -Dsonar.login=$SONAR_TOKEN
    //  -Dsonar.branch.name=$BITBUCKET_BRANCH
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["switchSonarCloudPipelineFailed"] = switchSonarCloudPipelineFailed
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectKey"] = "LIVESERV-API"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.language"] = "java"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.java.binaries"] = "src"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sources"] = "src"

    // Set specific variables for PR (pull request)
    if (typeJob == "multiBranchPR") {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.branch"] = CHANGE_BRANCH
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.key"] = CHANGE_ID
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.base"] = CHANGE_TARGET
    } else {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName
    }

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

    // Fortify
    def switchFortifyScan = params.fortify_scan ?: null
    if ( typeJob == "notMultiBranch" && branchName =~ /^release-.*/ ) {
        switchFortifyScan = "fortify_scan_upload_reports"
    } else {
        switchFortifyScan = "none"
    }
    lcgCommonFunctions.prettyPrinter(switchFortifyScan, "Fortify Scan:")

    // Switch on/off deploy
    def switchDeploy = true
    if (params.containsKey("deploy")) {
        if (!params.deploy) {
            switchDeploy = false
        }
    }
    // Deploy branches list
    def deployBranches = ["master"]
    if ((branchName in deployBranches && switchDeploy)) {
        switchDeploy = true
    }
    else
    {
        switchDeploy = false
    }

    println "Deploy: ${switchDeploy} Branches: ${deployBranches}"

    def repositoriesList = [service]

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
        }
        parameters {
            booleanParam(name: 'clean_ws', defaultValue: true, description: 'Clean up workspace in post build action')
        }
        stages {
            stage("Sanity workspace") {
                when { expression { return typeJob == "notMultiBranch" } }
                steps {
                    deleteDir()
                }
            }
            stage('Getting SCM sources') {
                steps {
                    script {
                        currentBuild.description = "Branch: ${branchName}"
                        lcgScmGitParallel(repositoriesList, false)
                    }
                }
            }
//            stage("Test and Build") {
//                steps {
//                    script {
//                        lcgAwsEcrLogin()
//                        containerBuild = lcgAgentDockerRun(service)
//                        lcgAgentDockerBootstrap(containerBuild)
//                        lcgAgentDockerExecService(service, containerBuild, './gradlew test build release -PnexusUser=symphony.devs "-PnexusPass=D3V$.symph0nY"')
//                    }
//                }
//            }
//            stage("Code Analysis") {
//                when { expression { return switchQualityGate } }
//                steps {
//                    script {
//                        lcgCodeQuality.sonarCloudPull(commonSonarGate)
//                    }
//                }
//            }
            stage ("Fortify simple scan") {
                when { expression { return switchFortifyScan == "fortify_simple_scan" } }
                steps {
                    script {
                        lcgCodeQualityFortify(serviceFortify, relativeTargetDir)
                    }
                }
            }
            stage ("Fortify upload reports ") {
                when { expression { return switchFortifyScan == "fortify_scan_upload_reports" } }
                steps {
                    script {
                        lcgCodeQualityFortify(serviceFortify, relativeTargetDir, "upload_reports")
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
