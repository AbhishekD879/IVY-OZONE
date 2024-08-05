def call() {

    def constants = [
            services: [
                    serviceTimeform         : [
                            // git repository parameters
                            "stageName"                : "Getting Timeform sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/timeform.git",
                            "branch_default"           : "dev",
                            "job_parameter_description": "Timeform sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "credentialsId"            : "gitBitBucketKey",
                            // Deploy parameters
                            "env"                      : "",
                            "repoInventories"          : "commonRepoAnsibleInventories",
                            "repoPlaybooks"            : "commonRepoOxygenPlaybook",
                            "playbook"                 : "timeform-bg.yml",
                            "hosts"                    : "timeform",
                            "extraVars"                : "",
                            "service_image_tag_name"   : "timeform_tag",
                            "service_image_tag"        : ""
                    ],
                    serviceBma              : [
                            // git repository parameters
                            "stageName"                   : "Getting BMA sources",
                            "url"                         : "git@bitbucket.org:symphonydevelopers/bma.git",
                            "branch_default"              : "develop",
                            "job_parameter_description"   : "BMA sources branch/commit/tag name",
                            "relativeTargetDir"           : "sources",
                            "applicationBuildDir"         : "bma",           // Directory in Application Build repository
                            "credentialsId"               : "gitDeploymentKey",
                            "nexusServer"                 : "artifactoryGvc",
                            // Build parameters
                            "build_image"                 : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:10.21.0.0",
                            "buildEnvVars"                : ["NODE_OPTIONS": "--max_old_space_size=10240"],
                            "compodocS3Bucket"            : "lcg-bma-compodoc",
                            "compodocS3BucketRegion"      : "eu-west-2",
                            switchSonarCloudPipelineFailed: true
                    ],
                    serviceBmaVanillaArtifact       : [
                            // git repository parameters
                            "stageName"                : "Getting BMA Vanilla sources",
                            "url"                      : "git@lcg.git.bwinparty.corp:agulati/coralsports.git",
                            "branch_default"           : "develop",
                            "job_parameter_description": "BMA Vanilla sources branch/commit/tag name",
                            "relativeTargetDir"        : "vanilla",
                            "credentialsId"            : "gitDeploymentKey",
                            "nexusServer"              : "artifactoryGvc",
                            // Build parameters
                            "build_image"              : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:10.21.0.0",
                            "buildEnvVars"             : ["NODE_OPTIONS": "--max_old_space_size=10240"],
                    ],
                    serviceBmaVanilla       : [
                            // git repository parameters
                            "stageName"                : "Getting BMA Vanilla sources",
                            "url"                      : "git@lcg.git.bwinparty.corp:agulati/coralsports.git",
                            "branch_default"           : "develop",
                            "job_parameter_description": "BMA Vanilla sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "credentialsId"            : "gitDeploymentKey",
                            "nexusServer"              : "artifactoryGvc",
                            // Build parameters
                            "build_image"              : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:8.9.4.3",
                            "buildEnvVars"             : ["NODE_OPTIONS": "--max_old_space_size=10240"],
                    ],
                    serviceVoltronCrlatObLoad : [
                            // git repository parameters
                            "stageName"                : "Getting Voltron Crlat Ob Load sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/crlat_ob_load.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "Voltron Crlat Ob Load sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "credentialsId"            : "gitBitBucketKey",
                            "nexusCredentialsId"       : "dev_read_nexus"
                    ],
                    serviceVoltronBmaUiTest : [
                            // git repository parameters
                            "stageName"                : "Getting Voltron BMA UI Test sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/voltron.git",
                            "branch_default"           : "invictus",
                            "job_parameter_description": "Voltron BMA UI Test sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "credentialsId"            : "gitBitBucketKey",
                            "nexusCredentialsId"       : "dev_read_nexus",
                            "testrailCredentialsId"    : "testrail_voltron",
                            // Build parameters
                            "build_image"              : "",
                            "buildEnvVars"             : ["DISCOVERY_DIR": "/opt/workDir/", "ACCOUNTS_SHARING": "https://accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com"],
                            "buildEnvVarsFile"         : "env.list"
                    ],
                    serviceLcgUatBmaUiTest : [
                            // git repository parameters
                            "stageName"                : "Getting LCG UAT BMA UI Test sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/lcg_uat.git",
                            "branch_default"           : "invictus",
                            "job_parameter_description": "Voltron BMA UI Test sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "credentialsId"            : "gitBitBucketKey",
                            "nexusCredentialsId"       : "dev_read_nexus",
                            "testrailCredentialsId"    : "testrail_voltron",
                            // Build parameters
                            "build_image"              : "",
                            // "buildImage"               : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/crlat_py3_remote_wd_cli:latest",
                            "buildEnvVars"             : ["DISCOVERY_DIR": "/opt/workDir/", "ACCOUNTS_SHARING": "https://accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com"],
                            "buildEnvVarsFile"         : "env.list"
                    ],
                    serviceOtfUI            : [
                            // git repository parameters
                            "stageName"                : "Getting OTF sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/one-two-free-ui.git",
                            "branch_default"           : "develop",
                            "job_parameter_description": "One Two Free UI sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "sourcesDir"               : "build",
                            "applicationBuildDir"      : "otf-ui",
                            "credentialsId"            : "gitDeploymentKey",
                            "nexusServer"              : "nexusServerOnprem",
                            "cloudFlareApiTokenId"     : "9ad48c1f-32dc-42ef-ba9c-dffcb3f0c3a55",
                            // Build parameters
                            "build_image"              : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/alpine-build-nodejs:8.9.3"
                    ],
                    serviceBmaAndroidWrapper: [
                            // git repository parameters
                            "stageName"                     : "Getting BMA Android Wrapper sources",
                            "url"                           : "git@bitbucket.org:symphonydevelopers/bma-androidwrapper.git",
                            "branch_default"                : "develop",
                            "job_parameter_description"     : "BMA Android Wrapper sources branch/commit/tag name",
                            "relativeTargetDir"             : "sources",
                            "applicationBuildDir"           : "bma-androidwrapper",
                            "credentialsId"                 : "gitBitBucketKey",
                            // Build parameters
                            "build_image"                   : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/android-sdk:6609375",
                            "switchSonarCloudPipelineFailed": false  // abort pipeline when SonarCloud return ERROR for quality code
                    ],
                    buildVoltronFlake8      : [
                            stageName              : "Getting Voltron sources",
                            url                    : "git@bitbucket.org:symphonydevelopers/mz_pipeline_test.git",
                            branchDefault          : "invictus",
                            jobParameterDescription: "Voltron branch/commit/tag name",
                            relativeTargetDir      : "sources",
                            credentialsId          : "gitBitBucketKey",
                            nexusCredentialsId     : "dev_read_nexus",
                            buildImage             : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/crlat-voltron-base:3.6.8.5",
                            buildEnvVars           : ["NEXUS_USER": '${NEXUS_USER}', "NEXUS_PASS": '${NEXUS_PASS}', "LOCATION_NAME": "AWS"]
                    ],
                    serviceLiveServAPI      : [
                            // git repository parameters
                            "stageName"                     : "Getting LiveServ API sources",
                            "url"                           : "git@bitbucket.org:symphonydevelopers/liveserv-api.git",
                            "branch_default"                : "master",
                            "job_parameter_description"     : "LiveServ API sources branch/commit/tag name",
                            "relativeTargetDir"             : "sources",
                            "credentialsId"                 : "gitBitBucketKey",
                            "nexusServer"                   : "nexusServerOnprem",
                            // Build parameters
                            "build_image"                   : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/openjdk-debian-gradle:8.131.2",
                            "switchSonarCloudPipelineFailed": false  // abort pipeline when SonarCloud return ERROR for quality code
                    ],
                    serviceCmsApi           : [
                            stageName                     : "Getting CMS API sources",
                            url                           : "git@bitbucket.org:symphonydevelopers/oxygen-cms-api.git",
                            runtimeImage                  : "cms-api",
                            branch_default                : "develop",
                            deployAnsiblePlaybook         : "cms-api-bg.yml",
                            deployAnsibleHostsLimit       : "cms-api",
                            deployExtraVars               : [:],
                            deployServiceTag              : "cms_api_tag",
                            multiBranchAutodeploy         : [
                                    [
                                            branches      : ["develop"],
                                            targetEnvsList: ["awsCoral.dev0"]
                                    ]
                            ],
                            job_parameter_description     : "CMS API sources branch/commit/tag name",
                            relativeTargetDir             : "sources",
                            applicationBuildDir           : "cms-api",           // Directory in Application Build repository
                            credentialsId                 : "gitDeploymentKey",
                            nexusServer                   : "nexusServerOnprem",
                            nexusCredentialsId            : "dev_read_nexus",
                            // SonarCloud
                            sonarScannerDockerSkip        : true,  // on/off Sonar Scanner in Docker version
                            sonarScannerGradleSkip        : false, // on/off Sonar Scanner in Gradle project
                            switchSonarCloudPipelineFailed: false, // abort pipeline when SonarCloud return ERROR for quality code
                            projectKeySonarCloud          : "symphonydevelopers_oxygen-cms-api",
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/openjdk-debian-gradle:8.131.3-node-jdk11",
                            buildEnvVars                  : ["NEXUS_USER": '${NEXUS_USER}', "NEXUS_PASS": '${NEXUS_PASS}']
                    ],
                    serviceCmsUi            : [
                            stageName                     : "Getting CMS UI sources",
                            url                           : "git@bitbucket.org:symphonydevelopers/oxygen-cms-ui.git",
                            branch_default                : "develop",
                            multiBranchAutodeploy         : [
                                    [
                                            branches      : ["develop"],
                                            targetEnvsList: ["awsCoralCloudFront.cmsUi.dev0"]
                                    ]
                            ],
                            job_parameter_description     : "CMS UI sources branch/commit/tag name",
                            relativeTargetDir             : "sources",
                            sourcesDir                    : "dist",
                            applicationBuildDir           : "cms-ui",           // Directory in Application Build repository
                            credentialsId                 : "gitDeploymentKey",
                            nexusServer                   : "nexusServerOnprem",
                            switchSonarCloudPipelineFailed: false,
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:12.18.2.1"
                    ],
                    serviceSdmFrontend      : [
                            // git repository parameters
                            stageName                     : "Getting SDM Frontend sources",
                            url                           : "git@bitbucket.org:symphonydevelopers/sdm-frontend.git",
                            branch_default                : "master",
                            job_parameter_description     : "SDM Frontend sources branch/commit/tag name",
                            relativeTargetDir             : "sources",
                            credentialsId                 : "gitBitBucketKey",
                            nexusServer                   : "nexusServerOnprem",
                            applicationBuildDir           : "sdm-frontend",           // Directory in Application Build repository
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/build-node-chrome:8.16.2.1",
                            switchSonarCloudPipelineFailed: false  // abort pipeline when SonarCloud return ERROR for quality code
                    ],
                    serviceSdmFrontendApp   : [
                            // git repository parameters
                            stageName                : "Getting SDM Frontend App",
                            url                      : "git@bitbucket.org:symphonydevelopers/sdm-frontend-app.git",
                            branch_default           : "master",
                            job_parameter_description: "SDM Frontend sources branch/commit/tag name",
                            relativeTargetDir        : "app",
                            sourcesDir               : "dist",
                            credentialsId            : "gitBitBucketKey",
                            nexusServer              : "nexusServerOnprem",
                            // Build parameters
                            buildImage               : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/alpine-build-nodejs:\${NODE_VERSION}",
                            buildEnvVars             : ["CONTEXT": '${CONTEXT}']
                    ],
                    serviceSdmFrontendTests : [
                            // git repository parameters
                            stageName                     : "Getting SDM Frontend Tests",
                            url                           : "git@bitbucket.org:symphonydevelopers/sdm-tests.git",
                            branch_default                : "master",
                            job_parameter_description     : "SDM Frontend sources branch/commit/tag name",
                            relativeTargetDir             : "tests",
                            credentialsId                 : "gitBitBucketKey",
                            nexusServer                   : "nexusServerOnprem",
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/selenium-gradle-chrome:3.141.59.2",
                            switchSonarCloudPipelineFailed: false,  // abort pipeline when SonarCloud return ERROR for quality code
                            buildEnvVars                  : ["CONTEXT": '${CONTEXT}']
                    ],
                    serviceOptinApi         : [
                            stageName                     : "Getting OPTIN API sources",
                            url                           : "git@bitbucket.org:symphonydevelopers/oxygen-settings-api.git",
                            runtimeImage                  : "oxygen-settings-api",
                            branchDefault                 : "develop",
                            jobParameterDescription       : "OPTIN API sources branch/commit/tag name",
                            relativeTargetDir             : "sources",
                            applicationBuildDir           : "oxygen-settings-api", // directory in Application Build repository
                            credentialsId                 : "gitDeploymentKey",
                            autoDeployBranchesList        : ["develop"],
                            nexusCredentialsId            : "dev_read_nexus",
                            // SonarCloud
                            sonarScannerDockerSkip        : true,  // on/off Sonar Scanner in Docker version
                            sonarScannerGradleSkip        : false, // on/off Sonar Scanner in Gradle project
                            switchSonarCloudPipelineFailed: false, // abort pipeline when SonarCloud return ERROR for quality code
                            projectKeySonarCloud          : "symphonydevelopers_oxygen-settings-api",
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/openjdk-debian-gradle:8.131.3-jdk11",
                            buildEnvVars                  : ["NEXUS_USER": '${NEXUS_USER}', "NEXUS_PASS": '${NEXUS_PASS}']
                    ],
                    serviceCashoutApi         : [
                            stageName                     : "Getting Cashout API sources",
                            url                           : "git@bitbucket.org:symphonydevelopers/cashout.git",
                            runtimeImage                  : "cashout",
                            branchDefault                 : "develop",
                            jobParameterDescription       : "Cashout API sources branch/commit/tag name",
                            relativeTargetDir             : "sources",
                            applicationBuildDir           : "cashout", // directory in Application Build repository
                            credentialsId                 : "gitDeploymentKey",
                            autoDeployBranchesList        : ["develop"],
                            nexusCredentialsId            : "dev_read_nexus",
                            // SonarCloud
                            sonarScannerDockerSkip        : true,  // on/off Sonar Scanner in Docker version
                            sonarScannerGradleSkip        : false, // on/off Sonar Scanner in Gradle project
                            switchSonarCloudPipelineFailed: false, // abort pipeline when SonarCloud return ERROR for quality code
                            projectKeySonarCloud          : "symphonydevelopers_cashout",
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/openjdk-debian-gradle:8.131.3-jdk11",
                            buildEnvVars                  : ["NEXUS_USER": '${NEXUS_USER}', "NEXUS_PASS": '${NEXUS_PASS}']
                    ],
                    serviceIos              : [
                            stageName                              : "Getting OXYGEN IOS sources",
                            url                                    : "git@bitbucket.org:symphonydevelopers/oxygen-ios.git",
                            branchDefault                          : "develop",
                            jobParameterDescription                : "NATIVE IOS sources branch/commit/tag name",
                            relativeTargetDir                      : "sources",
                            credentialsId                          : "gitDeploymentKey",
                            fastlaneKeychainPassword               : "ab7fc783-f9dc-4d90-8915-194dceaae2f7",
                            fastlaneLoginKeychainPassword          : "50755a42-07e9-4ccd-9e10-bc5679c91104",
                            fastlaneDistributionCertificatePassword: "b0a81ed5-faa3-4b59-9bc5-e23cc9f8b883",
                            fastlaneDevelopmentCertificatePassword : "751acc91-f1f1-4b43-ba0f-d403e62c11e2",
                            iosNativeGitUsernamePassword           : "94f23018-1507-4685-9d98-6890a3f0819c",
                            fastlaneDefaultCommand                 : "CoralUploadDebugBuildToTestFairy",
                            // SonarCloud
                            switchSonarCloudPipelineFailed         : false, // abort pipeline when SonarCloud return ERROR for quality code
                            sonarScannerDockerSkip                 : true,  // on/off Sonar Scanner in Docker version
                            fastlaneSonarCommand                   : "jenkinsSonarScaner",
                            projectKeySonarCloud                   : "symphonydevelopers_oxygen-ios"
                    ],
                    serviceBetPlacement         : [
                            stageName                     : "Getting BetPlacement sources",
                            url                           : "git@bitbucket.org:symphonydevelopers/pirozhok-api.git",
                            runtimeImage                  : "bet-placement",
                            branchDefault                 : "develop",
                            jobParameterDescription       : "BetPlacement sources branch/commit/tag name",
                            relativeTargetDir             : "sources",
                            applicationBuildDir           : "bet-placement", // directory in Application Build repository
                            credentialsId                 : "gitDeploymentKey",
                            autoDeployBranchesList        : ["develop"],
                            nexusCredentialsId            : "dev_read_nexus",
                            // SonarCloud
                            sonarScannerDockerSkip        : true,  // on/off Sonar Scanner in Docker version
                            sonarScannerGradleSkip        : false, // on/off Sonar Scanner in Gradle project
                            switchSonarCloudPipelineFailed: false, // abort pipeline when SonarCloud return ERROR for quality code
                            projectKeySonarCloud          : "symphonydevelopers_pirozhok-api",
                            // Build parameters
                            buildImage                    : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/openjdk-debian-gradle:8.131.3-jdk11",
                            buildEnvVars                  : ["NEXUS_USER": '${NEXUS_USER}', "NEXUS_PASS": '${NEXUS_PASS}']
                    ],
                    serviceNativeIos : [
                            // git repository parameters
                            "stageName"                : "Getting Native IOS sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/native-ios.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "NATIVE IOS sources branch/commit/tag name",
                            "relativeTargetDir"        : "nativeios",
                            "credentialsId"            : "gitBitBucketKey",
                    ],
                    serviceNativeIosAutomation : [
                            // git repository parameters
                            "stageName"                : "Getting Native_ios_automation sources",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/native_ios_automation.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "Voltron BMA UI Test sources branch/commit/tag name",
                            "relativeTargetDir"        : "sources",
                            "credentialsId"            : "gitBitBucketKey",
                            "nexusCredentialsId"       : "dev_read_nexus",
                            "testrailCredentialsId"    : "testrail_voltron",
                            // Build parameters
                            "build_image"              : "",
                            "buildEnvVars"             : ["DISCOVERY_DIR": "/opt/workDir/", "ACCOUNTS_SHARING": "https://accounts-sharing-dev0.coralsports.dev.cloud.ladbrokescoral.com"],
                            "buildEnvVarsFile"         : "env.list"
                    ],
            ]
    ]
    return constants
}
