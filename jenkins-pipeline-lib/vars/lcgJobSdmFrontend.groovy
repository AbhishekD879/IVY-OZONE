#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    def primaryAgentLabel = arguments.primaryAgentLabel ?: "dev-slave-ui"
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceSdmFrontend")
    def serviceApp = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceSdmFrontendApp")
    def serviceTests = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceSdmFrontendTests")
    def switchSonarCloudPipelineFailed = arguments.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def serviceFortify = arguments.serviceFortify ?: lcgCommonFunctions.getConstantsParameters("common.fortify")
    def targetEnvs = [arguments.targetEnvs ?: lcgCommonFunctions.getConstantsParameters("awsCoralCloudFront.sdmFrontendApp.dev0")]
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
        branchName = env.CHANGE_BRANCH
        typeJob = "multiBranchPR"
        skipCheckout = false
    }
    service["branchName"] = branchName

    println "Branch name: ${branchName}"
    println "Type job: ${typeJob}"
    println "Skip default checkout: ${skipCheckout}"

    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def relativeTargetDirApp = lcgCommonFunctions.getGitTargetDirectory(serviceApp)
    def relativeTargetDirTests = lcgCommonFunctions.getGitTargetDirectory(serviceTests)
    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def repositoriesList = [service, serviceApp, serviceTests, appBuild]

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir

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

    // Switch on/off clean up workspace in post build action
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

    // Switch on/off Autotests with Chrome
    def switchAutotestsChrome = (params.AutotestsChrome != null) ? params.AutotestsChrome : true

    // Switch on/off Autotests with Firefox
    def switchAutotestsFF = (params.AutotestsFF != null) ? params.AutotestsFF : false

    // Switch on/off Autotests with Internet Explorer
    def switchAutotestsIE = (params.AutotestsIE != null) ? params.AutotestsIE : false

    // Switch on/off deploy
