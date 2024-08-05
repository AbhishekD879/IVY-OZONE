def call() {
/**
 *     16.04.2019
 *
 *     STG & TST use:
 *     "envTypeDeploy"     : "akamaiRsyncParallel",
 *     "rsyncHost"         : "bm-mobile-prod2",
 *     "asperaSshKey"      : "~/.ssh/id_rsa_akamai.bm-mobile-prod-b",
 *
 *     HL & PROD use:
 *     "envTypeDeploy"     : "akamaiRsyncParallel",
 *     "rsyncHost"         : "bm-mobile-prod",
 *     "asperaSshKey"      : "~/.ssh/id_rsa_akamai.bm-mobile-prod",
 */

    def constants = [
            akamaiCoral: [
                    default       : [
                            "envTypeDeploy"     : "akamaiRsyncParallel",
                            "codeAkamaiHost"    : "328873",
                            "pathAkamaiHost"    : "CORAL",
                            "rsyncHost"         : "bm-mobile-prod2",
                            "rsyncParams"       : "ahW",
                            "rsyncFilter"       : "protect 3rdparty/*",
                            "rsyncVerbose"      : "vvv",
                            "rsyncRetry"        : 20,
                            "rsyncSleep"        : 30,
                            "asperaHost"        : "coraliassets.aspera.upload.akamai.com",
                            "asperaUser"        : "sshacs",
                            "asperaSshKey"      : "~/.ssh/id_rsa_akamai.bm-mobile-prod-b",
                            "asperaRetry"       : 20,
                            "asperaSleep"       : 30,
                            "ansiblePlaybooks"  : "common.repoOxygenPlaybook",
                            "ansibleInventories": "common.repoAnsibleInventories",
                            "artifactS3Bucket"  : "oxygen-coralsports-nonprod",
                            "artifactUpload"    : true,

                            "brands"            : [
                                    "coral"    : [
                                            "sourceDir": "dist/coral"
                                    ],
                                    "ladbrokes": [
                                            "sourceDir": "dist/ladbrokes"
                                    ]
                            ],
                            // UI Testing
                            uiTestingJob        : "CRLAT-BMA-UI-TESTING",
                            ref_voltron         : "invictus",
                            ref_jenkinsfile     : "invictus",
                            env_test_path       : "tests/pack_002_User_Account/Authentication/Login_Logout/test_C28220_C16268954_Successful_Log_In_with_Username_and_Password.py",
                            mark                : "tst2",
                            custom_marks        : "",
                            back_end            : "tst2",
                            run_on              : "mobile and desktop",
                            testingTimeout      : 600       // seconds
                    ],
                    envAkamaiTest : [
                            "envTypeDeploy"       : "akamaiRsyncParallel",
                            "envName"             : "Akamai test",
                            "envLevel"            : "tst1",
                            "rootWebServerDir"    : "test",
                            "codeCP"              : "730750",
                            "prePurgeCacheTimeout": 30,
                            "notificationsList"   : [
                                    email: [
                                            recipientsList: "kucher_ua@yahoo.com,habiba@aljazira.com",
                                            blueOcean     : false
                                    ]
                            ]
                    ],
                    envBetTst2    : [
                            "envName"         : "Coral Akamai Bet TST2",
                            "envLevel"        : "tst2",
                            "rootWebServerDir": "bet-tst2.coral.co.uk",
                            "codeCP"          : "730748",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-coralsportsbook-a"
                    ],
                    envBetStg2    : [
                            "envName"         : "Coral Akamai Bet STG2",
                            "envLevel"        : "stg2",
                            "rootWebServerDir": "bet-stg2.coral.co.uk",
                            "codeCP"          : "730758",
                            "envTypeDeploy"   : "akamaiRsyncParallel",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-coralsportsbook-a"
                    ],
                    envSportsProd : [
                            "envName"             : "Coral Akamai Sports PROD",
                            "envLevel"            : "prod",
                            "rootWebServerDir"    : "sports.coral.co.uk",
                            "codeCP"              : "473772",
                            "artifactS3Bucket"    : "oxygen-coralsports-prod",
                            "prePurgeCacheTimeout": 600,
                            "codeAkamaiHost"      : "",
                            "pathAkamaiHost"      : "",
                            "rsyncHost"           : "akamai-coralsportsbook-b"
                    ]
            ]
    ]
    return constants
}
