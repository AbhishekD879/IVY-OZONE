/*
*
* Build Coral & Ladbrokes based on Vanilla
*
* For Multibranch pipeline strategy
* BRANCH_NAME is defined only in Multibranch job
*
*/

def call(Map arguments = [:]) {

    env.VERBOSITY = 3
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceBma")
    def agentLabel = arguments.agentLabel ?: "dev-slave-ui"
    def switchDeploy = arguments.switchDeploy ?: false
    def autoDeployBranches = ["develop"]
    def brands = arguments.brands ?: ["coral", "ladbrokes"]
    def appPlatform = arguments.appPlatform ?: ["mobile", "desktop"]
    def coral_env_profile = arguments.coral_env_profile ?: "production"
    def ladbrokes_env_profile = arguments.ladbrokes_env_profile ?: "ladbrokes-tst2"
    def logNumToKeep = (arguments.logNumToKeep ?: 5).toString()
    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def repositoriesList = [appBuild]
    def typeJob = "notMultiBranch"
    def branchName = BRANCH_NAME
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def switchSonarCloudPipelineFailed = service.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    service["branchName"] = branchName

    // Allowing concurrent build per branches
    def switchBuildMainRelease = false
    if (branchName.matches("^release-(.*)") || branchName.matches("^develop")) {
        switchBuildMainRelease = true
    }

    if (env.BRANCH_NAME) {
        typeJob = "multiBranch"
        branchName = BRANCH_NAME
        skipCheckout = false
    }

    if (env.CHANGE_TARGET) {
        typeJob = "multiBranchPR"
        branchName = env.CHANGE_BRANCH
        skipCheckout = false
    }

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

    // Switch on/off Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true
    println "Check Quality Gate: " + switchQualityGate

    // Switch EverGreen
    def switchEverGreen = (params.switchEverGreen != null) ? params.switchEverGreen : true
    println "Build EverGreen: " + switchEverGreen

    // Switch on/off clean up workspace in post build action
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Generate Compodoc
    def switchCompodoc = (branchName.matches("^develop")) ? true : false
    switchCompodoc = (params.compodoc) ? true : switchCompodoc
    compodocS3Bucket = service.compodocS3Bucket
    compodocS3BucketRegion = service.compodocS3BucketRegion
    println "Compodoc: ${switchCompodoc} compodocS3Bucket: ${compodocS3Bucket} compodocS3Bucket: ${compodocS3Bucket}"

    // Switch on/off verification on data-crlat attributes
    def switchRunTestAttrs = (params.run_test_attrs != null) ? params.run_test_attrs : true
    println "Verification data-crlt attributes : ${switchRunTestAttrs}"

    // Autodeploy
    if ( branchName in autoDeployBranches ) {
        switchDeploy = true
    }
    println "Deploy: ${switchDeploy} Branches: ${autoDeployBranches}"

    pipeline {
        agent {
            node {
                label agentLabel
            }
        }
        triggers {
            bitbucketPush()
        }
        options {
            skipDefaultCheckout(skipCheckout)
            checkoutToSubdirectory(relativeTargetDir)
            timestamps()
            timeout(time: 120, unit: 'MINUTES')
            buildDiscarder(logRotator(numToKeepStr: logNumToKeep))
        }
        stages {
            stage("Pre build actions") {
                steps {
                    script {
                        if (switchBuildMainRelease) {
                            lcgCommonHudsonFunctions.jobSetConcurrentBuild(false)
                        } else {
                            lcgCommonHudsonFunctions.abortPreviousBuilds()
                        }
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
                        currentBuild.description = "Branch: ${branchName}, Brand: ${brands.join(', ')}, Profile: ${coral_env_profile}, ${ladbrokes_env_profile}, Platform: ${appPlatform.join(', ')}"
                        lcgScmGitParallel(repositoriesList, false)
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
                        lcgAgentDockerExecService(service, containerBuild, "make pre_build_tasks")
                    }
                }
            }
            stage("NPM install global") {
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "make npm_install_global")
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
            stage('Generate Coral SVG') {
                when { expression { return "coral" in brands } }
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "BRAND=coral make generate_svg")
                    }
                }
            }
            stage('Generate Ladbrokes SVG') {
                when { expression { return "ladbrokes" in brands } }
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "BRAND=ladbrokes make generate_svg")
                    }
                }
            }
            stage("Test and Build") {
                parallel {
                    stage("Coverage report and Code Analysis") {
                        stages {
                            stage("Coverage report") {
                                steps {
                                    script {
                                        lcgAgentDockerExecService(service, containerBuild, "make coverage_report")
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
                    }
                    stage("TypeScript Lint") {
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make lint")
                            }
                        }
                    }
                    stage("Build Coral-Vanilla") {
                        stages {
                            stage("Build Coral-Vanilla Mobile") {
                                when { expression { return "coral" in brands && "mobile" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "coral_mobile")
                                        lcgAgentDockerExecServiceClone(service, "coral_mobile", containerBuild, "BRAND=coral BRAND_PLATFORM_SUBCOMMAND=CoralMobile BRAND_PLATFORM=coralMobile PLATFORM=mobile ENV_PROFILE=${coral_env_profile} make build_app_all_vanilla")
                                    }
                                }
                            }
                            stage("Build Coral-Vanilla Desktop") {
                                when { expression { return "coral" in brands && "desktop" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "coral_desktop")
                                        lcgAgentDockerExecServiceClone(service, "coral_desktop", containerBuild, "BRAND=coral BRAND_PLATFORM_SUBCOMMAND=CoralDesktop BRAND_PLATFORM=coralDesktop PLATFORM=desktop ENV_PROFILE=${coral_env_profile} make build_app_all_vanilla")
                                    }
                                }
                            }
                        }
                    }
                    stage("Build Ladbrokes-Vanilla") {
                        stages {
                            stage("Build Ladbrokes-Vanilla Mobile") {
                                when { expression { return "ladbrokes" in brands && "mobile" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "ladbrokes_mobile")
                                        lcgAgentDockerExecServiceClone(service, "ladbrokes_mobile", containerBuild, "BRAND=ladbrokes BRAND_PLATFORM_SUBCOMMAND=LadbrokesMobile BRAND_PLATFORM=ladbrokesMobile PLATFORM=mobile ENV_PROFILE=${ladbrokes_env_profile} make build_app_all_vanilla")
                                    }
                                }
                            }
                            stage("Build Ladbrokes-Vanilla Desktop") {
                                when { expression { return "ladbrokes" in brands && "desktop" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "ladbrokes_desktop")
                                        lcgAgentDockerExecServiceClone(service, "ladbrokes_desktop", containerBuild, "BRAND=ladbrokes BRAND_PLATFORM_SUBCOMMAND=LadbrokesDesktop BRAND_PLATFORM=ladbrokesDesktop PLATFORM=desktop ENV_PROFILE=${ladbrokes_env_profile} make build_app_all_vanilla")
                                    }
                                }
                            }
                        }
                    }
                    stage("Compodoc") {
                        stages {
                            stage('Compodoc Coral') {
                                when { expression { return "coral" in brands && switchCompodoc } }
                                steps {
                                    script {
                                        lcgAgentDockerExecService(service, containerBuild, "BRAND=coral make compodoc || exit 0")
                                    }
                                }
                            }
                            stage('Compodoc Ladbrokes') {
                                when { expression { return "ladbrokes" in brands && switchCompodoc } }
                                steps {
                                    script {
                                        lcgAgentDockerExecService(service, containerBuild, "BRAND=ladbrokes make compodoc || exit 0")
                                    }
                                }
                            }
                        }

                    }
                    stage('Verification data-crlt attrs') {
                        when { expression { return switchRunTestAttrs } }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make testattrs")
                            }
                        }
                    }
                }
            }
            stage("Deploy") {
                when { expression { return switchDeploy } }
                parallel {
                    stage("WALLET-CORAL-UI-BET-TST1-Build") {
                        steps {
                            timeout(time: 3600, unit: 'SECONDS') {
                                build job: "WALLET-CORAL-UI-BET-TST1-Build",
                                        parameters: [
                                                string(name: "ref_bma", value: branchName),
                                                string(name: "ref_coralsports", value: "develop"),
                                                string(name: "brand", value: "coral"),
                                                string(name: "env_profile", value: "dev0"),
                                                booleanParam(name: "quality_gate", value: false),
                                                booleanParam(name: "clean_ws", value: true)
                                        ]
                            }
                        }
                    }
                    stage("WALLET-LADBROKES-UI-SPORTS-RED-TST1-Build") {
                        steps {
                            timeout(time: 3600, unit: 'SECONDS') {
                                build job: "WALLET-LADBROKES-UI-SPORTS-RED-TST1-Build",
                                        parameters: [
                                                string(name: "ref_bma", value: branchName),
                                                string(name: "ref_coralsports", value: "develop"),
                                                string(name: "brand", value: "ladbrokes"),
                                                string(name: "env_profile", value: "ladbrokes-dev0"),
                                                booleanParam(name: "quality_gate", value: false),
                                                booleanParam(name: "clean_ws", value: true)
                                        ]
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
