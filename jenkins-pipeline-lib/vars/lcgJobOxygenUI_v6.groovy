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
    def ladbrokes_env_profile = arguments.ladbrokes_env_profile ?: "production"
    def logNumToKeep = (arguments.logNumToKeep ?: 5).toString()
    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def vanilla = lcgCommonFunctions.getConstantsParameters("services.serviceBmaVanillaArtifact")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def repositoriesList = [appBuild, vanilla]
    def typeJob = "notMultiBranch"
    def branchName = BRANCH_NAME
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def switchSonarCloudPipelineFailed = service.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    def relativeTargetDirVanilla = lcgCommonFunctions.getGitTargetDirectory(vanilla)
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
    println "Post clean workspace ${switchPostCleanUpWs}"

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

    node {
        currentBuild.displayName = "${branchName}/${currentBuild.number}"
    }
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
            stage("Checkout Vanilla") {
                steps {
                    script {
                        sh """
                            # Checkout Vanilla version
                            VANILLA_VERSION=\$(cat $relativeTargetDir/package.json | jq -r '.\"vanilla-version\"')
                            cd $relativeTargetDirVanilla
                            git checkout \${VANILLA_VERSION}
                            git status
                            cd -
                        """.trim()
                    }
                }
            }
            stage("Pull submodules") {
                steps {
                    script {
                        dir(relativeTargetDirVanilla) {
                            sh """
                            git submodule update --init
                            git submodule foreach git checkout \${GIT_COMMIT}
                            # git submodule foreach git pull
                            """
                        }
                    }
                }
            }
            stage("Set bma project relativeTargetDir") {
                steps {
                    script {
                        relativeTargetDir = relativeTargetDirVanilla + "/Frontend.Oxygen.Host/Client/coralsports"
                        service["relativeTargetDir"] = relativeTargetDir
                        commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir
                    }
                }
            }
            stage("Pre build tasks") {
                steps {
                    script {
                        sh """
                            cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/
                        """.trim()
                    }
                }
            }
            stage("NPM install Vanilla") {
                steps {
                    script {
                        lcgCommonFunctions.setNexusServerProperties(vanilla)
                        lcgAgentDockerExecService(vanilla, containerBuild, "npm cache clean --force &&  npm install --pure-lockfile")
                    }
                }
            }

            stage("Build") {
                parallel {
                    stage("Build Coral-Vanilla Mobile") {
                        stages {
                            stage("Build Coral-Vanilla Mobile") {
                                when { expression { return "coral" in brands && "mobile" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(vanilla, "coral_mobile")
                                        lcgAgentDockerExecServiceClone(vanilla, "coral_mobile", containerBuild, "npm run buildCoralMobileLocal --env.environment=production")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(vanilla, "coral_mobile", "/build/Web/ClientDist/coralMobile/*", "/build/Web/ClientDist/coralMobile")
                                    }
                                }
                            }
                        }
                    }

                    stage("Build Coral-Vanilla Desktop") {
                        stages {
                            stage("Build Coral-Vanilla Desktop") {
                                when { expression { return "coral" in brands && "desktop" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(vanilla, "coral_desktop")
                                        lcgAgentDockerExecServiceClone(vanilla, "coral_desktop", containerBuild, "npm run buildCoralDesktopLocal --env.environment=production")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(vanilla, "coral_desktop", "/build/Web/ClientDist/coralDesktop/*", "/build/Web/ClientDist/coralDesktop")
                                    }
                                }
                            }
                        }
                    }

                    stage("Build Ladbrokes-Vanilla Mobile") {
                        stages {
                            stage("Build Ladbrokes-Vanilla Mobile") {
                                when { expression { return "ladbrokes" in brands && "mobile" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(vanilla, "ladbrokes_mobile")
                                        lcgAgentDockerExecServiceClone(vanilla, "ladbrokes_mobile", containerBuild, "npm run buildLadbrokesMobileLocal --env.environment=production")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(vanilla, "ladbrokes_mobile", "/build/Web/ClientDist/ladbrokesMobile/*", "/build/Web/ClientDist/ladbrokesMobile")
                                    }
                                }
                            }
                        }
                    }

                    stage("Build Ladbrokes-Vanilla Desktop") {
                        stages {
                            stage("Build Ladbrokes-Vanilla Desktop") {
                                when { expression { return "ladbrokes" in brands && "desktop" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(vanilla, "ladbrokes_desktop")
                                        lcgAgentDockerExecServiceClone(vanilla, "ladbrokes_desktop", containerBuild, "npm run buildLadbrokesDesktopLocal --env.environment=production")
                                        sh "ls -la ./vanilla_ladbrokes_desktop//build/Web/ClientDist/ladbrokesDesktop/"
                                        lcgCommonFunctions.mvCloneDirToSourceDir(vanilla, "ladbrokes_desktop", "/build/Web/ClientDist/ladbrokesDesktop/*", "/build/Web/ClientDist/ladbrokesDesktop")
                                    }
                                }
                            }
                        }
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
            stage("ProfileBuilder") {
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "npm run generateBrandProfiles")
                    }
                }
            }
            stage("Budgets") {
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "npm run budgets")
                    }
                }
            }

            stage("Test") {
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

            stage("ZIP and Post") {
                steps {
                    sh """
                        cd vanilla/build/Web/ClientDist
                        zip -r ${currentBuild.number}.zip \$(ls)
                        aws s3 cp \${BUILD_ID}.zip s3://oxygen-coralsports-prod/bma/${branchName}/${currentBuild.number}.zip --acl public-read
                    """
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
                                                string(name: "ref_bma", value: "${branchName}/${currentBuild.number}"),
                                                string(name: "brand", value: "coral"),
                                                string(name: "env_profile", value: "dev0"),
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
                                                string(name: "ref_bma", value: "${branchName}/${currentBuild.number}"),
                                                string(name: "brand", value: "ladbrokes"),
                                                string(name: "env_profile", value: "dev0"),
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
                        println "Cleaning workspace"
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
