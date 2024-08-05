#!/usr/bin/env groovy

def transformIntoStep(inputString, Map arguments = [:]) {

    def relativeTargetDir = arguments.relativeTargetDir ?: ""
    def customMarks = arguments.customMarks ?: ""
    def targetHost = arguments.targetHost ?: ""
    def backEnd = arguments.backEnd ?: ""

    sh """
cat <<EOF > test.sh
#!/bin/bash
cd ${relativeTargetDir}
source /etc/profile
source /Users/jenkins/PycharmProjects/native_ios_automation/venv/bin/activate
source ../env.list
pytest --hostname=${targetHost} --environment=${backEnd} ${inputString}
EOF
"""
    catchError {
        sh """
        export TESTRAIL_USER=${TESTRAIL_USER}
        export TESTRAIL_PASSWD=${TESTRAIL_PASSWD}
        export TESTRAIL_ID=${testrailId}

        MAX_RETRY=2
        RETRY=1
        CUSTOM_EXIT_CODE=86
        EXIT_CODE=86

        while [ \${EXIT_CODE} -eq \${CUSTOM_EXIT_CODE} ] && [ \${RETRY} -le \${MAX_RETRY} ]
        do
        cat test.sh
        bash test.sh && EXIT_CODE="\$?" || EXIT_CODE="\$?"
            RETRY=\$((RETRY+1))
        done

        if [ \$EXIT_CODE -ne 0 ]; then exit 1; fi
        """
    }
    echo currentBuild.result
}


