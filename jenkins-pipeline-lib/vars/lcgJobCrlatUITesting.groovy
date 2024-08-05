#!/usr/bin/env groovy

def selenoidHubStatus() {
    sh "ps -aux  | grep selenoid"
    sh "docker ps -a || exit 0"
    sh "docker top selenoid || exit 0"
}

def transformIntoStep(inputString, nodeLabel, Map arguments = [:]) {

    def runtimeImage = arguments.runtimeImage ?: ""
    def dockerImageTag = arguments.dockerImageTag ?: ""
    def mark = arguments.mark ?: ""
    def customMarks = arguments.customMarks ?: ""
    def runOn = arguments.runOn ?: ""
    def pytestTimeOut = arguments.pytestTimeOut ?: ""
    def targetHost = arguments.targetHost ?: ""
    def backEnd = arguments.backEnd ?: ""
    def envTestPath = arguments.envTestPath ?: ""
    def rerunTest = arguments.rerunTest ?: true
    def testrailId = arguments.testrailId ?: ""
    def deviceName =  arguments.deviceName ?: ""
    def branchName =  arguments.branchName ?: ""

    return {
        node(nodeLabel) {
            lcgAwsEcrLogin()
            sh "docker pull ${runtimeImage}:${dockerImageTag}"

            // selenoidHubStatus()

            timeout(time: 120, unit: 'SECONDS') {
                sh '''#!/bin/bash -ex
                SLEEPING=5
                RETRY=24
                CONTAINER=selenoid
                for i in $(seq 1 ${RETRY});
                    do [ "$(docker ps -q -f name=${CONTAINER})" ] && break || sleep ${SLEEPING};
                    echo "waiting for container ${CONTAINER}"
                done
                '''
            }

            // selenoidHubStatus()
            sh """
cat <<EOF > env.list
REMOTE_WD_URL=http://selenoid:4444/wd/hub
MARK=${mark}
TEST_PATH=${envTestPath}
CUSTOM_MARKS=${customMarks}
RUN_ON=${runOn}
PYTEST_TIMEOUT=${pytestTimeOut}
RERUN_TEST=${rerunTest}
TESTRAIL_USER=${TESTRAIL_USER}
TESTRAIL_PASSWD=${TESTRAIL_PASSWD}
TESTRAIL_ID=${testrailId}
OX_HOSTNAME=${targetHost}
GIT_BRANCH=${branchName}
BUILD_NUMBER=${BUILD_NUMBER}
JOB_NAME=${JOB_NAME}
EOF
            """

            sh """
            cat env.list
            MAX_RETRY=2
            RETRY=1
            CUSTOM_EXIT_CODE=86
            EXIT_CODE=86

            COMMAND="docker run --rm --link=selenoid:selenoid \\
            --env-file env.list ${runtimeImage}:${dockerImageTag} py.test ${inputString} \\
            --hostname=${targetHost} -v --junit-xml=results.xml --environment=${backEnd} --device_name=${deviceName}"

            while [ \${EXIT_CODE} -eq \${CUSTOM_EXIT_CODE} ] && [ \${RETRY} -le \${MAX_RETRY} ]
            do
                eval \${COMMAND} && EXIT_CODE="\$?" || EXIT_CODE="\$?"
                RETRY=\$((RETRY+1))
            done

            if [ \$EXIT_CODE -ne 0 ]; then exit 1; fi
            """
        }
    }
}

