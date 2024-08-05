#!/usr/bin/env groovy
import java.time.temporal.Temporal

CommonFunctions = new lcgCommonFunctions()
CommonConstantsGeneral = new lcgCommonConstantsGeneral()
CommonConstantsServices = new lcgCommonConstantsServices()
CommonConstantsEnvsDev0Coral = new lcgCommonConstantsEnvsDev0Coral()
CommonConstantsEnvsDevVanilla = new lcgCommonConstantsEnvsDevVanilla()
CommonConstantsEnvsDev0Ladbrokes = new lcgCommonConstantsEnvsDev0Ladbrokes()
CommonConstantsEnvsAkamaiCoral = new lcgCommonConstantsEnvsAkamaiCoral()
CommonConstantsEnvsAkamaiLadbrokes = new lcgCommonConstantsEnvsAkamaiLadbrokes()
CommonConstantsEnvsAwsCoral = new lcgCommonConstantsEnvsAwsCoral()
CommonConstantsEnvsAwsLadbrokes = new lcgCommonConstantsEnvsAwsLadbrokes()
CommonConstantsEnvsAwsCoralCloudFront = new lcgCommonConstantsEnvsAwsCoralCloudFront()

def dummy_constants = [
        defaultEcr       : "740335462382.dkr.ecr.eu-west-2.amazonaws.com",
        serviceDummy     : [
                // git repository parameters
                "stageName"                : "Getting Dummy sources",
                "url"                      : "git@bitbucket.org:symphonydevelopers/dummy-api_service.git",
                "branch_default"           : "dev_default",
                "branchDefault"            : "    devDefault   ",
                "job_parameter_description": "Timeform sources branch/commit/tag name",
                "relativeTargetDir"        : "dummy_sources",
                "applicationBuildDir"      : "dummy_appDir",
                "credentialsId"            : "gitBitBucketKey",
                // Build parameters
                "build_image"              : "registry-8.9.4.1",
                "buildEnvVars"             : ["NODE_OPTIONS": "--max_old_space_size=10240"],
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
        serviceDummyEmpty: [:],
        // Root level
        serviceDummy1    : [
                "service11": "service_param_11",
                "service12": "service_param_12",
        ],
        // Two level with default
        services1        : [
                default      : [
                        "def1": "default1",
                        "def2": "default2"
                ],
                serviceDummy1: [
                        "service11": "service_param_11",
                        "service12": "service_param_12",
                ],
                serviceDummy2: [
                        "def2"     : "custom_service_dummy_2",
                        "service21": "service_param_21",
                        "service22": "service_param_22",
                ]
        ],
        // Two levels without default
        services2        : [
                serviceDummy1: [
                        "service11": "service_param_11",
                        "service12": "service_param_12",
                ],
                serviceDummy2: [
                        "service21": "service_param_21",
                        "service22": "service_param_22",
                ]
        ],
        // Three levels
        services3        : [
                // with default
                services31: [
                        default      : [
                                "def1": "default1",
                                "def2": "default2"
                        ],
                        serviceDummy1: [
                                "service11": "service_param_11",
                                "service12": "service_param_12",
                        ],
                        serviceDummy2: [
                                "service21": "service_param_21",
                                "service22": "service_param_22",
                        ]
                ],
                // without default
                services32: [
                        serviceDummy1: [
                                "service11": "service_param_11",
                                "service12": "service_param_12",
                        ],
                        serviceDummy2: [
                                "service21": "service_param_21",
                                "service22": "service_param_22",
                        ]
                ]
        ],
        common           : [
                constant1         : "medvedko",
                constant2         : [
                        constant22: "prevedko",
                        constant23: 777
                ],
                notificationsList1: [
                        email: [
                                [
                                        envLevel      : ["tst1"],
                                        recipientsList: ["viktor.kucher@symphony-soutions.eu"]
                                ],
                                [
                                        envLevel      : ["hlv0"],
                                        recipientsList: ["lcl.leads@ladbrokescoral.com"]
                                ]
                        ],
                        slack: [
                                [
                                        envLevel      : ["tst1"],
                                        recipientsList: ["viktor.kucher", "orest.kapko"]
                                ]
                        ]
                ],
                notificationsList2: [
                        email: [
                                [
                                        envLevel      : ["tst1"],
                                        recipientsList: ["viktor.kucher@symphony-soutions.eu"]
                                ],
                                [
                                        envLevel      : ["hlv0"],
                                        recipientsList: ["lcl.leads@ladbrokescoral.com"]
                                ]
                        ]
                ]
        ]
]

clone_serviceDummy = dummy_constants["serviceDummy"].clone()


println("###   Checking Common functions...   ###")

// println('lcgCommonFunctions.getServiceImageTagLength')
// assert 24 == CommonFunctions.getServiceImageTagLength()
// println('Ok')

println('lcgCommonFunctions.getGitDefaultBranch')
assert "devDefault" == CommonFunctions.getGitDefaultBranch(dummy_constants["serviceDummy"])
assert "" == CommonFunctions.getGitDefaultBranch(dummy_constants["serviceDummyEmpty"])
println('Ok')

println('lcgCommonFunctions.getGitTargetDirectory')
assert "dummy_sources" == CommonFunctions.getGitTargetDirectory(dummy_constants["serviceDummy"])
assert "" == CommonFunctions.getGitTargetDirectory(dummy_constants["serviceDummyEmpty"])
println('Ok')

println('lcgCommonFunctions.getServiceAppDir')
assert "dummy_appDir" == CommonFunctions.getServiceAppDir(dummy_constants["serviceDummy"])
assert "" == CommonFunctions.getServiceAppDir(dummy_constants["serviceDummyEmpty"])
println('Ok')

println("lcgCommonFunctions.commandCdDir")
assert "cd testDir" == CommonFunctions.commandCdDir("testDir")
assert "" == CommonFunctions.commandCdDir("")
assert "" == CommonFunctions.commandCdDir(" ")
assert "" == CommonFunctions.commandCdDir("    ")
println('Ok')

println("lcgCommonFunctions.commandShInDirMain")
assert "cd dummy_sources && echo Prevedko" == CommonFunctions.commandShInDirMain(dummy_constants["serviceDummy"],
        "echo Prevedko")
clone_serviceDummy["relativeTargetDir"] = ""
assert "echo Prevedko" == CommonFunctions.commandShInDirMain(clone_serviceDummy, "echo Prevedko")
println('Ok')

println("lcgCommonFunctions.commandSudoShInDirMain")
assert "cd dummy_sources && sudo -E -H -u jenkins sh -c 'echo Medvedko'" == CommonFunctions.commandSudoShInDirMain(
        dummy_constants["serviceDummy"], "echo Medvedko")
assert "cd dummy_sources && sudo -E -H -u pupkin sh -c 'echo Medvedko'" == CommonFunctions.commandSudoShInDirMain(
        dummy_constants["serviceDummy"], "echo Medvedko", "pupkin")
clone_serviceDummy["relativeTargetDir"] = ""
assert "sudo -E -H -u jenkins sh -c 'echo Medvedko'" == CommonFunctions.commandSudoShInDirMain(clone_serviceDummy,
        "echo Medvedko")
assert "sudo -E -H -u jenkins sh -c 'echo Medvedko'" == CommonFunctions.commandSudoShInDirMain(
        dummy_constants["serviceDummyEmpty"], "echo Medvedko")
println('Ok')

println('lcgCommonFunctions.getJobGitRefParameter')
assert "ref_dummy_api_service" == CommonFunctions.getJobGitRefParameter(dummy_constants["serviceDummy"])
println('Ok')

println('lcgCommonFunctions.getServiceBuildImage')
assert "registry-8.9.4.1" == CommonFunctions.getServiceBuildImage(dummy_constants["serviceDummy"])
println('Ok')

println('lcgCommonFunctions.getBuildEnvVars')
assert "export NODE_OPTIONS=--max_old_space_size=10240" == CommonFunctions.getBuildEnvVars(
        dummy_constants["serviceDummy"])
clone_serviceDummy["buildEnvVars"] = ""
assert "" == CommonFunctions.getBuildEnvVars(clone_serviceDummy)
clone_serviceDummy["buildEnvVars"] = ["VAR1": "varsedko1", "VAR2": "varsedko2"]
assert "export VAR1=varsedko1 && export VAR2=varsedko2" == CommonFunctions.getBuildEnvVars(clone_serviceDummy)
println('Ok')

println('lcgCommonFunctions.getBuildEnvVarsDockerStyle')
assert "-e NODE_OPTIONS=--max_old_space_size=10240" == CommonFunctions.getBuildEnvVarsDockerStyle(
        dummy_constants["serviceDummy"])
clone_serviceDummy["buildEnvVars"] = ""
assert "" == CommonFunctions.getBuildEnvVarsDockerStyle(clone_serviceDummy)
clone_serviceDummy["buildEnvVars"] = ["VAR1": "varsedko1", "VAR2": "varsedko2"]
assert "-e VAR1=varsedko1 -e VAR2=varsedko2" == CommonFunctions.getBuildEnvVarsDockerStyle(clone_serviceDummy)
println('Ok')

println('lcgCommonFunctions.getConstantsParametersEngine')

assert ['service11': 'service_param_11', 'service12': 'service_param_12'] ==
        CommonFunctions.getConstantsParametersEngine("serviceDummy1", dummy_constants)

assert ['def1': 'default1', 'def2': 'default2', 'service11': 'service_param_11', 'service12': 'service_param_12'] ==
        CommonFunctions.getConstantsParametersEngine("services1.serviceDummy1", dummy_constants)

assert ['def1': 'default1', 'def2': 'custom_service_dummy_2', 'service21': 'service_param_21', 'service22': 'service_param_22'] ==
        CommonFunctions.getConstantsParametersEngine("services1.serviceDummy2", dummy_constants)

assert ['service11': 'service_param_11', 'service12': 'service_param_12'] ==
        CommonFunctions.getConstantsParametersEngine("services2.serviceDummy1", dummy_constants)

assert ['def1': 'default1', 'def2': 'default2', 'service11': 'service_param_11', 'service12': 'service_param_12'] ==
        CommonFunctions.getConstantsParametersEngine("services3.services31.serviceDummy1", dummy_constants)

assert ['service21': 'service_param_21', 'service22': 'service_param_22'] ==
        CommonFunctions.getConstantsParametersEngine("services3.services32.serviceDummy2", dummy_constants)

assert null == CommonFunctions.getConstantsParametersEngine("services3.services32.serviceDummy3", dummy_constants)

assert ['constant22': 'prevedko', 'constant23': 777] == CommonFunctions.getConstantsParametersEngine("common.constant2", dummy_constants)

assert 'medvedko' == CommonFunctions.getConstantsParametersEngine("common.constant1", dummy_constants)

assert 'prevedko' == CommonFunctions.getConstantsParametersEngine("common.constant2.constant22", dummy_constants)

assert 777 == CommonFunctions.getConstantsParametersEngine("common.constant2.constant23", dummy_constants)

assert null == CommonFunctions.getConstantsParametersEngine("common.constant2.constant222", dummy_constants)

assert [
        'email': [['envLevel': ['tst1'], 'recipientsList': ['viktor.kucher@symphony-soutions.eu']],
                  ['envLevel': ['hlv0'], 'recipientsList': ['lcl.leads@ladbrokescoral.com']]],
        'slack': [['envLevel': ['tst1'], 'recipientsList': ['viktor.kucher', 'orest.kapko']]]] ==
        CommonFunctions.getConstantsParametersEngine("common.notificationsList1", dummy_constants)

assert ['email': [['envLevel': ['tst1'], 'recipientsList': ['viktor.kucher@symphony-soutions.eu']],
                  ['envLevel': ['hlv0'], 'recipientsList': ['lcl.leads@ladbrokescoral.com']]]] ==
        CommonFunctions.getConstantsParametersEngine("common.notificationsList2", dummy_constants)

println('Ok')

println('lcgCommonFunctions.getUniqueListByKey')

def multiBranchAutodeploy = [
        [
                branches      : ["develop", "dev"],
                targetEnvsList: ["awsCoral.dev0", "awsLadbrokes.dev0"]
        ],
        [
                branches      : ["develop"],
                targetEnvsList: ["awsCoral.dev1", "awsLadbrokes.dev0"]
        ],
        [
                branches      : ["release-98.0.0"],
                targetEnvsList: ["awsCoral.tst0", "awsLadbrokes.tst0"]
        ],
        [
                branches      : ["release-97.0.0"],
                targetEnvsList: ["awsCoral.tst1"]
        ],
        [
                branches      : ["release-99.0.1"],
                targetEnvsList: ["awsLadbrokes.tst1"]
        ],
        [
                branches      : ["release-97.0.0"],
                targetEnvsList: ["awsLadbrokes.tst1"],
        ]
]

assert ['awsCoral.dev0', 'awsLadbrokes.dev0'] == CommonFunctions.getUniqueListByKey(multiBranchAutodeploy, "dev", "branches", "targetEnvsList")
assert ['awsCoral.dev0', 'awsLadbrokes.dev0', 'awsCoral.dev1'] == CommonFunctions.getUniqueListByKey(multiBranchAutodeploy, "develop", "branches", "targetEnvsList")
assert ['awsCoral.tst1', 'awsLadbrokes.tst1'] == CommonFunctions.getUniqueListByKey(multiBranchAutodeploy, "release-97.0.0", "branches", "targetEnvsList")
assert ['awsLadbrokes.tst1'] == CommonFunctions.getUniqueListByKey(multiBranchAutodeploy, "release-99.0.1", "branches", "targetEnvsList")
assert [] == CommonFunctions.getUniqueListByKey(multiBranchAutodeploy, "release-99.0.0", "branches", "targetEnvsList")

println('Ok')

println('###   Check constants structure...   ###')
CommonConstantsGeneral()
CommonConstantsServices()
CommonConstantsEnvsDev0Coral()
CommonConstantsEnvsDevVanilla()
CommonConstantsEnvsDev0Ladbrokes()
CommonConstantsEnvsAkamaiCoral()
CommonConstantsEnvsAkamaiLadbrokes()
CommonConstantsEnvsAwsCoral()
CommonConstantsEnvsAwsLadbrokes()
CommonConstantsEnvsAwsCoralCloudFront()
println('Ok')




