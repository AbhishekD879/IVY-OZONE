def call(String agentLabel, String agentDockerImage, List scmRepositories, Map entityService ) {

    pipeline {
        agent {
            docker {
                label agentLabel
                image agentDockerImage
                args "-u root:root"
            }
        }
        parameters {
            string(name: "env_profile", defaultValue: "dev1", description: "Environment profile")
        }

        stages {
            stage('Delete workspase') {
                steps {
                    dir('sources') {
                        deleteDir()
                    }
                }
            }

            stage('Getting SCM sources') {
                steps {
                    script {
                        lcgScmGitParallel(scmRepositories)
                    }
                }
            }

            stage("Bootsrap Docker agent") {
                steps {
                    script {
                        lcgCommonBootstrapDocker()
                    }
                }
            }

            stage("Pre build tasks") {
                steps {
                    script {
                        lcgCommonFunctions.commandSudoShInDir(entityService, "mkdir -pv src/assets/lib")
                    }
                }
            }

            stage('NPM install local') {
                steps {
                    script {
                        lcgCommonFunctions.commandSudoShInDir(entityService, "npm install")
                    }
                }
            }

            stage("NPM install global") {
                steps {
                    script {
                        lcgCommonFunctions.commandSudoShInDir(entityService, "npm install -g @angular/cli")
                        lcgCommonFunctions.commandSudoShInDir(entityService, "npm install -g svg-sprite")
                    }
                }
            }

            stage('TypeScript Lint') {
                steps {
                    script {
                        lcgCommonFunctions.commandSudoShInDir(entityService, "npm run lint")
                    }
                }
            }

            stage('Run Tests') {
                parallel {
                    stage('Unit Tests') {
                        steps {
                            script {
                                lcgCommonFunctions.commandSudoShInDir(entityService, "npm run test")
                            }
                        }
                    }
                    stage('Coverage report') {
                        steps {
                            script {
                                lcgCommonFunctions.commandSudoShInDir(entityService, "npm run coverage-report")
                            }
                        }
                    }
                }
            }

            stage('Build') {
                parallel {
                    stage('Coral - Mobile') {
                        steps {
                            script {
                                lcgCommonFunctions.commandSudoShInDir(entityService, "npm run preBuild --env.environment=${env_profile} --env.platform=mobile")
                                lcgCommonFunctions.commandSudoShInDir(entityService, "ng build coralMobile -c ${env_profile}")
                            }
                        }
                    }
                    stage('Coral - Desktop') {
                        steps {
                            script {
                                lcgCommonFunctions.commandSudoShInDir(entityService, "npm run preBuild --env.environment=${env_profile} --env.platform=desktop")
                                lcgCommonFunctions.commandSudoShInDir(entityService, "ng build coralDesktop -c ${env_profile}")
                            }
                        }
                    }
                }
            }
        }
    }

}
