#!/usr/bin/env groovy

def call(Map arguments = [:], Closure deployJobs = {}) {

    def verbosity = (arguments.verbosity == null) ? 3 : (arguments.verbosity).count("v")
    env.VERBOSITY = verbosity
    lcgCommonFunctions.prettyPrinter(arguments, "Service parameters:")

    // Setting jobs parameters
    def service = arguments.service
    def primaryAgentLabel = params.primaryAgentLabel ?: "native-ios"
    def commonSonarGate = arguments.commonSonarGate ?: [:]
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)

    // Setting IOS specific parameters
    def fastlaneCommand = params.fastlane_Command ?: lcgCommonFunctions.getFastlaneCommand(service, "fastlaneDefaultCommand")
    def fastlaneSonarCommand = params.fastlaneSonarCommand ?: lcgCommonFunctions.getFastlaneCommand(service, "fastlaneSonarCommand")
    def fastlaneKeychainPassword = params.fastlaneKeychainPassword ?: lcgCommonFunctions.getFastlaneCredId(service, "fastlaneKeychainPassword")
    def fastlaneLoginKeychainPassword = params.fastlaneLoginKeychainPassword ?: lcgCommonFunctions.getFastlaneCredId(service, "fastlaneLoginKeychainPassword")
    def fastlaneDistributionCertificatePassword = params.fastlaneDistributionCertificatePassword ?: lcgCommonFunctions.getFastlaneCredId(service, "fastlaneDistributionCertificatePassword")
    def fastlaneDevelopmentCertificatePassword = params.fastlaneDevelopmentCertificatePassword ?: lcgCommonFunctions.getFastlaneCredId(service, "fastlaneDevelopmentCertificatePassword")
    def iosNativeGitUsernamePassword = params.iosNativeGitUsernamePassword ?: lcgCommonFunctions.getIosNativeGitUsernamePassword(service, "iosNativeGitUsernamePassword")
    def workspace = "\$(pwd)"
    def sonarMetadataFilePath = workspace + "/report-task.txt"
    def defaultSonarToken = lcgCommonFunctions.getDefaultSonarToken()

    def typeJob = "notMultiBranch"
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def targetBranchName = ""
    def pullRequestId = ""
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
        targetBranchName = env.CHANGE_TARGET
        pullRequestId = env.CHANGE_ID
        skipCheckout = false
        triggerBitBucket = true
        concurrentBuild = true
        invokeParameters = false
    }

    // Set specific variables for PR (pull request)
    if (typeJob == "multiBranchPR") {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.branch"] = branchName
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.key"] = pullRequestId
        commonSonarGate["parametersSonarCloud"]["-Dsonar.pullrequest.base"] = targetBranchName
    } else {
        commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName
    }
    // Sonar metadata path
    commonSonarGate["parametersSonarCloud"]["-Dsonar.scanner.metadataFilePath"] = sonarMetadataFilePath

    // Switch on/off Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true

    // Switch on/off Quality Gate
    def switchFastlaneBuild = (params.fastlane_build != null) ? params.fastlane_build : true

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Init repositories list for SCM pulling
    def repositoriesList = [service]

    // Sonar params for fastlane
    def sonarParams = lcgCodeQuality.sonarCloudParamsToString(commonSonarGate)

    println "Build parameters:\n================="
    println "Workspace: ${workspace}"
    println "Branch name: ${branchName}"
    println "Skip default checkout: ${skipCheckout}"
    println "Check Quality Gate: ${switchQualityGate}"
    println "Sonar scanner Docker skip: ${lcgCommonFunctions.getServiceSonarScannerDockerSkip(service)}"
    println "Clean workspace: ${switchPostCleanUpWs}"
    lcgCommonFunctions.prettyPrinter(repositoriesList, "Repositories list:")

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
        }
        environment {
            VERBOSITY = "${verbosity}"
            BRANCH = "${branchName}"
            PATH = "$PATH:/usr/local/bin:$HOME/.rbenv/bin:$HOME/.rbenv/shims"
            RBENV_SHELL = "sh"
            LANG = "en_US.UTF-8"
            LANGUAGE = "en_US.UTF-8"
            LC_ALL = "en_US.UTF-8"
            SONAR_PARAMS = "${sonarParams}"
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
                        currentBuild.description = "Branch: ${branchName}\n Fastlane executed with: ${fastlaneCommand}"
                        lcgScmGitParallel(repositoriesList, invokeParameters)
                    }
                }
            }
            stage("Start fastlane build") {
                when { expression { return switchFastlaneBuild } }
                steps {
                    script {
                        withCredentials([string(credentialsId: fastlaneKeychainPassword, variable: 'KeychainPassword'),
                                         string(credentialsId: fastlaneLoginKeychainPassword, variable: 'LoginKeychainPassword'),
                                         string(credentialsId: fastlaneDistributionCertificatePassword, variable: 'DistributionCertificatePassword'),
                                         string(credentialsId: fastlaneDevelopmentCertificatePassword, variable: 'DevelopmentCertificatePassword'),
                                         usernamePassword(credentialsId: iosNativeGitUsernamePassword, usernameVariable: 'IOS_GIT_USER', passwordVariable: 'IOS_GIT_PASSWORD')])
                                {
                                    sh """
                                        GIT_USER="\${IOS_GIT_USER}" 
                                        export GIT_PASSWORD="\${IOS_GIT_PASSWORD}"
                                        echo "echo \$GIT_PASSWORD" > /Users/jenkins/git_env_password.sh && chmod +x /Users/jenkins/git_env_password.sh
                                        export GIT_ASKPASS=/Users/jenkins/git_env_password.sh
                                        echo "DEBUG: \${GIT_USER}"
                                        echo "DEBUG: \${GIT_PASSWORD}"
                                        git config --global credential.username "\${GIT_USER}"
                                        cd ${relativeTargetDir} && fastlane ${fastlaneCommand}
                                    """
                                }
                    }
                }
            }
            stage("Code Analysis") {
                when { expression { return switchQualityGate } }
                steps {
                    script {
                        withCredentials([string(credentialsId: defaultSonarToken, variable: 'SONAR_TOKEN')])
                                {
                                    sh "cd ${relativeTargetDir} && fastlane ${fastlaneSonarCommand}"
                                }
                                    lcgCodeQuality.sonarCloudPull(commonSonarGate, relativeTargetDir)
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
