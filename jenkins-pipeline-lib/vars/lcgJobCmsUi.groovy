#!/usr/bin/env groovy

def call(Map arguments = [:]) {
    def verbosity = (arguments.verbosity == null) ? 3 : (arguments.verbosity).count("v")
    env.VERBOSITY = verbosity

    def primaryAgentLabel = arguments.primaryAgentLabel ?: "dev-slave"
    def forceReleaseFortify = arguments.forceReleaseFortify ?: false
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceCmsUi")
    def switchDeploy = arguments.switchDeploy ?: true
    def targetEnvs = arguments.targetEnvs ?: []
    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?:
            lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def serviceFortify = arguments.serviceFortify ?: lcgCommonFunctions.getConstantsParameters("common.fortify")
    def logNumToKeep = (arguments.logNumToKeep ?: 20).toString()
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def multiBranchAutodeploy = service.multiBranchAutodeploy ?: []
    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)

    def typeJob = "notMultiBranch"
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def skipCheckout = true
    def triggerBitBucket = false
    def concurrentBuild = false
    def invokeParameters = true

    if (env.BRANCH_NAME) {
        typeJob = "multiBranch"
        branchName = BRANCH_NAME
        skipCheckout = false
        triggerBitBucket = true
        concurrentBuild = true
        invokeParameters = false
    }
    if (env.CHANGE_TARGET) {
        typeJob = "multiBranchPR"
        branchName = env.CHANGE_BRANCH
        skipCheckout = false
        triggerBitBucket = true
        concurrentBuild = true
        invokeParameters = false
    }
    service.branchName = branchName

    // Select angular version
    def angularVersion = params.angular_version ?: arguments.angularVersion
    def makeTarget = "build_app"
    println "angularVersion: ${angularVersion}"
    switch (angularVersion) {
        case ~/^4$/:
            service.buildImage = "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:8.9.4.2";
            makeTarget = "build_app_angular4"
            break;
        case ~/^9$/:
            service.buildImage = "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:12.18.2.1";
            makeTarget = "build_app_angular9"
            break;
        default:
            println "Angular version selector: unable to select proper version, will use defaults"
            break;
    }
    println "service.buildImage: ${service.buildImage}"
    println "makeTarget: ${makeTarget}"

    // Set build parameters
    def aot = (params.aot) ? "--prod" : ""
    println "AOT: ${aot}"

    def env_profile = params.cms_env_profile ?: "dev0"
    println "Profile: ${env_profile}"

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["switchSonarCloudPipelineFailed"] = switchSonarCloudPipelineFailed
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./${relativeTargetDir}"

    // Set specific variables for PR (pull request)
    if (typeJob == "multiBranchPR") {
        
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.branch"] = CHANGE_BRANCH
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.key"] = CHANGE_ID
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.base"] = CHANGE_TARGET
    } else {
        
        commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName
    }

    // Switch on/off Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true
    println "Check Quality Gate: " + switchQualityGate
    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Fortify
    def fortifyPreBuildStage = arguments.fortifyPreBuildStage ?: true
    def switchFortifyScan = params.fortify_scan ?: null
    if ( typeJob == "notMultiBranch" && branchName =~ /^release-.*/ && forceReleaseFortify  ) {
        switchFortifyScan = "fortify_scan_upload_reports"
    } else {
        switchFortifyScan = "fortify_scan_upload_reports"
        fortifyPreBuildStage = false
    }
    lcgCommonFunctions.prettyPrinter(switchFortifyScan, "Fortify Scan:")

    // Switch on/off deploy
    switchDeploy = (typeJob == "multiBranchPR") ? false : switchDeploy
    switchDeploy = (params.deploy != null) ? params.deploy : switchDeploy

    // Autodeploy for multiBranch
    if (typeJob == "multiBranch") {
        switchDeploy = lcgCommonFunctions.getTargetEnvs(multiBranchAutodeploy, targetEnvs, branchName)
    }

    // Add service info into target deployment environments
    if (switchDeploy) {
        lcgDeployAws.prepareEnvsList(targetEnvs, service)
    }

    // Init repositories list for SCM pull
    def repositoriesList = (typeJob == "notMultiBranch") ? [service, appBuild] : [appBuild]

    println "Build parameters:\n================="
    println "Branch name: ${branchName}"
    println "Type job: ${typeJob}"
    println "Skip default checkout: ${skipCheckout}"
    println "Deploy: ${switchDeploy}"
    println "Check Quality Gate: ${switchQualityGate}"
    println "Clean workspace: ${switchPostCleanUpWs}"
    lcgCommonFunctions.prettyPrinter(repositoriesList, "Repositories list:")
    lcgCommonFunctions.prettyPrinter(targetEnvs, "Target environments:")

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
            booleanParam(name: "aot", defaultValue: false, description: "Flag to enable AOT")
            booleanParam(name: "clean_ws", defaultValue: true, description: "Clean up workspace in post build action")
            }
        environment {
                VERBOSITY = "${verbosity}"
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
                            currentBuild.description = "Branch: ${branchName} Profile: ${env_profile} AOT: ${aot}"
                            lcgScmGitParallel(repositoriesList, invokeParameters)
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
                            containerBuild = lcgAgentDockerRun(service)
                            lcgAgentDockerBootstrap(containerBuild)
                        }
                    }
                }
            stage("Pre build tasks") {
                    steps {
                        script {
                            sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/"
                            lcgCommonFunctions.setNexusServerProperties(service)
                        }
                    }
                }
            stage("NPM install local") {
                    steps {
                        script {
                            lcgCommonFunctions.setNexusServerProperties(service)
                            lcgAgentDockerExecService(service, containerBuild, "make npm_install_local")
                        }
                    }
                }
            stage("Build") {
                    steps {
                        script {
                            lcgAgentDockerExecService(service, containerBuild, "ENV_PROFILE=${env_profile} AOT=${aot} make ${makeTarget}")
                        }
                    }
                }
            /*stage("Code Analysis") {
                    when { expression { return switchQualityGate } }
                    steps {
                        script {
                            lcgCodeQuality.sonarCloudPull(commonSonarGate)
                        }
                    }
                }*/
            stage("Deploy") {
                    when { expression { return switchDeploy } }
                    steps {
                        script {
                            lcgDeploy.deploy(targetEnvs)
                        }
                    }
                }
            stage ("Post deploy") {
                    when { expression { return switchDeploy } }
                    steps {
                        script {
                            lcgDeploy.post(targetEnvs)
                        }
                    }
                }
            stage("Fortify simple scan") {
                when { expression { return switchFortifyScan == "fortify_simple_scan" && fortifyPreBuildStage } }
                steps {
                    script {
                        lcgCodeQualityFortify(serviceFortify, relativeTargetDir)
                    }
                }
            }
            stage("Fortify upload reports ") {
                when { expression { return switchFortifyScan == "fortify_scan_upload_reports" && fortifyPreBuildStage } }
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
