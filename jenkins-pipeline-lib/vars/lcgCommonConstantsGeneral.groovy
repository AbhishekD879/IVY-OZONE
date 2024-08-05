def call() {

    def constants = [
            common: [
                    defaultEcr                     : "740335462382.dkr.ecr.eu-west-2.amazonaws.com",
                    defaultSonarToken              : "26581a47-d398-4279-a369-f30eea3a1018",
                    fortify360ServerAddOn          : "http://fortify.bwin.com/Fortify360ServerAddOn",
                    repoApplicationBuild           : [
                            "stageName"                : "Getting application build scripts",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/application-build.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "Application-build branch/commit/tag name",
                            "relativeTargetDir"        : "scripts",
                            "credentialsId"            : "gitDeploymentKey",
                            "ignoreNotifyCommit"       : true
                    ],
                    repoOxygenPlaybook             : [
                            "stageName"                : "Getting Oxygen playbooks",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/oxygen-playbook.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "Oxygen-playbook branch/commit/tag name",
                            "relativeTargetDir"        : "playbooks",
                            "credentialsId"            : "gitDeploymentKey",
                            "ignoreNotifyCommit"       : true
                    ],
                    repoAnsibleInventories         : [
                            "stageName"                : "Getting Ansible inventories",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/ansible-inventories.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "Ansible-inventories branch/commit/tag name",
                            "relativeTargetDir"        : "inventories",
                            "credentialsId"            : "gitDeploymentKey",
                            "ignoreNotifyCommit"       : true
                    ],
                    repoLadbrokesAnsibleInventories: [
                            "stageName"                : "Getting Ladbrokes Ansible inventories",
                            "url"                      : "git@bitbucket.org:symphonydevelopers/lad-ansible-inventories.git",
                            "branch_default"           : "master",
                            "job_parameter_description": "Ladbrokes Ansible-inventories branch/commit/tag name",
                            "relativeTargetDir"        : "lad-inventories",
                            "credentialsId"            : "gitDeploymentKey",
                            "ignoreNotifyCommit"       : true
                    ],
                    sonarCloud                     : [
                            parametersSonarCloud            : [
                                    "-Dsonar.host.url"                : "https://sonarcloud.io",
                                    "-Dsonar.organization"            : "coral-devops-support-bitbucket",
                                    "-Dsonar.projectBaseDir"          : "./",
                                    "-Dproject.settings"              : "./sonar-project.properties",
                                    "-Dsonar.scanner.metadataFilePath": "\\\$(pwd)/report-task.txt"
                            ],
                            "build_image"                   : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/sonar-scanner-node:3.2.0_jdk11",
                            "serviceTimeout"                : 1800,                // Seconds
                            "switchSonarCloudPipelineFailed": true,               // abort pipeline when SonarCloud return ERROR for quality code
                            "sonarService"                  : "SonarCloud"        // sonarService name is configured in Jenkins global configuration
                    ],
                    sonarCloudIos                  : [
                            parametersSonarCloud            : [
                                    "-Dsonar.c.file.suffixes"            :  "-",
                                    "-Dsonar.cpp.file.suffixes"          :  "-",
                                    "-Dsonar.objc.file.suffixes"         :  "-",
                                    "-Dsonar.exclusions"                 : "Pods/**",
                                    "-Dsonar.swift.coverage.reportPath"  : "report.llcov",
                                    "-Dsonar.swift.swiftLint.reportPaths": "swiftlint.result.json",
                                    "-Dproject.settings"                 : "./sonar-project.properties",
                                    "-Dsonar.organization"               : "coral-devops-support-bitbucket"
                            ]
                    ],
                    fortify                        : [
                            s3Bucket             : "lcg-fortify-reports",
                            s3Region             : "eu-west-2 ",
                            defaultEntrypoint    : "/opt/entrypoint",
                            overwrittenEntrypoint: "/bin/sh",
                            build_image          : "740335462382.dkr.ecr.eu-west-2.amazonaws.com/fortify-scan:20.1.0",
                    ],
                    gitBitBucketKey                : "694990c6-125c-41ad-9742-122af94bd50a",
                    gitDeploymentKey               : "7ed15632-c054-4fe1-9305-479847dc754b",
                    awsDeploymentKey               : "coral-14-12-2017.pem",
                    serviceImageTagLength          : 24,
                    hostWebServerDev               : "192.168.132.193",
                    userWebServerDev               : "ubuntu",
                    pathWebServerDev               : "proxy/html",
                    nexusServerSymphony            : [
                            registry   : "https://nexus-vie.coral.co.uk/repository/npm-all",
                            always_auth: true,
                            _auth      : "c3ltcGhvbnkubmV4dXM6U3ltcGgwbnkwcmNoMyR0cjQ="
                    ],
                    nexusServerOnprem  : [
                            registry   : "https://nexus-vie.coral.co.uk/repository/npm-all",
                            always_auth: true,
                            _auth      : "c3ltcGhvbnkubmV4dXM6U3ltcGgwbnkwcmNoMyR0cjQ="
                    ],
                    artifactoryGvc     : [
                            registry   : "https://artifactory.bwinparty.corp/artifactory/api/npm/npm-coral/",
                            always_auth: true,
                            _auth      : "dy5wLnN5bS5ibGQwMTpBUDdINnFwY2pYSEhUYWFiNGVIVWhjenRpcWc=",
                            strict_ssl : false
                    ],
                    notificationsList              : [
                            email: [
                                    [
                                            envLevel      : ["dev0", "dev1", "dev2", "tst0", "tst1", "hlv0", "prd0", "prod"],
                                            recipientsList: "IVY_LCG_DEV@entaingroup.com"
                                    ],
                                    [
                                            envLevel      : ["hlv0"],
                                            recipientsList: "IVY_LCG_DEV@entaingroup.com"
                                    ],
                                    [
                                            envLevel      : ["prd0", "prod"],
                                            recipientsList: "IVY_LCG_DEV@entaingroup.com"
                                    ]
                            ]

                    ]
            ]
    ]
    return constants
}
