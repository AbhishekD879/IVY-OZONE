def call() {
/**
 *     16.04.2019
 *
 *     STG & TST use:
 *     "envTypeDeploy"     : "akamaiAsperaParallel",
 *     "rsyncHost"         : "bm-mobile-prod3",
 *     "asperaSshKey"      : "~/.ssh/id_rsa_akamai.bm-mobile-prod-c",
 *
 *     HL & PROD use:
 *     "envTypeDeploy"     : "akamaiAsperaParallel",
 *     "rsyncHost"         : "bm-mobile-prod4",
 *     "asperaSshKey"      : "~/.ssh/id_rsa_akamai.bm-mobile-prod-d",
 */

    def constants = [
            akamaiLadbrokes: [
                    default         : [
                            "envTypeDeploy"     : "akamaiRsyncParallel",
                            "codeAkamaiHost"    : "328873",
                            "pathAkamaiHost"    : "CORAL",
                            "rsyncHost"         : "bm-mobile-prod4",
                            "rsyncParams"       : "ahW",
                            "rsyncFilter"       : "protect 3rdparty/*",
                            "rsyncVerbose"      : "vvv",
                            "rsyncRetry"        : 20,
                            "rsyncSleep"        : 30,
                            "asperaHost"        : "coraliassets.aspera.upload.akamai.com",
                            "asperaUser"        : "sshacs",
                            "asperaSshKey"      : "~/.ssh/id_rsa_akamai.bm-mobile-prod-d",
                            "asperaRetry"       : 20,
                            "asperaSleep"       : 30,
                            "ansiblePlaybooks"  : "common.repoOxygenPlaybook",
                            "ansibleInventories": "common.repoLadbrokesAnsibleInventories",
                            "artifactS3Bucket"  : "oxygen-ladbrokesoxygen-nonprod",
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
                            env_test_path       : "tests/pack_002_User_Account/Authentication/Login_Logout/test_C28220_Successful_Log_In_with_Username_and_Password.py",
                            mark                : "tst2",
                            custom_marks        : "",
                            back_end            : "tst2",
                            run_on              : "mobile and desktop",
                            testingTimeout      : 600       // seconds
                    ],
                    envSportsRedTst2: [
                            "envName"         : "Ladbrokes Akamai Sports Red Tst2",
                            "envLevel"        : "tst0",
                            "rootWebServerDir": "sports-red-tst2.ladbrokes.com",
                            "codeCP"          : "812270",
                            "envTypeDeploy"   : "akamaiRsyncParallel",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-roxanne-a"
                    ],
                    envSportsTst1   : [
                            "envName"         : "Ladbrokes Akamai Sports Tst1",
                            "envLevel"        : "tst1",
                            "rootWebServerDir": "sports-tst1.ladbrokes.com",
                            "codeCP"          : "755786"
                    ],
                    envSportsTst2   : [
                            "envName"         : "Ladbrokes Akamai Sports Tst2",
                            "envLevel"        : "tst0",
                            "rootWebServerDir": "sports-tst2.ladbrokes.com",
                            "codeCP"          : "812270",
                            "envTypeDeploy"   : "akamaiRsyncParallel",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-roxanne-a"
                    ],
                    envSportsStg2   : [
                            "envName"         : "Ladbrokes Akamai Sports Stg2",
                            "envLevel"        : "stg0",
                            "rootWebServerDir": "sports-stg2.ladbrokes.com",
                            "codeCP"          : "824362",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-roxanne-b"
                    ],
                    envSportsHl     : [
                            "envName"         : "Ladbrokes Akamai Sports HL",
                            "envLevel"        : "hlv0",
                            "rootWebServerDir": "sports-hl.ladbrokes.com",
                            "codeCP"          : "816744",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-roxanne-b",
                            "artifactS3Bucket": "oxygen-ladbrokesoxygen-nonprod"
                    ],
                    envSportsRedProd: [
                            "asperaSshKey"    : "~/.ssh/id_rsa_akamai.bm-mobile-prod-c",
                            "rsyncHost"       : "bm-mobile-prod3",
                            "envName"         : "Ladbrokes Akamai Sports Red Prod",
                            "envLevel"        : "prd0",
                            "rootWebServerDir": "sports-red.ladbrokes.com",
                            "codeCP"          : "821654",
                            "artifactS3Bucket": "oxygen-ladbrokesoxygen-prod"
                    ],
                    envMSportsProd  : [
                            "envName"         : "Ladbrokes Akamai MSports Prod",
                            "envLevel"        : "prd0",
                            "rootWebServerDir": "msports.ladbrokes.com",
                            "codeCP"          : "877633",
                            "artifactS3Bucket": "oxygen-ladbrokesoxygen-prod",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-roxanne-b"
                    ],
                    envSportsProd  : [
                            "envName"         : "Ladbrokes Akamai Sports Prod",
                            "envLevel"        : "prd0",
                            "rootWebServerDir": "sports.ladbrokes.com",
                            "codeCP"          : "877633",
                            "artifactS3Bucket": "oxygen-ladbrokesoxygen-prod",
                            "codeAkamaiHost"  : "",
                            "pathAkamaiHost"  : "",
                            "rsyncHost"       : "akamai-roxanne-a"
                    ],
                    envOtfRedPrd0V1 : [
                            "envTypeDeploy"    : "akamaiRsync",
                            "envName"          : "Ladbrokes One-Two-Free UI Akamai PRD0 v1",
                            "envLevel"         : "prd0",
                            "rootWebServerDir" : "otf.ladbrokes.com/v1",
                            "codeCP"           : "821924",
                            "sourceDir"        : "build",
                            "relativeSourceDir": "sources",
                            "artifactS3Bucket" : "oxygen-ladbrokesoxygen-prod",
                            "codeAkamaiHost"   : "",
                            "pathAkamaiHost"   : "",
                            "rsyncHost"        : "akamai-roxanne-b"
                    ],
                    envOtfRedHlv0V1 : [
                            "envTypeDeploy"    : "akamaiRsync",
                            "envName"          : "Ladbrokes One-Two-Free UI Akamai HLV0 v1",
                            "envLevel"         : "hlv0",
                            "rootWebServerDir" : "otf-hlv0.ladbrokes.com/v1",
                            "codeCP"           : "882999",
                            "sourceDir"        : "build",
                            "relativeSourceDir": "sources",
                            "artifactS3Bucket" : "oxygen-ladbrokesoxygen-nonprod",
                            "codeAkamaiHost"   : "",
                            "pathAkamaiHost"   : "",
                            "rsyncHost"        : "akamai-roxanne-b"
                    ],
                    envAkamaiTest   : [
                            "asperaSshKey"    : "~/.ssh/id_rsa_akamai.bm-mobile-prod-c",
                            "rsyncHost"       : "bm-mobile-prod3",
                            "envName"         : "Akamai test",
                            "envLevel"        : "tst1",
                            "rootWebServerDir": "test",
                            "codeCP"          : "730750"
                    ]
            ]
    ]
    return constants
}
