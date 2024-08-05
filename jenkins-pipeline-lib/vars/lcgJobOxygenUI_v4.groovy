/*
*
* For Pipeline job strategy
*
*  Init
*  ----
*  Allow multi deployment environments for one brand
*  Add using Makefile from ApplicationBuild repo
*
*  11/22/2018
*  ----------
*  Add select build platform Desktop. Mobile platform build always.
*/

/* Example Jenkinsfile

@Library(value='jenkins-pipeline-lib@master', changelog=false)
def entityService = lcgCommonConstants('serviceBma')
def agentLabel = "BuildPipelineUI"

def envDeployDevInvictus = lcgCommonFunctions.getDeployDevEnvParameters("envDevInvictus")

lcgJobOxygenUI_v4(agentLabel, entityService, [envDeployDevInvictus, envDeployDevInplay, envDeployAkamayInvictus])
 */


/* Example Jenkinsfile for multi environments deploying

@Library(value='jenkins-pipeline-lib@master', changelog=false)
def entityService = lcgCommonConstants('serviceBma')
def agentLabel = "BuildPipelineUI"

def envDeployDevInvictus = lcgCommonFunctions.getDeployDevEnvParameters("envDevInvictus")
def envDeployDevInplay = lcgCommonFunctions.getDeployDevEnvParameters("envDevInplay")
def envDeployAkamayInvictus = lcgCommonFunctions.getDeployDevEnvParameters("envAkamaiInvictus")

lcgJobOxygenUI_v4(agentLabel, entityService, [envDeployDevInvictus, envDeployDevInplay, envDeployAkamayInvictus])
 */