def call(Map arguments = [:]) {
    def parameterizedCronDef = arguments.parameterizedCronDef ?: ""

    def service = lcgCommonFunctions.getConstantsParameters("services.serviceNativeIosAutomation")
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def nexusCredentialsId = service.nexusCredentialsId
    def testrailCredentialsId = service.testrailCredentialsId

    def runOn = params.run_on ?: "mobile and desktop"
    def mark = params.mark ?: "tst2"
    def customMarks = params.custom_marks ?: ""
    def pytestTimeOut = params.pytest_timeout ?: "650"
    def targetHost = params.target_host ?: "bet-tst1.coral.co.uk"
    def backEnd = params.back_end ?: "tst2"
    def rerunTest = (params.rerun_test != null) ? (params.rerun_test ? "True" : "False") : "True"
    def testrailId = params.testrailId ?: ""
    def emailRecipients = params.email_recipients.trim() ?: ""
    def emailBody = ""
    def locationName = params.locationName ?: "AWS"
    def branchName = params.ref_ios_automation ?: ""
    def brand = params.brand ?: ""
    def testPath = params.test_path ?: "./tests_ios_fully_native_regression"


    def native_ios_repo = lcgCommonFunctions.getConstantsParameters("services.serviceNativeIos")
    def relativeTargetDirNativeIos = lcgCommonFunctions.getGitTargetDirectory(native_ios_repo)
    def repositories = [service, native_ios_repo]

    // Switch clean up workspace
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    println "Test parameters:\n================="
    println("Branch: ${branchName}")
    println "Agent Label: ${node_label}"
    println "Parameterized Cron: ${parameterizedCronDef}"
    lcgCommonFunctions.prettyPrinter(service, "Service:")


    pipeline {
        agent {
            node {
                label node_label
            }
        }
        environment {
            def BUILDVERSION = sh(script: "echo `date`", returnStdout: true)
        }
        options {
            skipDefaultCheckout true
            timestamps()
        }
        triggers {
            parameterizedCron(parameterizedCronDef)
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
                        currentBuild.description = "Target host: ${targetHost}. Branch: ${branchName}"
                        lcgScmGitParallel(repositories, false)
                    }
                }
            }
            stage("Start appium") {
                steps {
                    script {
                        sh """
                        source /etc/profile
                        sudo pkill -f appium 2>/dev/null || true
                        sudo pkill -f xcode 2>/dev/null || true
                        sudo pkill -f Simulator 2>/dev/null || true
                        appium &
                    """
                    }
                }
            }
            stage("install NPM packages") {
                steps {
                    script {
                        withCredentials([usernamePassword(credentialsId: nexusCredentialsId,
                                usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASSWD')]) {
                            sh """
cat <<EOF > env.list
export MARK=${mark}
export CUSTOM_MARKS=${customMarks}
export RUN_ON="${runOn}"
export PYTEST_TIMEOUT=${pytestTimeOut}
export RERUN_TEST=${rerunTest}
export OX_HOSTNAME=${targetHost}
export GIT_BRANCH=${branchName}
export JOB_NAME=${JOB_NAME}
export TESTRAIL_ID=${testrailId}
export BRAND=${brand}
export LOCATION_NAME=${locationName}
export TEST_PATH=${testPath}
source /etc/profile
source /Users/jenkins/PycharmProjects/native_ios_automation/venv/bin/activate
EOF
                  """
                            sh """
                        cd ${relativeTargetDir}
                        source ../env.list
                        export PIP_EXTRA_INDEX_URL=https://\${NEXUS_USER}:\${NEXUS_PASSWD}@npm-repo.coral.co.uk/repository/crlat_pypi/simple
                        pip install -r requirements.txt
                        """
                        }
                    }
                }
            }
            stage("Generate Discovery Test File") {
                steps {
                    script {
                        sh """
                        cd ${relativeTargetDir}
                        source ../env.list
                        python jenkins_test_discovery.py
                        """
                    }
                }
            }
            stage("Generate ID for TESTRAIL") {
                when { expression { return testrailId == "" } }
                steps {
                    script {
                        withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {
                            sh """
                        cd ${relativeTargetDir}
                        export TESTRAIL_USER=\${TESTRAIL_USER}
                        export TESTRAIL_PASSWD=\${TESTRAIL_PASSWD}
                        source ../env.list
                        create_run
                        """
                            testrailId = readFile("${relativeTargetDir}/test_run_id.txt")
                        }
                    }
                }
            }
            stage("Create ios application file") {
                steps {
                    script {
                        sh """
                        cd ${relativeTargetDirNativeIos}
                        source ../env.list
                        ls -lha 
                        fastlane buildForAutomation endpoint:"\${OX_HOSTNAME}" app_path:"/Users/Shared/"
                        """
                    }
                }
            }
            stage("Run Desktop") {
                steps {
                    catchError {
                        script {
                            withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                    usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {

                                def desktopTestsFile = readFile("sources/discovered-tests/native_ios.txt")
                                def desktopTests = desktopTestsFile.split()
                                def stepsForSeparateTests = desktopTests.collectEntries {
                                    ["${it}": transformIntoStep(it,
                                            [
                                                    relativeTargetDir: relativeTargetDir,
                                                    customMarks      : customMarks,
                                                    targetHost       : targetHost,
                                                    backEnd          : backEnd,
                                            ]
                                    )
                                    ]
                                }
                                stepsForSeparateTests
                            }
                        }
                        echo currentBuild.result
                    }
                }
            }
            stage("Remove untested tests") {
                steps {
                    catchError {
                        script {
                            withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                    usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {

                                sh """
                        cd ${relativeTargetDir}
                        source ../env.list
                        export TESTRAIL_USER=\${TESTRAIL_USER}
                        export TESTRAIL_PASSWD=\${TESTRAIL_PASSWD}
                        remove_untested_tests
                        """
                            }
                        }
                        echo currentBuild.result
                    }
                }
            }
            stage("Close old runs") {
                steps {
                    catchError {
                        script {
                            withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                    usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {

                                sh """
                        cd ${relativeTargetDir}
                        source ../env.list
                        export TESTRAIL_USER=\${TESTRAIL_USER}
                        export TESTRAIL_PASSWD=\${TESTRAIL_PASSWD}
                        export TESTRAIL_ID=${testrailId}
                        close_old_runs
                        """
                            }
                        }
                    }
                    echo currentBuild.result
                }
            }
            stage("Generate data for email newsletter") {
                steps {
                    catchError {
                        script {
                            withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                    usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {
                                sh """
                        cd ${relativeTargetDir}
                        source ../env.list
                        export TESTRAIL_USER=\${TESTRAIL_USER}
                        export TESTRAIL_PASSWD=\${TESTRAIL_PASSWD}
                        create_data_for_email
                        """
                            }
                        }
                        echo currentBuild.result
                    }
                }
            }
        }

        post {
            always {
                script {
                    if (fileExists('sources/result.txt')) {
                        emailBody = readFile("sources/result.txt")
                    } else {
                        emailBody = "File result.txt doesn't exists"
                    }
                }
                emailext body: "${emailBody}\n More info at: ${env.BUILD_URL}",
                        recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                        subject: "Run #${env.BUILD_NUMBER} @ ${targetHost} ${env.BUILDVERSION}",
                        to: "${emailRecipients}"
                sh """
                #!/usr/bin/env bash
                sudo pkill -f appium 2>/dev/null || true
                sudo pkill -f xcode 2>/dev/null || true
                sudo pkill -f Simulator 2>/dev/null || true
                """
            }
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