def call(Map arguments = [:]) {

    // Arguments
    def service = arguments.service ?: lcgCommonFunctions.getConstantsParameters("services.serviceVoltronBmaUiTest")
    def parameterizedCronDef = arguments.parameterizedCronDef ?: ""

    def stepsPerStage = arguments.stepsPerStage ?: 125

    // Job parameters
    def agentLabel = params.node_label ?: "dev-slave-crlat"
    def envTestPath = params.env_test_path ?: "./tests"
    def mark = params.mark ?: "tst2"
    def customMarks = params.custom_marks ?: ""
    def runOn = params.run_on ?: "mobile and desktop"
    def pytestTimeOut = params.pytest_timeout ?: "650"
    def targetHost = params.target_host ?: "bet-tst1.coral.co.uk"
    def backEnd = params.back_end ?: "tst2"
    def rerunTest = (params.rerun_test != null) ? ( params.rerun_test ? "True" : "False" ) : "True"
    def testrailId = params.testrailId ?: ""
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def emailRecipients = (params.email_recipients != null) ? params.email_recipients.trim() : ""
    def switchPostCleanUpWs = (params.clean_ws != null) ? params.clean_ws : true

    // Pipeline variables
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def testrailCredentialsId = service.testrailCredentialsId
    def repositories = [service]
    def ecr = lcgCommonFunctions.getDefaultEcr()
    def runtimeImage = "${ecr}/crlat-voltron-runtime"
    def dockerImageTag = ""
    def imageTagLength = lcgCommonFunctions.getServiceImageTagLength()
    def emailBody = ""

    println "Test parameters:\n================="
    println("Branch: ${branchName}")
    println "Agent Label: ${agentLabel}"
    println "Parameterized Cron: ${parameterizedCronDef}"
    lcgCommonFunctions.prettyPrinter(service, "Service:")

    pipeline {
        agent {
            node {
                label agentLabel
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
            stage("Build runtime Docker image") {
                steps {
                    script {
                        lcgAwsEcrLogin()
                        dockerImageTag = (sh(returnStdout: true, script: "cd ${relativeTargetDir} && ID=\$(git log -1 |" +
                                " grep ^commit | awk '{print \$2}' | cut -c -${imageTagLength}) && echo \${ID}")).trim()
                        service["build_image"] = "${runtimeImage}:${dockerImageTag}"

                        sh """
                        cd ${relativeTargetDir}
                        # find . -name "*.pyc" -execdir rm '{}' \\;
                        docker build --pull -t ${runtimeImage}:${dockerImageTag} .
                        docker push ${runtimeImage}:${dockerImageTag}
                    """
                    }
                }
            }
            stage("Generate Discovery Test File") {
                steps {
                    catchError {
                        script {
                            sh """
cat <<EOF > env.list
TEST_PATH=${envTestPath}
MARK=${mark}
CUSTOM_MARKS=${customMarks}
RUN_ON=${runOn}
TESTRAIL_ID=${testrailId}
GIT_BRANCH=${branchName}
OX_HOSTNAME=${targetHost}
BUILD_NUMBER=${BUILD_NUMBER}
JOB_NAME=${JOB_NAME}
EOF
cat env.list
            """
                            containerDTS = lcgAgentDockerRun(service)
                            lcgAgentDockerBootstrap(containerDTS)
                            lcgAgentDockerExecService(service, containerDTS, "python jenkins_test_discovery.py")
                        }
                    }
                }
                post {
                    always {
                        script {
                            lcgAgentDockerRm(containerDTS)
                        }
                    }
                }
            }
            stage("Generate ID for TESTRAIL") {
                steps {
                    script {
                        withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {
                            sh """
cat <<EOF > env.list
TEST_PATH=${envTestPath}
MARK=${mark}
CUSTOM_MARKS=${customMarks}
RUN_ON=${runOn}
TESTRAIL_USER=${TESTRAIL_USER}
TESTRAIL_PASSWD=${TESTRAIL_PASSWD}
OX_HOSTNAME=${targetHost}
GIT_BRANCH=${branchName}
BUILD_NUMBER=${BUILD_NUMBER}
BUILD_URL=${BUILD_URL}
JOB_NAME=${JOB_NAME}
TESTRAIL_ID=${testrailId}
EOF
            """
                            containerDTS = lcgAgentDockerRun(service)
                            lcgAgentDockerBootstrap(containerDTS)
                            lcgAgentDockerExecService(service, containerDTS, "python scripts/testrail_integration/create_run.py")
                            testrailId = readFile("${relativeTargetDir}/test_run_id.txt")
                        }
                    }
                }
                post {
                    always {
                        script {
                            lcgAgentDockerRm(containerDTS)
                        }
                    }
                }
            }
            stage("Run Mobile") {
                steps {
                    script {
                        withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {

                            def mobileTestsFile = readFile("mobile.txt")
                            List mobileTests = mobileTestsFile.split()
                            def mobileTestsPerStages = lcgCommonFunctions.splitListPerStages(mobileTests, stepsPerStage)
                            lcgCommonFunctions.prettyPrinter(mobileTestsPerStages, "Mobile tests per stages:")
                            def deviceName = "'Galaxy S9'"

                            mobileTestsPerStages.each {
                                stage("Mobile#$it.key") {
                                    catchError {
                                        def stageSteps = it.value
                                        def stepsForParallel = stageSteps.collectEntries {
                                            ["${it}": transformIntoStep(it, agentLabel,
                                                    [
                                                            runtimeImage  : runtimeImage,
                                                            dockerImageTag: dockerImageTag,
                                                            mark          : mark,
                                                            envTestPath   : envTestPath,
                                                            customMarks   : customMarks,
                                                            runOn         : runOn,
                                                            pytestTimeOut : pytestTimeOut,
                                                            targetHost    : targetHost,
                                                            backEnd       : backEnd,
                                                            rerunTest     : rerunTest,
                                                            testrailId    : testrailId,
                                                            deviceName    : deviceName,
                                                            branchName    : branchName
                                                    ]
                                            )
                                            ]
                                        }
                                        parallel stepsForParallel
                                    }
                                }
                            }
                        }
                        echo currentBuild.result
                    }
                }
            }
            stage("Run Desktop") {
                steps {
                    script {
                        withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {

                            def desktopTestsFile = readFile("desktop.txt")
                            List desktopTests = desktopTestsFile.split()
                            def desktopTestsPerStages = lcgCommonFunctions.splitListPerStages(desktopTests, stepsPerStage)
                            lcgCommonFunctions.prettyPrinter(desktopTestsPerStages, "Desktop tests per stages:")
                            def deviceName = "'Desktop Chrome'"

                            desktopTestsPerStages.each {
                                stage("Desktop#$it.key") {
                                    catchError {
                                        def stageSteps = it.value
                                        def stepsForParallel = stageSteps.collectEntries {
                                            ["${it}": transformIntoStep(it, agentLabel,
                                                    [
                                                            runtimeImage  : runtimeImage,
                                                            dockerImageTag: dockerImageTag,
                                                            mark          : mark,
                                                            envTestPath   : envTestPath,
                                                            customMarks   : customMarks,
                                                            runOn         : runOn,
                                                            pytestTimeOut : pytestTimeOut,
                                                            targetHost    : targetHost,
                                                            backEnd       : backEnd,
                                                            rerunTest     : rerunTest,
                                                            testrailId    : testrailId,
                                                            deviceName    : deviceName,
                                                            branchName    : branchName
                                                    ]
                                            )
                                            ]
                                        }
                                        parallel stepsForParallel
                                    }
                                }
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
cat <<EOF > env.list
TEST_PATH=${envTestPath}
MARK=${mark}
CUSTOM_MARKS=${customMarks}
RUN_ON=${runOn}
TESTRAIL_USER=${TESTRAIL_USER}
TESTRAIL_PASSWD=${TESTRAIL_PASSWD}
GIT_BRANCH=${branchName}
BUILD_NUMBER=${BUILD_NUMBER}
JOB_NAME=${JOB_NAME}
EOF
            """
                                containerDTS = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerDTS)
                                lcgAgentDockerExecService(service, containerDTS, "python scripts/testrail_integration/remove_untested_tests.py")
                            }
                            echo currentBuild.result
                        }
                    }
                }
                post {
                    always {
                        script {
                            lcgAgentDockerRm(containerDTS)
                        }
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
cat <<EOF > env.list
TEST_PATH=${envTestPath}
MARK=${mark}
CUSTOM_MARKS=${customMarks}
RUN_ON=${runOn}
TESTRAIL_USER=${TESTRAIL_USER}
TESTRAIL_PASSWD=${TESTRAIL_PASSWD}
GIT_BRANCH=${branchName}
BUILD_NUMBER=${BUILD_NUMBER}
JOB_NAME=${JOB_NAME}
EOF
            """
                                containerDTS = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerDTS)
                                lcgAgentDockerExecService(service, containerDTS, "python scripts/testrail_integration/close_old_runs.py")
                            }
                            echo currentBuild.result
                        }
                    }
                }
                post {
                    always {
                        script {
                            lcgAgentDockerRm(containerDTS)
                        }
                    }
                }
            }
            stage("Generate data for email newsletter and send email") {
                steps {
                    catchError {
                        script {
                            withCredentials([usernamePassword(credentialsId: testrailCredentialsId,
                                    usernameVariable: 'TESTRAIL_USER', passwordVariable: 'TESTRAIL_PASSWD')]) {
                                sh """
cat <<EOF > env.list
TEST_PATH=${envTestPath}
MARK=${mark}
CUSTOM_MARKS=${customMarks}
RUN_ON=${runOn}
OX_HOSTNAME=${targetHost}
TESTRAIL_ID=${testrailId}
TESTRAIL_USER=${TESTRAIL_USER}
TESTRAIL_PASSWD=${TESTRAIL_PASSWD}
GIT_BRANCH=${branchName}
BUILD_NUMBER=${BUILD_NUMBER}
JOB_NAME=${JOB_NAME}
EOF
            """
                                containerDTS = lcgAgentDockerRun(service)
                                lcgAgentDockerBootstrap(containerDTS)
                                lcgAgentDockerExecService(service, containerDTS, "python scripts/testrail_integration/create_data_for_email.py")
                            }
                            if (fileExists('sources/result.txt')) {
                                emailBody = readFile("sources/result.txt")
                            } else {
                                emailBody = "File result.txt doesn't exists"
                            }
                            echo currentBuild.result
                        }
                        emailext body: "${emailBody}\n More info at: ${env.BUILD_URL}",
                                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                                subject: "Run #${env.BUILD_NUMBER} @ ${targetHost} ${env.BUILDVERSION}",
                                to: "${emailRecipients}"
                    }
                }
                post {
                    always {
                        script {
                            lcgAgentDockerRm(containerDTS)
                        }
                    }
                }
            }
        }
//        post {
//            cleanup {
//                script {
//                    if (switchPostCleanUpWs) {
//                        cleanWs()
//                    }
//                }
//            }
//        }
    }
}