//    def switchDeploy = true
//    if (params.containsKey("deploy")) {
//        if (!params.deploy) {
//            switchDeploy = false
//        }
//    }
//    // Deploy branches list
//    def deployBranches = ["master"]
//    if ((branchName in deployBranches && switchDeploy)) {
//        switchDeploy = true
//    }
//    else
//    {
//        switchDeploy = false
//    }
//
//    println "Deploy: ${switchDeploy} Branches: ${deployBranches}"

    // Add service info into target deployment environments
    lcgDeployAws.prepareEnvsList(targetEnvs, serviceApp)

    println "Target envs: ${targetEnvs}"
    println "Repositories list: ${repositoriesList}"

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
        environment {
            NODE_VERSION = "8.9.3"
            CONTEXT = "${branchName}"
        }
        parameters {
            booleanParam(name: 'clean_ws', defaultValue: true, description: 'Clean up workspace in post build action')
            booleanParam(name: 'AutotestsChrome', defaultValue: true, description: 'Run Autotests Chrome')
            booleanParam(name: 'AutotestsFF', defaultValue: false, description: 'Run Autotests Firefox')
            booleanParam(name: 'AutotestsIE', defaultValue: false, description: 'Run Autotests Internet Explorer')
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
                        lcgScmGitParallel(repositoriesList, true)
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
            stage("Start Docker Build Container") {
                steps {
                    script {
                        lcgAwsEcrLogin()
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
                        lcgAgentDockerExecService(service, containerBuild, "make npm_install_local")
                    }
                }
            }
            stage("Test and Build") {
                parallel {
                    stage("Unit Tests") {
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make npm_run_tests")
                            }
                        }
                    }
                    stage("Autotests") {
                        stages {
                            stage("Build Component") {
                                steps {
                                    script {
                                        lcgAgentDockerExecService(service, containerBuild, "make npm_build_component")
                                    }
                                }
                            }
                            stage("Start Docker Build Container App") {
                                steps {
                                    script {
                                        containerBuildApp = lcgAgentDockerRun(serviceApp)
                                        lcgAgentDockerBootstrap(containerBuildApp)
                                    }
                                }
                            }
                            stage("Build Test App") {
                                steps {
                                    script {
                                        sh "rm -rf ${relativeTargetDirApp}/src/scoreboard"
                                        sh "cp -rv ${relativeTargetDir}/dist-testapp/scoreboard ${relativeTargetDirApp}/src/scoreboard"
                                        sh "cp -v ${relativeTargetDir}/src/builders/buildInfo.json ${relativeTargetDirApp}/src/scoreboard/buildInfo.json"
                                        sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDirApp}/"
                                        lcgCommonFunctions.setNexusServerProperties(serviceApp)
                                        lcgAgentDockerExecService(serviceApp, containerBuildApp, "make npm_build_test_app")
                                    }
                                }
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
                steps {
                    script {
                        lcgDeploy.deploy(targetEnvs)
                    }
                }
            }
            stage ("Post deploy") {
                steps {
                    script {
                        lcgDeploy.post(targetEnvs)
                    }
                }
            }
            stage("Start Docker Container for Autotests Chrome") {
                steps {
                    script {
                        if (switchAutotestsChrome) {
                            containerTests = lcgAgentDockerRun(serviceTests)
                            lcgAgentDockerBootstrap(containerTests)
                        }
                    }
                }
            }
            stage("Run Autotests Chrome") {
                steps {
                    script {
                        if (switchAutotestsChrome) {
                            sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDirTests}/"
                            lcgAgentDockerExecService(serviceTests, containerTests, "make gradle_test_app")
                            lcgAgentDockerRm(containerTests)
                        }
                    }
                }
            }
            stage("Start Docker Container for Autotests Firefox") {
                steps {
                    script {
                        if (switchAutotestsFF) {
                            serviceTests.buildImage = "740335462382.dkr.ecr.eu-west-2.amazonaws.com/selenium-gradle-firefox:71.0"
                            containerTests = lcgAgentDockerRun(serviceTests)
                            lcgAgentDockerBootstrap(containerTests)
                        }
                    }
                }
            }
            stage("Run Autotests Firefox") {
                steps {
                    script {
                        if (switchAutotestsFF) {
                            sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDirTests}/"
                            lcgAgentDockerExecService(serviceTests, containerTests, "make gradle_test_app_ff")
                            lcgAgentDockerRm(containerTests)
                        }
                    }
                }
            }
            stage("Run Autotests IE") {
                agent { label "dev-slave-win-ui" }
                steps {
                    script {
                        if (switchAutotestsIE) {
                            lcgScmGitParallel([serviceTests, appBuild], true)
                            sh """
                            cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDirTests}/
                            cd ${relativeTargetDirTests} && make gradle_test_app_ie
                            """
                        }
                    }
                }
            }
            stage("Fortify simple scanning") {
                when { expression { return switchFortifyScan == "fortify_simple_scan" && !fortifyPreBuildStage} }
                steps {
                    script {
                        lcgCodeQualityFortify(serviceFortify, relativeTargetDir)
                    }
                }
            }
            stage("Fortify upload reports to Fortify server") {
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
                            allure([
                                    includeProperties: false,
                                    jdk: "",
                                    report: "${relativeTargetDirTests}/build/reports/allure-report",
                                    properties: [],
                                    reportBuildPolicy: "ALWAYS",
                                    results: [[path: "${relativeTargetDirTests}/build/allure-results"]]
                            ])
                }
                script {
                    if (binding.hasVariable('containerBuild')) {
                        lcgAgentDockerRm(containerBuild)
                    }
                    if (binding.hasVariable('containerBuildApp')) {
                        lcgAgentDockerRm(containerBuildApp)
                    }
                    if (binding.hasVariable('containerTests')) {
                        lcgAgentDockerRm(containerTests)
                    }
                }
            }
        }
    }
}
