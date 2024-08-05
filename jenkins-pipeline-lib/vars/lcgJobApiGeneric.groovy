#!/usr/bin/env groovy

def call(Map arguments = [:], Closure deployJobs = {}) {

    def verbosity = (arguments.verbosity == null) ? 3 : (arguments.verbosity).count("v")
    env.VERBOSITY = verbosity
    lcgCommonFunctions.prettyPrinter(arguments, "Service parameters:")

    // Setting jobs parameters
    def service = arguments.service
    def primaryAgentLabel = arguments.primaryAgentLabel ?: "dev-slave"
    def commonSonarGate = arguments.commonSonarGate ?: [:]
    def serviceFortify = arguments.serviceFortify ?: lcgCommonFunctions.getConstantsParameters("common.fortify")
    def imageTagLength = arguments.imageTagLength ?: lcgCommonFunctions.getServiceImageTagLength()
    def nexusCredentialsId = arguments.nexusCredentialsId ?: lcgCommonFunctions.getServiceNexusCredentialsId(service)
    def deploymentTimeout = arguments.deploymentTimeout ?: 1200 // seconds
    def dockerEcr = arguments.dockerEcr ?: lcgCommonFunctions.getDefaultEcr()
    def defaultSonarToken = lcgCommonFunctions.getDefaultSonarToken()
    def logNumToKeep = (arguments.logNumToKeep ?: 20).toString()
    def runtimeImage = lcgCommonFunctions.getServiceRuntimeImage(service)
    def autoDeployBranchesList = lcgCommonFunctions.getServiceAutoDeployBranchesList(service)
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def containerBuild = ""
    def jobLevel = arguments.jobLevel ?: null

    def typeJob = "notMultiBranch"
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def targetBranchName = ""
    def pullRequestId = ""
    def imageTag = branchName.take(imageTagLength)
    def tagId = ""
    def skipCheckout = true
    def triggerBitBucket = false
    def concurrentBuild = false
    def invokeParameters = true
    def switchPush = true
    def switchDeploy = false

    if (env.BRANCH_NAME) {
        typeJob = "multiBranch"
        branchName = BRANCH_NAME
        imageTag = branchName.take(imageTagLength)
        skipCheckout = false
        triggerBitBucket = true
        concurrentBuild = true
        invokeParameters = false
        switchPush = (branchName in autoDeployBranchesList) ? true : false
        switchDeploy = (branchName in autoDeployBranchesList) ? true : false
    }

    if (env.CHANGE_TARGET) {
        typeJob = "multiBranchPR"
        branchName = env.CHANGE_BRANCH
        targetBranchName = env.CHANGE_TARGET
        pullRequestId = env.CHANGE_ID
        imageTag = branchName.take(imageTagLength)
        skipCheckout = false
        triggerBitBucket = true
        concurrentBuild = true
        invokeParameters = false
        switchPush = false
        switchDeploy = false
    }

    // Set specific variables for PR (pull request)
    if (typeJob == "multiBranchPR") {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.branch"] = branchName
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.key"] = pullRequestId
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.base"] = targetBranchName
    } else {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName
    }

    // Switch on/off Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true

    // Switch on/off Sonar Scanner in Gradle project
    def sonarScannerGradleSkip = (lcgCommonFunctions.getServiceSonarScannerGradleSkip(service) == null) ? true : lcgCommonFunctions.getServiceSonarScannerGradleSkip(service)
    sonarScannerGradleSkip = !switchQualityGate ? true : sonarScannerGradleSkip

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Fortify
    def switchFortifyScan = params.fortify_scan ?: null
    if ( typeJob == "notMultiBranch" && branchName =~ /^release-.*/ ) {
        switchFortifyScan = "fortify_scan_upload_reports"
    } else {
        switchFortifyScan = "none"
    }
    lcgCommonFunctions.prettyPrinter(switchFortifyScan, "Fortify Scan:")

    // Init repositories list for SCM pulling
    def repositoriesList = (typeJob == "notMultiBranch") ? [service, appBuild] : [appBuild]

    println "Build parameters:\n================="
    println "Branch name: ${branchName}"
    println "Service Docker image tag: ${imageTag}"
    println "Push images to ECR: ${switchPush}"
    println "Skip default checkout: ${skipCheckout}"
    println "Deploy: ${switchDeploy}"
    println "Check Quality Gate: ${switchQualityGate}"
    println "Sonar scanner Gradle project skip: ${sonarScannerGradleSkip}"
    println "Sonar scanner Docker skip: ${lcgCommonFunctions.getServiceSonarScannerDockerSkip(service)}"
    println "Fortify scanner: ${switchFortifyScan}"
    println "Clean workspace: ${switchPostCleanUpWs}"
    lcgCommonFunctions.prettyPrinter(repositoriesList, "Repositories list:")

    // Prohibit release branches on dev job
    if (branchName =~ /^release-.*/ && jobLevel == "dev" ) {
        error "Release branches are prohibited on DEV jobs! Use PROD jobs instead"
    }

    pipeline {
        agent {
            node {
                label primaryAgentLabel
            }
        }
        options {
            skipDefaultCheckout(skipCheckout)
            checkoutToSubdirectory(relativeTargetDir)
            timestamps()
            buildDiscarder(logRotator(numToKeepStr: logNumToKeep))
            }
        environment {
            VERBOSITY = "${verbosity}"
            SERVICE_RUNTIME_IMAGE = "${runtimeImage}"
            REGISTRY = "${dockerEcr}"
            BRANCH = "${branchName}"
            TAG_LENGTH = "${imageTagLength}"
        }
        stages {
            stage("Set build parameters") {
                    steps {
                        script {
                            lcgCommonHudsonFunctions.jobSetTriggerBitBucket(triggerBitBucket)
                            lcgCommonHudsonFunctions.jobSetConcurrentBuild(concurrentBuild)
                        }
                    }
                }
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
                        currentBuild.description = "Branch: ${branchName} Image tag: ${imageTag}"
                        lcgScmGitParallel(repositoriesList, invokeParameters)
                        tagId = (lcgCommonFunctions.getGitIdCommit(service)).take(imageTagLength)
                        lcgAwsEcrLogin()
                        sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/"
                        sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Dockerfile ${relativeTargetDir}/"
                        sh "cd ${relativeTargetDir} && git checkout -b ${branchName}"
                        }
                    }
                }
                stage("Fortify simple scanning") {
                    when { expression { return switchFortifyScan == "fortify_simple_scan" } }
                    steps {
                        script {
                            lcgCodeQualityFortify(serviceFortify, relativeTargetDir)
                        }
                    }
                }
                stage("Fortify upload reports to Fortify server") {
                    when { expression { return switchFortifyScan == "fortify_scan_upload_reports" } }
                    steps {
                        script {
                            lcgCodeQualityFortify(serviceFortify, relativeTargetDir, "upload_reports")
                        }
                    }
                }
                stage("Start Docker Build Container") {
                    steps {
                        script {
                            withCredentials([usernamePassword(credentialsId: nexusCredentialsId,
                                    usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                                containerBuild = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerBuild)
                            }
                        }
                    }
                }
                stage("Build artifact") {
                    steps {
                        script {
                            withCredentials([string(credentialsId: defaultSonarToken, variable: 'SONAR_TOKEN')])
                                    {
                                        if (typeJob == "multiBranchPR") {
                                            sh "cd ${relativeTargetDir} && git fetch --no-tags ${service.url} +refs/heads/${targetBranchName}:refs/remotes/origin/${targetBranchName}"
                                        }
                                        def sonarParams = lcgCodeQuality.sonarCloudParamsToStringWithCreds(commonSonarGate)
                                        lcgAgentDockerExecService(service, containerBuild, "SONAR_SKIP=${sonarScannerGradleSkip} SONAR_PARAMS=\\\"${sonarParams}\\\" make build_artifact")
                                    }
                        }
                    }
                }
                stage("Code Analysis") {
                    when { expression { return switchQualityGate } }
                    steps {
                        script {
                            lcgCodeQuality.sonarCloudPull(commonSonarGate, relativeTargetDir)
                        }
                    }
                }
                stage("Build runtime image") {
                    environment {
                        TAG_ID = "${tagId}"
                    }
                    steps {
                        script {
                                lcgAgentDocker.build(service)
                            }
                        }
                    }
                stage("Push image to ECR") {
                    environment {
                        TAG_ID = "${tagId}"
                    }
                    when { expression { return switchPush } }
                    steps {
                        script {
                            lcgAgentDocker.push(service)
                        }
                    }
                }
                stage("Deploy") {
                    when { expression { return switchDeploy } }
                    steps {
                        script {
                            deployJobs([branchName: branchName, imageTag: imageTag, deploymentTimeout: deploymentTimeout]).call()
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
                    lcgAgentDockerRm(containerBuild)
                }
            }
        }
    }
}
