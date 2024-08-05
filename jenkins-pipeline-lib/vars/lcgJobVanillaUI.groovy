def call(Map arguments) {

    def entityService = arguments.entityService
    def targetEnvs = arguments.targetEnvs ?: []
    def primaryAgentLabel = arguments.primaryAgentLabel
    def secondaryAgentLabel = arguments.secondaryAgentLabel
    def buildUserId = "agulati"
    def teamName = arguments.teamName ?: ""
    def switchDeploy = (arguments.switchDeploy != null) ? arguments.switchDeploy : false
    def switchStartNetContainer = (arguments.switchStartNetContainer !=null) ? arguments.switchStartNetContainer : switchDeploy
    def artifactS3Bucket = arguments.artifactS3Bucket ?: "vanilla-ui-dev"
    def imageTagLength = arguments.imageTagLength ?: lcgCommonFunctions.getServiceImageTagLength()
    def tagId = (params.Container_tag != null) ? params.Container_tag : "poc"
    def sourceJob = (arguments.sourceJob != null) ? (arguments.sourceJob + "_") : ""
    def comandBuildLocal = (arguments.comandBuildLocal != null) ? arguments.comandBuildLocal : false
    def remoteEnv = (params.environment != null) ? params.environment : "qa2"
    def forceProfile = true

    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(entityService))
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(entityService)

    def repositoriesList = [entityService]

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectKey"] = "VANILLA"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectName"] = "VANILLA"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sources"] = "Frontend.Oxygen.Host/Client/coralsports/src/"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.sourceEncoding"] = "UTF-8"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.language"] = "ts"
    commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName

    // Add sourceDir and relativeTargetDir to targetEnv
    targetEnvs.each {
        it.sourceDir = "build/Web/ClientDist"
        it.relativeSourceDir = "./"
    }

    // Brand
    def brand = params.brand ?: "vanilla"
    println "Brand: ${brand}"

    // Set env profile
    def envProfile = params.env_profile
    println "Env profile: ${envProfile}"

    // Switch Fortify Gate
    def switchFotrifyGate = (params.fortify_gate != null) ? params.fortify_gate : false
    println "Check Fortify Gate: ${switchFotrifyGate}"

    // Switch Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true
    println "Check Quality Gate: ${switchQualityGate}"

    // Switch build .NET
    def switchBuildNet = (params.build_net != null) ? params.build_net : false
    println "Build .Net: ${switchBuildNet}"

    // Switch build .NET Docker image
    def switchBuildNetImage = (params.build_net_image != null) ? params.build_net_image : false
    println "Build .Net Docker Image: ${switchBuildNetImage}"

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true
    println "Post clean up workspace: ${switchPostCleanUpWs}"

    println "Deploy: ${switchDeploy}"
    println "Start .Net container: ${switchStartNetContainer}"
    println "Target env: ${targetEnvs}"
    pipeline {
        agent {
            node {
                label primaryAgentLabel
            }
        }
        options {
            skipDefaultCheckout true
            timestamps()
            // disableConcurrentBuilds()
        }
        environment {
            BptyMetadata_SCM_BranchName = "${branchName}"
            BUILD_USER_ID = "${buildUserId}"
        }
        stages {
            stage("Sanity workspace") {
                steps {
                    cleanWs()
                    deleteDir()
                }
            }
            stage('Getting SCM sources') {
                steps {
                    script {
                        currentBuild.description = "Branch: ${branchName} Brand: ${brand}"
                        lcgScmGitParallel(repositoriesList, false)
                    }
                }
            }
            stage("Pull submodules") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            bat """
                            git submodule update --init
                            git submodule foreach git checkout ${params.ref_bma}
                            git submodule foreach git pull
                            """
                        }
                    }
                }
            }
            stage("NPM install") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            bat "node -v"
                            bat "npm config set legacy-peer-deps true"
                            bat "npm install --pure-lockfile"
                        }
                    }
                }
            }
           /* stage("NPM fix-memory-limit") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            bat "npm run fix-memory-limit"
                        }
                    }
                }
            } */
            stage("Webpack && Fortify") {
               parallel {
                   stage("NPM Webpack Mobile") {
                        steps {
                            script {
                                def sources_mobile = "sources_mobile"
                                bat """
                                rem https://weblogs.sqlteam.com/robv/2010/02/17/61106/
                                rem suppress successful robocopy exit statuses, only report genuine errors (bitmask 16 and 8 settings)
                                robocopy /S /E ${relativeTargetDir} ${sources_mobile}
                                set/A errlev="%ERRORLEVEL% & 24"
                                exit/B %errlev%
                                """

                                if (brand in ["coral", "vanilla"]) {
                                    dir(sources_mobile) {
                                        if (comandBuildLocal) {
                                            bat "npm run buildCoralMobileLocal --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                        else
                                        {
                                            bat "npm run buildMobile --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                    }
                                }

                                if (brand in ["ladbrokes"]) {
                                    dir(sources_mobile) {
                                        if (comandBuildLocal) {
                                            bat "npm run buildLadbrokesMobileLocal --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                        else
                                        {
                                            bat "npm run buildLadbrokesMobile --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                    }
                                }

                                bat """
                                robocopy /S /E ${sources_mobile}\\build\\Web\\ClientDist\\${brand}Mobile ${relativeTargetDir}\\build\\Web\\ClientDist\\${brand}Mobile
                                set/A errlev="%ERRORLEVEL% & 24"
                                exit/B %errlev%
                                """
                            }
                        }
                   }
                   stage("NPM Webpack Desktop") {
                        steps {
                            script {
                                def sources_desktop = "sources_desktop"
                                bat """
                                robocopy /S /E ${relativeTargetDir} ${sources_desktop}"
                                rem suppress successful robocopy exit statuses, only report genuine errors (bitmask 16 and 8 settings)
                                set/A errlev="%ERRORLEVEL% & 24"
                                exit/B %errlev%
                                """

                                if (brand in ["coral", "vanilla"]) {
                                    dir(sources_desktop) {
                                        if (comandBuildLocal) {
                                            bat "npm run buildCoralDesktopLocal --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                        else
                                        {
                                            bat "npm run buildDesktop --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                    }
                                }

                                if (brand in ["ladbrokes"]) {
                                    dir(sources_desktop) {
                                        if (comandBuildLocal) {
                                            bat "npm run buildLadbrokesDesktopLocal --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                        else
                                        {
                                            bat "npm run buildLadbrokesDesktop --env.environment=${envProfile} --env.forceProfile=${forceProfile}"
                                        }
                                    }
                                }

                                bat """
                                robocopy /S /E ${sources_desktop}\\build\\Web\\ClientDist\\${brand}Desktop ${relativeTargetDir}\\build\\Web\\ClientDist\\${brand}Desktop
                                set/A errlev="%ERRORLEVEL% & 24"
                                exit/B %errlev%
                                """
                            }
                        }
                    }
                    stage("Fortify") {
                        when { expression { return switchFotrifyGate } }
                        steps {
                            script {
                                dir(relativeTargetDir) {
                                    bat '''
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\MSBuild\\Current\\Bin\\MSBuild.exe"  /target:Bpty_CleanSolution;Bpty_FetchNuget;Bpty_Fortify_MSBuild /p:Configuration=Debug /p:FortifyTranslateBuildTarget=Bpty_BuildSolution Bpty.Build.proj
echo Fortify
                        '''
                                }
                            }
                        }
                    }
                   stage("Build .NET Docker Image") {
                       when { expression { return switchBuildNetImage } }
                       steps {
                           script {
                               tagId = (lcgCommonFunctionsWin.getGitIdCommit(entityService)).take(imageTagLength)
                               currentBuild.description = "Branch: ${branchName} Image: ${tagId}"

                               build job: "IIS-UI-DEV-FRAMEWORK-Build",
                                       parameters: [
                                               string(name: "environment", value: remoteEnv),
                                               string(name: "Commit_base_docker_files", value: "master"),
                                               string(name: "Commit_coralsports", value: "docker_build_targets"),
                                               string(name: "Commit_bpty_build", value: "master"),
                                               string(name: "tag", value: tagId)
                                       ]
                           }
                       }
                   }
               }
            }
            stage("Start .NET container") {
                when { expression { return switchStartNetContainer } }
                steps {
                    script {
                        lcgVanillaUIAdditional.startNetContainer(
                                [
                                        jobName: "IIS-UI-DEV0-FRAMEWORK-Deployment",
                                        commitAnsibleInventories: params.Commit_ansible_inventories,
                                        commitOxygenPlaybook: params.Commit_oxygen_playbook,
                                        containerTag: tagId
                                ],
                                targetEnvs
                        )
                    }
                }
            }
            stage("Build .NET app") {
                when { expression { return switchBuildNet } }
                steps {
                    script {
                        dir(relativeTargetDir) {
                        bat """
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\MSBuild\\Current\\Bin\\MSBuild.exe" -t:Bpty_NugetInstall,Bpty_SetAssemblyInfo -p:Configuration=Publish;InformationalVersion=${brand}_${teamName}_${sourceJob}%BUILD_NUMBER% /p:OxyVersionInfo=${brand}_${teamName}_${sourceJob}%BUILD_NUMBER% Bpty.Build.proj
dotnet publish -c Release --source https://artifactory.bwinparty.corp/artifactory/api/nuget/nuget-public -o Frontend.Oxygen.Host\\bin\\Publish Frontend.CoralSports.sln
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\MSBuild\\Current\\Bin\\MSBuild.exe" -t:Bpty_Package;Bpty_DismeApiUpload -p:Configuration=Publish;InformationalVersion=${brand}_${teamName}_${sourceJob}%BUILD_NUMBER% /p:UserName=%BUILD_USER_ID% /p:OxyVersionInfo=${brand}_${teamName}_${sourceJob}%BUILD_NUMBER% Bpty.Build.proj
"""
                        }
                    }
                }
            }
            stage("Stash artifact") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            stash includes: 'Frontend.Oxygen.Host/Client/coralsports/**', name: 'artifactSources'
                            stash includes: 'build/Web/ClientDist/**', name: 'artifactDist'
                            stash includes: 'node_modules/typescript/**', name: 'artifactNodeModules'
                        }
                    }
                }
            }
            stage("Code Analysis") {
                agent { label secondaryAgentLabel }
                when { expression { return switchQualityGate } }
                steps {
                    script {
                        cleanWs()
                        unstash name: 'artifactSources'
                        unstash name: 'artifactNodeModules'
                        lcgAwsEcrLogin()
                        lcgCodeQuality.sonarCloudPull(commonSonarGate)
                    }
                }
            }
            stage("Deploy") {
                agent { label secondaryAgentLabel }
                when { expression { return switchDeploy } }
                steps {
                    script {
                        cleanWs()
                        unstash name: 'artifactDist'
                        lcgDeploy.deploy(targetEnvs)
                    }
                }
            }
        }
      /*  post {
            cleanup {
                script {
                    if (switchPostCleanUpWs) {
                        cleanWs()
                    }
                }
            }
        } */
    }
}
