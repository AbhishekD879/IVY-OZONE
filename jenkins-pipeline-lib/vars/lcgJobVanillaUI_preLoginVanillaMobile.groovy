def call(Map arguments) {

    entityService = arguments.entityService
    primaryAgentLabel = arguments.primaryAgentLabel
    secondaryAgentLabel = arguments.secondaryAgentLabel
    buildUserId = "agulati"

    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(entityService)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(entityService))) : ""
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

    // Switch Fortify Gate
    def switchFotrifyGate = (params.switchFotrifyGate != null) ? params.switchFotrifyGate : false
    println "Check Fortify Gate: ${switchFotrifyGate}"

    // Switch Quality Gate
    def switchQualityGate = (params.quality_gate != null) ? params.quality_gate : true
    println "Check Quality Gate: ${switchQualityGate}"

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true
    println "Post clean up workspace: ${switchPostCleanUpWs}"

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
        parameters {
            string(name: "env_profile", defaultValue: "dev0", description: "Environment profile")
            string(name: "ref_bma", defaultValue: "develop", description: "BMA branch")
        }
        environment {
            BptyMetadata_SCM_BranchName = "${branchName}"
            BUILD_USER_ID = "${buildUserId}"
        }
        stages {
            stage("Sanity workspace") {
                steps {
                    deleteDir()
                }
            }
            stage('Getting SCM sources') {
                steps {
                    script {
                        currentBuild.description = "Branch: ${branchName}"
                        lcgScmGitParallel(repositoriesList)
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
            /*
            stage ("Clean up Packages") {
                steps {
                    script {
                        bat '''
                        RMDIR /S /Q packages
                        '''
                    }
                }
            }
            */
            stage("NPM install") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            bat "npm install --pure-lockfile"
                        }
                    }
                }
            }
            stage("NPM fix-memory-limit") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            bat "npm run fix-memory-limit"
                        }
                    }
                }
            }
            stage("Webpack && Fortify") {
                parallel {
                    stage("NPM Webpack preLoginVanillaMobile") {
                        steps {
                            script {
                                def sources_prelogin_mobile = "sources_preloginmobile"
                                bat """
                                robocopy /S /E ${relativeTargetDir} ${sources_prelogin_mobile}"
                                rem suppress successful robocopy exit statuses, only report genuine errors (bitmask 16 and 8 settings)
                                set/A errlev="%ERRORLEVEL% & 24"
                                exit/B %errlev%
                                """

                                dir(sources_prelogin_mobile) {
                                    bat "npm run preLoginVanillaMobile --env.environment=${params.env_profile}"
                                }

                                bat """
                                robocopy /S /E ${sources_prelogin_mobile}\\build\\Web\\ClientDist\\preLoginVanillaMobile ${relativeTargetDir}\\build\\Web\\ClientDist\\preLoginVanillaMobile
                                set/A errlev="%ERRORLEVEL% & 24"
                                exit/B %errlev%
                                """
                            }
                        }
                    }
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

                                dir(sources_mobile) {
                                    bat "npm run buildMobile --env.environment=${params.env_profile}"
                                }

                                bat """
                                robocopy /S /E ${sources_mobile}\\build\\Web\\ClientDist\\vanillaMobile ${relativeTargetDir}\\build\\Web\\ClientDist\\vanillaMobile
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

                                dir(sources_desktop) {
                                    bat "npm run buildDesktop --env.environment=${params.env_profile}"
                                }

                                bat """
                                robocopy /S /E ${sources_desktop}\\build\\Web\\ClientDist\\vanillaDesktop ${relativeTargetDir}\\build\\Web\\ClientDist\\vanillaDesktop
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
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\MSBuild\\15.0\\Bin\\MSBuild.exe"  /target:Bpty_CleanSolution;Bpty_FetchNuget;Bpty_Fortify_MSBuild /p:Configuration=Debug /p:FortifyTranslateBuildTarget=Bpty_BuildSolution Bpty.Build.proj
echo Fortify
                        '''
                                }
                            }
                        }
                    }
                }
            }
            stage("Build .NET app") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            bat '''
"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\MSBuild\\15.0\\Bin\\MSBuild.exe" @%BPTY_BUILD_ROOT%\\MSBuild40\\MSBuild.rsp /target:Bpty_SetAssemblyInfo;Bpty_FetchNuget;Bpty_BuildSolution;Bpty_WebPackage;Bpty_DismeUpload /p:UserName=%BUILD_USER_ID% /p:OxyVersionInfo=%BUILD_NUMBER% Bpty.Build.proj
'''
                        }
                    }
                }
            }
            stage("Stash artifact") {
                steps {
                    script {
                        dir(relativeTargetDir) {
                            stash includes: 'Frontend.Oxygen.Host/Client/coralsports/**', name: 'artifactSources'
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