def call(String agentLabel, Map service, List targetEnvs) {

    env.VERBOSITY = 3
    def branchName = env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service)) != null ?
            lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(service))) : ""
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def applicationBuildDir = lcgCommonFunctions.getServiceAppDir(service)

    // Set Sonar Cloud parameters
    def commonSonarGate = lcgCommonFunctions.getConstantsParameters("common.sonarCloud")
    commonSonarGate["parametersSonarCloud"]["-Dsonar.projectBaseDir"] = "./" + relativeTargetDir
    commonSonarGate["parametersSonarCloud"]["-Dsonar.branch.name"] = branchName

    /*
    *   Set brands list and env_profile
    *   In order to support compatibility and reuse 'stage ("Test and Build")' between Multibranch and Pipeline type of jobs
    */
    def brands = []
    if (params.brand) {
        brands.add(params.brand)

        targetEnvs.each {
            it["brand"] = params.brand
            it["relativeSourceDir"] = relativeTargetDir
        }
    }
    if (params.env_profile) {
        coral_env_profile = env_profile
        ladbrokes_env_profile = env_profile
        vanilla_env_profile = env_profile
    }

    // Build platform list
    def appPlatform = ["mobile", "desktop"]
    if (params.platform_desktop == false) {
        appPlatform.remove(1)
    }
    println "Platforms to build: " +  appPlatform

    // Switch Quality Gate
    def switchQualityGate = true
    if (params.containsKey("quality_gate")) {
        if (!params.quality_gate) {
            switchQualityGate = false
        }
    }
    println "Check Quality Gate: " +  switchQualityGate

    // Fortify
    // parameter: name: "fortify_scan"
    // choices: ["none", "fortify_simple_scan", "fortify_scan_upload_reports"]
    // description: "Please choose fortify type"
    def switchFortifyScan = null
    if (params.containsKey("fortify_scan")) {
        switchFortifyScan = params.fortify_scan
    }
    println "Fortify Scan: ${switchFortifyScan}"

    // Switch EverGreen
    def switchEverGreen = false
    if (params.containsKey("evergreen_build")) {
        if (params.evergreen_build) {
            switchEverGreen = true
        }
    }
    println "Build EverGreen: " +  switchEverGreen

    // Switch on/off clean up workspace in post build action
    def switchPostCleanUpWs = true
    if (params.containsKey("clean_ws")) {
        if (!params.clean_ws) {
            switchPostCleanUpWs = false
        }
    }
    println "Post clean up workspace: " + switchPostCleanUpWs

    // Switch on/off run tests (coverage report, type script)
    def switchRunTests = true
    if (params.containsKey("tests_run")) {
        if (!params.tests_run) {
            switchRunTests = false
        }
    }
    println "Run tests: " + switchRunTests

    // Switch on/off deploy
    def switchDeploy = "vanilla" in brands ? false : true
    if (params.containsKey("deploy")) {
        if (!params.deploy) {
            switchDeploy = false
        }
    }
    // Deploy branches list
    def deployBranches = [branchName]
    if ( !(branchName in deployBranches && switchDeploy) ) {
        switchDeploy = false
    }
    println "Deploy: ${switchDeploy} Branches: ${deployBranches}"

    def appBuild = lcgCommonFunctions.getConstantsParameters("common.repoApplicationBuild")
    def relativeTargetDirAppBuild = lcgCommonFunctions.getGitTargetDirectory(appBuild)
    def repositoriesList = [service, appBuild]

    // Switch Akamai deploy add set relative dir to Ansible inventories and playbooks
    def switchAkamaiDeploy = lcgDeployAkamai.checkAkamaiDeploy(targetEnvs, repositoriesList)

    println "Akamai deploy: " +  switchAkamaiDeploy
    println "Repositories list: " +  repositoriesList

    // Generate Compodoc
    // def switchCompodoc = (branchName.matches("^develop")) ? true : false
    def switchCompodoc = false
    // switchCompodoc = (params.compodoc) ? true : switchCompodoc
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

    def switchEmail = false
    def recipientsList = ""
    def deployEnv = ""
    targetEnvs.each {
        if (it.envLevel in ["hlv0"]) {
            switchEmail = true
            recipientsList = "lcl.leads@ladbrokescoral.com"
            deployEnv = it.envLevel
        }
        if (it.envLevel in ["prd0", "prod"]) {
            switchEmail = true
            recipientsList = "lcl.leads@ladbrokescoral.com,coral-devops@symphony-solutions.eu,support.operation.coral@symphony-solutions.eu"
            deployEnv = it.envLevel
        }
    }
    println "Send Email: ${switchEmail} Recipients: ${recipientsList}"

    pipeline {
        agent {
            node {
                label agentLabel
            }
        }
        options {
            skipDefaultCheckout true
            timestamps()
            disableConcurrentBuilds()
            timeout(time: 120, unit: 'MINUTES')
        }
        stages {
            stage ("Sanity workspace") {
                steps {
                    deleteDir()
                }
            }
            stage ('Getting SCM sources') {
                steps {
                    script {
                        currentBuild.description = "Branch: ${branchName}, Brand: ${brands.join(', ')}, Profile: ${params.env_profile}, Platform: ${appPlatform.join(', ')}"
                        lcgScmGitParallel(repositoriesList)
                    }
                }
            }
            stage ("Fortify simple scan") {
                when { expression { return switchFortifyScan == "fortify_simple_scan" } }
                steps {
                    script {
                        lcgAwsEcrLogin()
                        lcgCodeQualityFortify(lcgCommonFunctions.getConstantsParameters("common.fortify"), relativeTargetDir)
                    }
                }
            }
            stage ("Fortify upload reports ") {
                when { expression { return switchFortifyScan == "fortify_scan_upload_reports" } }
                steps {
                    script {
                        lcgAwsEcrLogin()
                        lcgCodeQualityFortify(lcgCommonFunctions.getConstantsParameters("common.fortify"), relativeTargetDir, "upload_reports")
                    }
                }
            }
            stage ("Start Docker Build Container") {
                steps {
                    script {
                        lcgAwsEcrLogin()
                        containerBuild = lcgAgentDockerRun(service)
                        lcgAgentDockerBootstrap(containerBuild)
                    }
                }
            }
            stage ("Pre build tasks") {
                steps {
                    script {
                        sh "cp -v ${relativeTargetDirAppBuild}/${applicationBuildDir}/Makefile ${relativeTargetDir}/"
                        lcgCommonFunctions.setNexusServerProperties(service)
                        lcgAgentDockerExecService(service, containerBuild, "make pre_build_tasks")
                    }
                }
            }
            stage ("NPM install global") {
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "make npm_install_global")
                    }
                }
            }
            stage ("NPM install local") {
                steps {
                    script {
                        lcgAgentDockerExecService(service, containerBuild, "make npm_install_local")
                    }
                }
            }
            stage('Generate Coral SVG') {
                when { expression { return "coral" in brands }}
                    steps {
                        script {
                            lcgAgentDockerExecService(service, containerBuild, "BRAND=coral make generate_svg")
                        }
                    }
            }
            stage('Generate Ladbrokes SVG') {
                when { expression { return "ladbrokes" in brands }}
                     steps {
                        script {
                            lcgAgentDockerExecService(service, containerBuild, "BRAND=ladbrokes make generate_svg")
                        }
                     }
            }
            stage ("Test and Build") {
                parallel {
                    stage('Coverage report') {
                        when { expression { return switchRunTests } }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make coverage_report")
                            }
                        }
                    }
                    stage ("TypeScript Lint") {
                        when { expression { return switchRunTests } }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make lint")
                            }
                        }
                    }
                    stage('Build Coral Mobile') {
                        when { expression { return "coral" in brands && "mobile" in appPlatform} }
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
                        when { expression { return "coral" in brands && "mobile" in appPlatform  && switchEverGreen} }
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
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "111")
                                lcgAgentDockerExecServiceClone(service, "111", containerBuild, "BRAND_PLATFORM=coralDesktop PLATFORM=desktop ENV_PROFILE=${coral_env_profile} make build_app_all")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "111", "dist/coralDesktop/*", "dist/coral/desktop/")
                            }
                        }
                    }
                    stage('Compodoc Coral') {
                        when { expression { return "coral" in brands && switchCompodoc} }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "BRAND=coral make compodoc || exit 0")
                            }
                        }
                    }
                    stage('Build Ladbrokes Mobile') {
                        when { expression { return "ladbrokes" in brands && "mobile" in appPlatform} }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "2")
                                lcgAgentDockerExecServiceClone(service, "2", containerBuild, "BRAND_PLATFORM=ladbrokesMobile PLATFORM=mobile ENV_PROFILE=${ladbrokes_env_profile} make build_app_all")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "2", "dist/ladbrokesMobile/*", "dist/ladbrokes/mobile/")
                                if (!("desktop" in appPlatform)) {
                                    sh "cd ${relativeTargetDir} && cp -r dist/ladbrokes/mobile/ dist/ladbrokes/desktop/"
                                }
                            }
                        }
                    }
                    stage('Build Ladbrokes Evergreen Mobile') {
                        when { expression { return "ladbrokes" in brands && "mobile" in appPlatform && switchEverGreen } }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "22")
                                lcgAgentDockerExecServiceClone(service, "22", containerBuild, "BRAND_PLATFORM=ladbrokesEvergreenMobile PLATFORM=mobile ENV_PROFILE=${ladbrokes_env_profile} make build_app_all")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "22", "dist/ladbrokesEvergreenMobile/*", "dist/ladbrokes/evergreenmobile/")
                            }
                        }
                    }
                    stage('Build Ladbrokes Desktop') {
                        when { expression { return "ladbrokes" in brands && "desktop" in appPlatform} }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "222")
                                lcgAgentDockerExecServiceClone(service, "222", containerBuild, "BRAND_PLATFORM=ladbrokesDesktop PLATFORM=desktop ENV_PROFILE=${ladbrokes_env_profile} make build_app_all")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "222", "dist/ladbrokesDesktop/*", "dist/ladbrokes/desktop/")
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
                    stage('Verification data-crlt attrs') {
                        when { expression { return switchRunTestAttrs } }
                        steps {
                            script {
                                lcgAgentDockerExecService(service, containerBuild, "make testattrs")
                            }
                        }
                    }
                    stage('Build Vanilla Mobile') {
                        when { expression { return "vanilla" in brands && "mobile" in appPlatform} }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "3")
                                lcgAgentDockerExecServiceClone(service, "3", containerBuild, "BRAND_PLATFORM=vanillaMobile PLATFORM=mobile ENV_PROFILE=${vanilla_env_profile} make build_app_all")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "3", "dist/vanillaMobile/*", "dist/vanilla/mobile/")
                                if (!("desktop" in appPlatform)) {
                                    sh "cd ${relativeTargetDir} && cp -r dist/vanilla/mobile/ dist/vanilla/desktop/"
                                }
                            }
                        }
                    }
                    stage('Build Vanilla Desktop') {
                        when { expression { return "vanilla" in brands && "desktop" in appPlatform } }
                        steps {
                            script {
                                lcgCommonFunctions.cpSourceDirToCloneDir(service, "333")
                                lcgAgentDockerExecServiceClone(service, "333", containerBuild, "BRAND_PLATFORM=vanillaDesktop PLATFORM=desktop ENV_PROFILE=${vanilla_env_profile} make build_app_all")
                                lcgCommonFunctions.mvCloneDirToSourceDir(service, "333", "dist/vanillaDesktop/*", "dist/vanilla/desktop/")
                            }
                        }
                    }
                }
            }
            stage ("Code Analysis") {
                when { expression { return switchQualityGate}}
                steps {
                    script {
                        lcgCodeQuality.sonarCloudPull(commonSonarGate)
                    }
                }
            }
            stage ("Post build tasks") {
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
            stage ("Deploy") {
                when { expression { return switchDeploy } }
                steps {
                    script {
                        lcgDeploy.deploy(targetEnvs)
                    }
                }
            }
            stage ("Post deploy") {
                when { expression { return switchDeploy } }
                steps {
                    script {
                        lcgDeploy.post(targetEnvs)
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
            success {
                script {
                    if (switchEmail) {
                        lcgNotify.notifySuccessful([recipientsList: recipientsList, deployEnv: deployEnv])
                    }
                }
            }
            aborted {
                    script {
                        lcgNotify.notifyAborted([recipientsList: recipientsList, deployEnv: deployEnv])
                    }
            }
            failure {
                    script {
                        lcgNotify.notifyFailed([recipientsList: recipientsList, deployEnv: deployEnv])
                    }
            }
        }
    }
}
