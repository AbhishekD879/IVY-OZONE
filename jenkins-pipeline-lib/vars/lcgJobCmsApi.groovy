#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    def verbosity = (arguments.verbosity == null) ? 3 : (arguments.verbosity).count("v")
    env.VERBOSITY = verbosity

    // Setting jobs purpose
    def jobAssignmentBuild = arguments.jobAssignmentBuild ?: false
    def jobAssignmentDeploy = arguments.jobAssignmentDeploy ?: false
    def jobLevel = arguments.jobLevel ?: null

    def primaryAgentLabel = arguments.primaryAgentLabel ?: "dev-slave-ui"
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceCmsApi")
    def runtimeImage = lcgCommonFunctions.getServiceRuntimeImage(service)
    def switchDeploy = arguments.switchDeploy ?: false
    def targetEnvs = arguments.targetEnvs ?: []
    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?:
            lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def serviceFortify = arguments.serviceFortify ?: lcgCommonFunctions.getConstantsParameters("common.fortify")
    def dockerEcr = arguments.dockerEcr ?: lcgCommonFunctions.getDefaultEcr()
    def defaultSonarToken = lcgCommonFunctions.getDefaultSonarToken()
    def logNumToKeep = (arguments.logNumToKeep ?: 20).toString()
    def imageTagLength = lcgCommonFunctions.getServiceImageTagLength()
    def nexusCredentialsId = service.nexusCredentialsId
    def multiBranchAutodeploy = service.multiBranchAutodeploy ?: []
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def sonarScannerDockerSkip = lcgCommonFunctions.getServiceSonarScannerDockerSkip(service)

    def typeJob = "notMultiBranch"
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def targetBranchName = ""
    def pullRequestId = ""
    def imageTag = (params.service_image_tag != null) ? lcgCommonFunctions.cleanString(params.service_image_tag) : branchName.take(imageTagLength)

    def skipCheckout = true
    def triggerBitBucket = false
    def concurrentBuild = false
    def invokeParameters = true

    if (env.BRANCH_NAME) {
        typeJob = "multiBranch"
        branchName = BRANCH_NAME
        imageTag = branchName.take(imageTagLength)
        skipCheckout = false
        triggerBitBucket = true
        concurrentBuild = true
        invokeParameters = false
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
    }

    service.branchName = branchName
    service.imageTag = imageTag

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["switchSonarCloudPipelineFailed"] = switchSonarCloudPipelineFailed
    commonSonarGate["sonarScannerDockerSkip"] = sonarScannerDockerSkip   // gradle run sonar scan instead of Docker version
    commonSonarGate["parametersSonarCloud"]["-Dproject.settings"] = ""
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "/opt/workDir/sources/src/"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.exclusions"] = "/opt/workDir/sources/src/**/*.java"

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

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Fortify
    def fortifyPreBuildStage = arguments.fortifyPreBuildStage ?: true
    def switchFortifyScan = params.fortify_scan ?: null
    if ( typeJob == "notMultiBranch" && branchName =~ /^release-.*/ ) {
        switchFortifyScan = "fortify_scan_upload_reports"
    } else {
        switchFortifyScan = "fortify_scan_upload_reports"
        fortifyPreBuildStage = false
    }
    lcgCommonFunctions.prettyPrinter(switchFortifyScan, "Fortify Scan:")

    // Push Docker image to AWS ECR
    switchPush = (typeJob == "notMultiBranch" && jobAssignmentBuild) ? false : true

    // Switch on/off deploy
    switchDeploy = (typeJob == "multiBranchPR") ? false : switchDeploy
    switchDeploy = (params.deploy != null) ? params.deploy : switchDeploy
    switchDeploy = jobAssignmentDeploy ? true : switchDeploy

    // Deploy and Push for multibranch job
    if (typeJob == "multiBranch") {
        switchDeploy = lcgCommonFunctions.getTargetEnvs(multiBranchAutodeploy, targetEnvs, branchName)
        switchPush = switchDeploy
    }

    // Init repositories list for SCM pulling
    def repositoriesList = (typeJob == "notMultiBranch") ? [service, appBuild] : [appBuild]
    repositoriesList = (jobAssignmentDeploy) ? [] : repositoriesList

    // Add service info into target deploy environments
    if (switchDeploy || jobAssignmentDeploy) {
        lcgDeployDocker.prepareEnvsList(targetEnvs, repositoriesList, service)
    }

    println "Build parameters:\n================="
    println "Branch name: ${branchName}"
    println "Service Docker image tag: ${imageTag}"
    println "Job purpose: jobAssignmentBuild: ${jobAssignmentBuild} jobAssignmentDeploy: ${jobAssignmentDeploy}"
    println "Type job: ${typeJob}"
    println "Skip default checkout: ${skipCheckout}"
    println "Deploy: ${switchDeploy}"
    println "Check Quality Gate: ${switchQualityGate}"
    println "Clean workspace: ${switchPostCleanUpWs}"
    println "Push images to ECR: ${switchPush}"
    lcgCommonFunctions.prettyPrinter(repositoriesList, "Repositories list:")
    lcgCommonFunctions.prettyPrinter(targetEnvs, "Target environments:")

    // Prohibit release branches on dev job
    if (branchName =~ /^release-.*/ && jobLevel == "dev" ) {
        error "Release branches are prohibited on DEV jobs! Use PROD jobs instead"
    }

    if (jobAssignmentBuild || typeJob in ["multiBranch", "multiBranchPR"]) {
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
            parameters {
                booleanParam(name: 'clean_ws', defaultValue: true, description: 'Clean up workspace in post build action')
            }
            environment {
                VERBOSITY = "${verbosity}"
                SERVICE_RUNTIME_IMAGE = "${runtimeImage}"
                SCRIPTS_PATH = "../${relativeTargetDirAppBuild}"
                SOURCES_PATH = "../${relativeTargetDir}"
                REGISTRY = "${dockerEcr}"
                BRANCH = "${branchName}"
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
                            sh "env"
                            currentBuild.description = "Branch: ${branchName} Image tag: ${imageTag}"
                            lcgScmGitParallel(repositoriesList, invokeParameters)
                            sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/"
                            sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Dockerfile ${relativeTargetDir}/"
                            sh "cd ${relativeTargetDir} && git checkout -b ${branchName}"
                            lcgAwsEcrLogin()
                        }
                    }
                }
                stage("Fortify simple scanning") {
                    when { expression { return switchFortifyScan == "fortify_simple_scan" && fortifyPreBuildStage } }
                    steps {
                        script {
                            lcgCodeQualityFortify(serviceFortify, relativeTargetDir)
                        }
                    }
                }
                stage("Fortify upload reports to Fortify server") {
                    when { expression { return switchFortifyScan == "fortify_scan_upload_reports" && fortifyPreBuildStage } }
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
                                        lcgAgentDockerExecService(service, containerBuild, "SONAR_PARAMS=\\\"${sonarParams}\\\" make build_artifact")
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
                    steps {
                        script {
                            lcgCommonFunctions.setNexusServerProperties(service)
                            sh "make -C ${relativeTargetDir} build_application"
                        }
                    }
                }
                stage("Push image to ECR") {
//                    when { expression { return switchPush } }
                    steps {
                        script {
                            sh "make -C ${relativeTargetDir} push"
                        }
                    }
                }
                stage("Start integration tests") {
                    steps {
                        build job: "CRLAT-CMS-API-DEV3-BACK-END-INTEGRATION-TESTING",
                            parameters: [
                                    string(name: "service_image_tag", value: "${branchName}")
                            ],
                        wait: false
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
                stage("Fortify simple scan") {
                    when { expression { return switchFortifyScan == "fortify_simple_scan" && !fortifyPreBuildStage } }
                    steps {
                        script {
                            lcgCodeQualityFortify(serviceFortify, relativeTargetDir)
                        }
                    }
                }
                stage("Fortify upload reports ") {
                    when { expression { return switchFortifyScan == "fortify_scan_upload_reports" && !fortifyPreBuildStage } }
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

    if (jobAssignmentDeploy) {
        pipeline {
            agent {
                node {
                    label primaryAgentLabel
                }
            }
            options {
                skipDefaultCheckout(true)
                timestamps()
            }
            parameters {
                booleanParam(name: 'clean_ws', defaultValue: true, description: 'Clean up workspace in post build action')
            }
            stages {
                stage("Set build parameters") {
                    steps {
                        script {
                            lcgCommonHudsonFunctions.jobSetTriggerBitBucket(false)
                            lcgCommonHudsonFunctions.jobSetConcurrentBuild(false)
                        }
                    }
                }
                stage("Sanity workspace") {
                    steps {
                        deleteDir()
                    }
                }
                stage('Getting SCM sources') {
                    steps {
                        script {
                            currentBuild.description = "Image tag: ${imageTag}"
                            lcgScmGitParallel(repositoriesList, false)
                            lcgAwsEcrLogin()
                        }
                    }
                }
                stage("Deploy") {
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
                success {
                    script {
                        lcgNotify.notifySuccessful(targetEnvs)
                    }
                }
                aborted {
                    script {
                        lcgNotify.notifyAborted(targetEnvs)
                    }
                }
                failure {
                    script {
                        lcgNotify.notifyFailed(targetEnvs)
                    }
                }
            }
        }
    }
}