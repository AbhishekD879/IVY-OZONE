/*
*
* For Multibranch pipeline strategy
* BRANCH_NAME is defined only in Multibranch job
*
* Test and Build stages in parallel
*
*  13/12/2018
*  Allow multi deployment environments for one brand
*  Add using Makefile from ApplicationBuild repo
*/

/* Example Jenkinsfile

@Library(value='jenkins-pipeline-lib@master', changelog=false)

def agentLabel = "BuildPipelineUI"
def entityService = lcgCommonFunctions.getConstantsParameters('serviceBma')

deployInvictus = lcgCommonFunctions.getDeployDevEnvParameters("envDevInvictus")
deployInvictus["brand"] = "coral"

deployInplay = lcgCommonFunctions.getDeployDevEnvParameters("envDevInplay")
deployInplay["brand"] = "ladbrokes"

lcgJobOxygenUI_v1(agentLabel, entityService, [deployInvictus, deployInplay])

*/

def call(String agentLabel, Map service, List targetEnvs = []) {

    env.VERBOSITY = 3
    def typeJob = "notMultiBranch"
    def branchName = BRANCH_NAME
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)
    def switchSonarCloudPipelineFailed = service.switchSonarCloudPipelineFailed ?: lcgCommonFunctions.getServiceSonarCloudPipelineFailed(service)
    service["branchName"] = branchName
    def logNumToKeep = "5"

    // Configure agentLabel
    // branch develop run on Symphony account
    // other branches run on Framework

    /*
    if (branchName != "develop" && !branchName.matches("^release-(.*)")) {
        agentLabel = "dev-slave"
    }
    *
    * https://jira.egalacoral.com/browse/SDO-5171 force run on dev-slave-ui
    */
    agentLabel = "dev-slave-ui"

    // Allowing concurrent build per branches
    def switchBuildMainRelease = false
    if (branchName.matches("^release-(.*)") || branchName.matches("^develop") || branchName.matches("^SDO-(.*)")) {
        switchBuildMainRelease = true
    }
    println "Agent Label: ${agentLabel}"

    // Configure profiles
    def coral_env_profile = "dev0"
    def ladbrokes_env_profile = "ladbrokes-tst2"
    def vanilla_env_profile = "production"

    if (branchName.matches("^release-(.*)")) {
        coral_env_profile = "ob-tst2"
        ladbrokes_env_profile = "ladbrokes-tst2"
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

    if (branchName.matches("^release-97.0.0")) {
        commonSonarGate["switchSonarCloudPipelineFailed"] = false
    }

    // Build brands list
    def brands = ["coral", "ladbrokes", "vanilla"]

    if (branchName.matches("^release-(.*)")) {
        brands = ["coral", "ladbrokes"]
    }

    //skip build ladbrokes
    if (branchName == "release-97.2.0") {
        brands = ["coral"]
    }

    // Build platform list
    def appPlatform = ["mobile", "desktop"]

    // Switch on/off Quality Gate
    def switchQualityGate = true
    println "Check Quality Gate: " + switchQualityGate

    // Switch EverGreen
    def switchEverGreen = true
    if (params.containsKey("evergreen_build")) {
        if (!params.evergreen_build) {
            switchEverGreen = false
        }
    }
    println "Build EverGreen: " + switchEverGreen

    // Switch on/off clean up workspace in post build action
    def switchPostCleanUpWs = true
    if (params.containsKey("clean_ws")) {
        if (!params.clean_ws) {
            switchPostCleanUpWs = false
        }
    }

    // Switch on/off deploy
    def switchDeploy = true
    if (params.containsKey("deploy")) {
        if (!params.deploy) {
            switchDeploy = false
        }
    }
    // Deploy branches list
    def deployBranches = ["develop"]
    // if ( !( (branchName in deployBranches || branchName.matches("^release-(.*)")) && switchDeploy) ) {
    if (!(branchName in deployBranches && switchDeploy)) {
        switchDeploy = false
    }
    println "Deploy: ${switchDeploy} Branches: ${deployBranches}"

    // Regarding https://jira.egalacoral.com/browse/SDO-4759 force set environment to deploy
    /*
    def deployCoral = lcgCommonFunctions.getConstantsParameters("akamaiCoral.envBetTst1")
    deployCoral["brand"] = "coral"
    def deployLadbrokes = lcgCommonFunctions.getConstantsParameters("akamaiLadbrokes.envSportsRedTst1")
    deployLadbrokes["brand"] = "ladbrokes"
    */
    /*
    if (branchName.matches("^release-(.*)")) {
        deployCoral = lcgCommonFunctions.getConstantsParameters("akamaiCoral.envSportsTst2")
        deployCoral["brand"] = "coral"
        deployLadbrokes = lcgCommonFunctions.getConstantsParameters("akamaiLadbrokes.envSportsRedTst2")
        deployLadbrokes["brand"] = "ladbrokes"
    }
    */

    targetEnvs = []


    // Configure target environment for deployment
    targetEnvs.each {
        it["relativeSourceDir"] = relativeTargetDir
    }
    println "Deploy environments: ${targetEnvs}"

    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    // def repositoriesList = [service, appBuild]
    def repositoriesList = [appBuild]

    // Switch Akamai deploy add set relative dir to Ansible inventories and playbooks
    def switchAkamaiDeploy = false
    if (switchDeploy) {
        switchAkamaiDeploy = lcgDeployAkamai.checkAkamaiDeploy(targetEnvs, repositoriesList)
    }

    println "Akamai deploy: " + switchAkamaiDeploy
    println "Repositories list: " + repositoriesList

    // Generate Compodoc
    def switchCompodoc = (branchName.matches("^develop")) ? true : false
    switchCompodoc = (params.compodoc) ? true : switchCompodoc
    compodocS3Bucket = service.compodocS3Bucket
    compodocS3BucketRegion = service.compodocS3BucketRegion
    println "Compodoc: ${switchCompodoc} compodocS3Bucket: ${compodocS3Bucket} compodocS3Bucket: ${compodocS3Bucket}"

    // Switch on/off verification on data-crlt attributes
    def switchRunTestAttrs= true
    if (params.containsKey("run_test_attrs")) {
        if (!params.run_test_attrs) {
            switchRunTestAttrs = false
        }
    }
    println "Verification data-crlt attributes : ${switchRunTestAttrs}"

    // Switch compression brotli
    def switchCompression = params.compression ?: "brotli"
    println "Compression brotli : ${switchCompression}"

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
                        currentBuild.description = "Branch: ${branchName}, Brand: ${brands.join(', ')}, Profile: ${coral_env_profile}, ${ladbrokes_env_profile}, ${vanilla_env_profile} Platform: ${appPlatform.join(', ')}"
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
            /*
            stage("Stash code") {
                steps {
                    script {
                        stash includes: "${relativeTargetDir}/**", name: "artifactSources"
                    }
                }

            }
            */
            stage("Test and Build") {
                parallel {
                    /*
                    stage("Coverage report and Code Analysis") {
                        agent {
                            node {
                                label agentLabel
                            }
                        }
                        stages {
                            stage("Coverage report") {
                                steps {
                                    script {
                                        cleanWs()
                                        unstash name: "artifactSources"
                                        lcgAwsEcrLogin()
                                        containerCoverage = lcgAgentDockerRun(service)
                                        lcgAgentDockerBootstrap(containerCoverage)
                                        lcgAgentDockerExecService(service, containerCoverage, "make coverage_report")
                                    }
                                }
                            }
                            stage("Code Analysis") {
                                steps {
                                    script {
                                        lcgCodeQuality.sonarCloudPull(commonSonarGate)
                                    }
                                }
                            }
                        }
                        post {
                            always {
                                script {
                                    if (binding.hasVariable("containerCoverage")) {
                                        lcgAgentDockerRm(containerCoverage)
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
                        }
                    }
                    */
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
                                when { expression { return switchQualityGate}}
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
                    stage("Build Coral") {
                        stages {
                            stage('Build Coral Mobile') {
                                when { expression { return "coral" in brands && "mobile" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "1")
                                        lcgAgentDockerExecServiceClone(service, "1", containerBuild, "BRAND_PLATFORM=coralMobile PLATFORM=mobile ENV_PROFILE=${coral_env_profile} make build_app_all")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(service, "1", "dist/coralMobile/*", "dist/coral/mobile/")
                                        if (!("desktop" in appPlatform)) {
                                            sh "cd ${relativeTargetDir} && cp -r dist/coral/mobile/ dist/coral/desktop/"
                                        }

                                    }
                                }
                            }
                            stage('Build Coral Evergreen Mobile') {
                                when { expression { return "coral" in brands && "mobile" in appPlatform && switchEverGreen } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "11")
                                        lcgAgentDockerExecServiceClone(service, "11", containerBuild, "BRAND_PLATFORM=coralEvergreenMobile PLATFORM=mobile ENV_PROFILE=${coral_env_profile} make build_app_all")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(service, "11", "dist/coralEvergreenMobile/*", "dist/coral/evergreenmobile/")
                                    }
                                }
                            }
                            stage('Build Coral Desktop') {
                                when { expression { return "coral" in brands && "desktop" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "2")
                                        lcgAgentDockerExecServiceClone(service, "2", containerBuild, "BRAND_PLATFORM=coralDesktop PLATFORM=desktop ENV_PROFILE=${coral_env_profile} make build_app_all")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(service, "2", "dist/coralDesktop/*", "dist/coral/desktop/")
                                    }
                                }
                            }
                        }
                    }
                    stage("Build Ladbrokes") {
                        stages {
                            stage('Build Ladbrokes Mobile') {
                                when { expression { return "ladbrokes" in brands && "mobile" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "3")
                                        lcgAgentDockerExecServiceClone(service, "3", containerBuild, "BRAND_PLATFORM=ladbrokesMobile PLATFORM=mobile ENV_PROFILE=${ladbrokes_env_profile} make build_app_all")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(service, "3", "dist/ladbrokesMobile/*", "dist/ladbrokes/mobile/")
                                        if (!("desktop" in appPlatform)) {
                                            sh "cd ${relativeTargetDir} && cp -r dist/ladbrokes/mobile/ dist/ladbrokes/desktop/"
                                        }
                                    }
                                }
                            }
                            stage('Build Ladbrokes Evergreen Mobile') {
                                when {
                                    expression { return "ladbrokes" in brands && "mobile" in appPlatform && switchEverGreen }
                                }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "33")
                                        lcgAgentDockerExecServiceClone(service, "33", containerBuild, "BRAND_PLATFORM=ladbrokesEvergreenMobile PLATFORM=mobile ENV_PROFILE=${ladbrokes_env_profile} make build_app_all")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(service, "33", "dist/ladbrokesEvergreenMobile/*", "dist/ladbrokes/evergreenmobile/")
                                    }
                                }
                            }
                            stage('Build Ladbrokes Desktop') {
                                when { expression { return "ladbrokes" in brands && "desktop" in appPlatform } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "4")
                                        lcgAgentDockerExecServiceClone(service, "4", containerBuild, "BRAND_PLATFORM=ladbrokesDesktop PLATFORM=desktop ENV_PROFILE=${ladbrokes_env_profile} make build_app_all")
                                        lcgCommonFunctions.mvCloneDirToSourceDir(service, "4", "dist/ladbrokesDesktop/*", "dist/ladbrokes/desktop/")
                                    }
                                }
                            }
                        }
                    }
                    stage("Build Vanilla") {
                        stages {
                            stage('Build Vanilla Mobile') {
                                when { expression { return "vanilla" in brands && "mobile" in appPlatform && !(branchName in ["roxanne-wallet"]) } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "vanilla_mobile")
                                        lcgAgentDockerExecServiceClone(service, "vanilla_mobile", containerBuild, "BRAND_PLATFORM=vanillaMobile PLATFORM=mobile ENV_PROFILE=${vanilla_env_profile} make build_app_all")
                                    }
                                }
                            }
                            stage('Build Vanilla Desktop') {
                                when { expression { return "vanilla" in brands && "desktop" in appPlatform && !(branchName in ["roxanne-wallet"]) } }
                                steps {
                                    script {
                                        lcgCommonFunctions.cpSourceDirToCloneDir(service, "vanilla_desktop")
                                        lcgAgentDockerExecServiceClone(service, "vanilla_desktop", containerBuild, "BRAND_PLATFORM=vanillaDesktop PLATFORM=desktop ENV_PROFILE=${vanilla_env_profile} make build_app_all")
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
            stage("Post build tasks") {
                stages {
                    stage("Compression Brotli") {
                        when { expression { return switchCompression == "brotli" } }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make compression_brotli")
                            }
                        }
                    }
                    stage("Backup index.html") {
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make backup_index_html")
                            }
                        }
                    }
                    stage("Pre Akamai tasks") {
                        when { expression { return switchAkamaiDeploy } }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make pre_akamai")
                            }
                        }
                    }
                    stage("Upload Compodoc") {
                        when { expression { return switchCompodoc } }
                        steps {
                            script {
                                sh "test -d ${relativeTargetDir}/documentation && aws s3 sync --region ${compodocS3BucketRegion} ${relativeTargetDir}/documentation/ s3://${compodocS3Bucket} --acl public-read --delete || exit 0"
                            }
                        }
                    }
                }
            }
            stage("Deploy") {
                when { expression { return switchDeploy } }
                steps {
                    script {
                        lcgDeploy.deploy(targetEnvs)
                    }
                }
            }
            stage("Post deploy") {
                when { expression { return switchDeploy } }
                steps {
                    script {
                        lcgDeploy.post(targetEnvs)
                    }
                }
            }
            /*
            stage("Build Vanilla") {
                parallel {
                    stage('Build Vanilla Mobile') {
                        when { expression { return "vanilla" in brands && "mobile" in appPlatform} }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "vanilla_mobile")
                                lcgAgentDockerExecServiceClone(service, "vanilla_mobile", containerBuild, "BRAND_PLATFORM=vanillaMobile PLATFORM=mobile ENV_PROFILE=${vanilla_env_profile} make build_app_all")
                            }
                        }
                    }
                    stage('Build Vanilla Desktop') {
                        when { expression { return "vanilla" in brands && "desktop" in appPlatform } }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "vanilla_desktop")
                                lcgAgentDockerExecServiceClone(service, "vanilla_desktop", containerBuild, "BRAND_PLATFORM=vanillaDesktop PLATFORM=desktop ENV_PROFILE=${vanilla_env_profile} make build_app_all")
                            }
                        }
                    }
                }
            }
            */
            stage("UI Testing") {
                when { expression { return switchDeploy } }
                steps {
                    script {
                        lcgTesting.bma(targetEnvs)
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
