def call() {

    def constants = [
            nginxCoralDev0: [
                    default             : [
                            "envTypeDeploy"   : "nginxRsyncAwsDiscoveryHost",
                            "hostWebServerDev": "",
                            "userWebServerDev": "ubuntu",
                            "pathWebServerDev": "/opt/nginx/vhosts/",
                            "deploymentKey"   : "",
                            "brands"          : [
                                    "coral"    : [
                                            "sourceDir": "dist/coral"
                                    ],
                                    "ladbrokes": [
                                            "sourceDir": "dist/ladbrokes"
                                    ]
                            ],
                            jumpNodeLabel     : "DevDeploy"
                    ],
                    envDevInvictus      : [
                            "envName"          : "Dev0 Invictus",
                            "urlWebServerDev"  : "invictus.coral.co.uk",
                            "defaultEnvProfile": [
                                    "name"        : "envProfileInvictus",
                                    "defaultValue": "dev0",
                                    "description" : "Invictus environment profile"
                            ]
                    ],
                    envDevInplay        : [
                            "envName"          : "Dev0 Inplay",
                            "urlWebServerDev"  : "inplay-invictus.coral.co.uk",
                            "defaultEnvProfile": [
                                    "name"        : "envProfileInplay",
                                    "defaultValue": "ladbrokes-dev1",
                                    "description" : "Inplay environment profile"
                            ]
                    ],
                    envDevDevops        : [
                            "envName"        : "Dev0 Devops",
                            "urlWebServerDev": "devops-invictus.coral.co.uk"
                    ],
                    envDevFantom1       : [
                            "envName"        : "Dev0 Fantom1",
                            "urlWebServerDev": "fantom1-invictus.coral.co.uk"
                    ],
                    envDevFantom2       : [
                            "envName"        : "Dev0 Fantom2",
                            "urlWebServerDev": "fantom2-invictus.coral.co.uk"
                    ],
                    envDevFantom3       : [
                            "envName"        : "Dev0 Fantom3",
                            "urlWebServerDev": "fantom3-invictus.coral.co.uk"
                    ],
                    envDevFantom4       : [
                            "envName"        : "Dev0 Fantom4",
                            "urlWebServerDev": "fantom4-invictus.coral.co.uk"
                    ],
                    envDevFantom5       : [
                            "envName"        : "Dev0 Fantom5",
                            "urlWebServerDev": "fantom5-invictus.coral.co.uk"
                    ],
                    envDevFantom6       : [
                            "envName"        : "Dev0 Fantom6",
                            "urlWebServerDev": "fantom6-invictus.coral.co.uk"
                    ],
                    envDevVoltron       : [
                            "envName"        : "Dev0 Voltron",
                            "urlWebServerDev": "voltron-invictus.coral.co.uk"
                    ],
                    envDevVoltron2      : [
                            "envName"        : "Dev0 Voltron2",
                            "urlWebServerDev": "voltron2-invictus.coral.co.uk"
                    ],
                    envDevMustang2      : [
                            "envName"        : "Dev0 Mustang2",
                            "urlWebServerDev": "mustang2-invictus.coral.co.uk"
                    ],
                    envDevMustang3      : [
                            "envName"        : "Dev0 Mustang3",
                            "urlWebServerDev": "mustang3-invictus.coral.co.uk"
                    ],
                    envDevMustang4      : [
                            "envName"        : "Dev0 Mustang4",
                            "urlWebServerDev": "mustang4-invictus.coral.co.uk"
                    ],
                    envDevMustang5      : [
                            "envName"        : "Dev0 Mustang5",
                            "urlWebServerDev": "mustang5-invictus.coral.co.uk"
                    ],
                    envDevAvengers2     : [
                            "envName"        : "Dev0 Avengers2",
                            "urlWebServerDev": "avengers2-invictus.coral.co.uk"
                    ],
                    envDevAvengers3     : [
                            "envName"        : "Dev0 Avengers3",
                            "urlWebServerDev": "avengers3-invictus.coral.co.uk"
                    ],
                    envDevHulk          : [
                            "envName"        : "Dev0 Hulk",
                            "urlWebServerDev": "hulk-invictus.coral.co.uk"
                    ],
                    envDevMarvel        : [
                            "envName"        : "Dev0 Marvel",
                            "urlWebServerDev": "marvel-invictus.coral.co.uk"
                    ],
                    envDevSunny         : [
                            "envName"        : "Dev0 Sunny",
                            "urlWebServerDev": "sunny-invictus.coral.co.uk"
                    ],
                    envDevRainy         : [
                            "envName"        : "Dev0 Rainy",
                            "urlWebServerDev": "rainy-invictus.coral.co.uk"
                    ],
                    envDevSnowy         : [
                            "envName"        : "Dev0 Snowy",
                            "urlWebServerDev": "snowy-invictus.coral.co.uk"
                    ],
                    envDevStrawberry    : [
                            "envName"        : "Dev0 Strawberry",
                            "urlWebServerDev": "strawberry-invictus.coral.co.uk"
                    ],
                    envDevPineapple     : [
                            "envName"        : "Dev0 Pineapple",
                            "urlWebServerDev": "pineapple-invictus.coral.co.uk"
                    ],
                    envDevWatermelon    : [
                            "envName"        : "Dev0 Watermelon",
                            "urlWebServerDev": "watermelon-invictus.coral.co.uk"
                    ],
                    envDevCurious       : [
                            "envName"        : "Dev0 Curious",
                            "urlWebServerDev": "curious-invictus.coral.co.uk"
                    ],
                    envDevFunny         : [
                            "envName"        : "Dev0 Funny",
                            "urlWebServerDev": "funny-invictus.coral.co.uk"
                    ],
                    envDevBright        : [
                            "envName"        : "Dev0 Bright",
                            "urlWebServerDev": "bright-invictus.coral.co.uk"
                    ],
                    envDevCherry        : [
                            "envName"        : "Dev0 Cherry",
                            "urlWebServerDev": "cherry-invictus.coral.co.uk"
                    ],
                    envDevRaspberry     : [
                            "envName"        : "Dev0 Raspberry",
                            "urlWebServerDev": "raspberry-invictus.coral.co.uk"
                    ],
                    envDevExcalibur     : [
                            "envName"        : "Dev0 Excalibur",
                            "urlWebServerDev": "excalibur-invictus.coral.co.uk"
                    ],
                    envDevNative        : [
                            "envName"        : "Dev0 Native",
                            "urlWebServerDev": "native-invictus.coral.co.uk"
                    ],
                    envDevNative1       : [
                            "envName"        : "Dev0 Native1",
                            "urlWebServerDev": "native1-invictus.coral.co.uk"
                    ],
                    envDevMuckers2      : [
                            "envName"        : "Dev0 Muckers2",
                            "urlWebServerDev": "muckers2-invictus.coral.co.uk"
                    ],
                    envDevAvengers      : [
                            "envName"        : "Dev0 Avengers",
                            "urlWebServerDev": "avengers-invictus.coral.co.uk"
                    ],
                    envDevDesktop       : [
                            "envName"        : "Dev0 Desktop",
                            "urlWebServerDev": "desktop-invictus.coral.co.uk"
                    ],
                    envDevAmazing       : [
                            "envName"        : "Dev0 Amazing",
                            "urlWebServerDev": "amazing-invictus.coral.co.uk"
                    ],
                    envDevCherryRed     : [
                            "envName"        : "Dev0 Cherry Red",
                            "urlWebServerDev": "cherry-excalibur.coral.co.uk"
                    ],
                    envDevDesktopRelease: [
                            "envName"        : "Dev0 Desktop Release",
                            "urlWebServerDev": "desktop-release-invictus.coral.co.uk"
                    ],
                    envDevKorali        : [
                            "envName"        : "Dev0 Korali",
                            "urlWebServerDev": "korali-invictus.coral.co.uk"
                    ],
                    envDevMuckers3      : [
                            "envName"        : "Dev0 Muckers3",
                            "urlWebServerDev": "muckers3-invictus.coral.co.uk"
                    ],
                    envDevBrave         : [
                            "envName"        : "Dev0 Brave",
                            "urlWebServerDev": "brave-invictus.coral.co.uk"
                    ],
                    envDevSilent        : [
                            "envName"        : "Dev0 Silent",
                            "urlWebServerDev": "silent-invictus.coral.co.uk"
                    ],
                    envDevMustang       : [
                            "envName"        : "Dev0 Mustang",
                            "urlWebServerDev": "mustang-invictus.coral.co.uk"
                    ],
                    envDevFramework     : [
                            "envName"        : "Dev0 Framework",
                            "urlWebServerDev": "framework-invictus.coral.co.uk"
                    ],
                    envDevExcaliburRed  : [
                            "envName"        : "Dev0 Excalibur Red",
                            "urlWebServerDev": "excalibur.coral.co.uk"
                    ],
                    envDevGrim          : [
                            "envName"        : "Dev0 Grim",
                            "urlWebServerDev": "grim-invictus.coral.co.uk"
                    ],
                    envDevRelease       : [
                            "envName"        : "Dev0 Release",
                            "urlWebServerDev": "release-invictus.coral.co.uk"
                    ],
                    envDevKorali2       : [
                            "envName"        : "Dev0 Korali2",
                            "urlWebServerDev": "korali2-invictus.coral.co.uk"
                    ],
                    envDevKorali3       : [
                            "envName"        : "Dev0 Korali3",
                            "urlWebServerDev": "korali3-invictus.coral.co.uk"
                    ],
                    envDevKorali4       : [
                            "envName"        : "Dev0 Korali4",
                            "urlWebServerDev": "korali4-invictus.coral.co.uk"
                    ],
                    envDevKorali5       : [
                            "envName"        : "Dev0 Korali5",
                            "urlWebServerDev": "korali5-invictus.coral.co.uk"
                    ],
                    envDevNaughty       : [
                            "envName"        : "Dev0 Naughty",
                            "urlWebServerDev": "naughty-invictus.coral.co.uk"
                    ],
                    envDevHollow        : [
                            "envName"        : "Dev0 Hollow",
                            "urlWebServerDev": "hollow-invictus.coral.co.uk"
                    ],
                    envDevTest          : [
                            "envName"        : "Dev0 Test",
                            "urlWebServerDev": "test-invictus.coral.co.uk"
                    ],
                    envDevOdds          : [
                            "envName"        : "Dev0 Odds",
                            "urlWebServerDev": "odds-invictus.coral.co.uk"
                    ],
                    envDevGraceful      : [
                            "envName"        : "Dev0 Graceful",
                            "urlWebServerDev": "graceful-invictus.coral.co.uk"
                    ],
                    envDevFantom        : [
                            "envName"        : "Dev0 Fantom",
                            "urlWebServerDev": "fantom-invictus.coral.co.uk"
                    ],
                    envDevMustangNew    : [
                            "envName"        : "Dev0 Mustang New",
                            "urlWebServerDev": "mustang-new-invictus.coral.co.uk"
                    ],
                    envDevTd            : [
                            "envName"        : "Dev0 Td",
                            "urlWebServerDev": "td-invictus.coral.co.uk"
                    ],
                    envDevPhoenix       : [
                            "envName"        : "Dev0 Phoenix",
                            "urlWebServerDev": "phoenix-invictus.coral.co.uk"
                    ],
                    envDevRaspberryRed  : [
                            "envName"        : "Dev0 Raspberry Red",
                            "urlWebServerDev": "raspberry-excalibur.coral.co.uk"
                    ],
                    envDevLaffly        : [
                            "envName"        : "Dev0 Laffly",
                            "urlWebServerDev": "laffly-invictus.coral.co.uk"
                    ],
                    envDevMuckers       : [
                            "envName"        : "Dev0 Muckers",
                            "urlWebServerDev": "muckers-invictus.coral.co.uk"
                    ],
                    envDevMuckers4       : [
                            "envName"        : "Dev0 Muckers4",
                            "urlWebServerDev": "muckers4-invictus.coral.co.uk"
                    ],
                    envDevMuckers5       : [
                            "envName"        : "Dev0 Muckers5",
                            "urlWebServerDev": "muckers5-invictus.coral.co.uk"
                    ],
                    envDevMuckers6       : [
                            "envName"        : "Dev0 Muckers6",
                            "urlWebServerDev": "muckers6-invictus.coral.co.uk"
                    ],
                    envDevExpress       : [
                            "envName"        : "Dev0 Express",
                            "urlWebServerDev": "express-invictus.coral.co.uk"
                    ],
                    envDevNew           : [
                            "envName"        : "Dev0 New",
                            "urlWebServerDev": "new-invictus.coral.co.uk"
                    ],
                    envDevNitro         : [
                            "envName"        : "Dev0 Nitro",
                            "urlWebServerDev": "nitro-invictus.coral.co.uk"
                    ],
                    envDevNitro2        : [
                            "envName"        : "Dev0 Nitro2",
                            "urlWebServerDev": "nitro2-invictus.coral.co.uk"
                    ],
                    envDevNitro3        : [
                            "envName"        : "Dev0 Nitro3",
                            "urlWebServerDev": "nitro3-invictus.coral.co.uk"
                    ],
                    envDevNitro4        : [
                            "envName"        : "Dev0 Nitro4",
                            "urlWebServerDev": "nitro4-invictus.coral.co.uk"
                    ],
                    envDevNitro5        : [
                            "envName"        : "Dev0 Nitro5",
                            "urlWebServerDev": "nitro5-invictus.coral.co.uk"
                    ],
                    envDevNitro6        : [
                            "envName"        : "Dev0 Nitro6",
                            "urlWebServerDev": "nitro6-invictus.coral.co.uk"
                    ],
                    envDevBe            : [
                            "envName"        : "Dev0 Be",
                            "urlWebServerDev": "be-invictus.coral.co.uk"
                    ],
                    envDevKanban        : [
                            "envName"        : "Dev0 Kanban",
                            "urlWebServerDev": "kanban-invictus.coral.co.uk"
                    ],
                    envDevScoreboard    : [
                            "envName"        : "Dev0 Scoreboard",
                            "urlWebServerDev": "scoreboard-invictus.coral.co.uk"
                    ],
                    envOtfDev0          : [
                            "envName"          : "Dev0 OTF",
                            "urlWebServerDev"  : "otf-dev0.coral.co.uk",
                            "sourceDir"        : "build",
                            "relativeSourceDir": "sources"
                    ],
                    envBetTst1          : [
                            "envName"        : "Dev0 envBetTst1",
                            "urlWebServerDev": "bet-tst1.coral.co.uk"
                    ],
                    envDevAmigos1       : [
                            "envName"        : "Dev Amigos1",
                            "urlWebServerDev": "amigos1-invictus.coral.co.uk"
                    ],
                    envDevAmigos2       : [
                            "envName"        : "Dev Amigos2",
                            "urlWebServerDev": "amigos2-invictus.coral.co.uk"
                    ],
                    envDevSpartans1     : [
                            "envName"        : "Dev Spartans1",
                            "urlWebServerDev": "spartans1-invictus.coral.co.uk"
                    ],
                    envDevSpartans2     : [
                            "envName"        : "Dev Spartans2",
                            "urlWebServerDev": "spartans2-invictus.coral.co.uk"
                    ],
                    envDevPioneers1     : [
                            "envName"        : "Dev Pioneers1",
                            "urlWebServerDev": "pioneers1-invictus.coral.co.uk"
                    ],
                    envDevPioneers2     : [
                            "envName"        : "Dev Pioneers2",
                            "urlWebServerDev": "pioneers2-invictus.coral.co.uk"
                    ],
                    envSportsTst1       : [
                            "envName"        : "Dev0 envSportsTst1",
                            "urlWebServerDev": "sports-tst1.coral.co.uk"
                    ],
                    envSportsTst2       : [
                            "envName"        : "Dev0 envSportsTst2",
                            "urlWebServerDev": "sports-tst2.coral.co.uk"
                    ],
                    envSportsStg2       : [
                            "envName"        : "Dev0 envSportsStg2",
                            "urlWebServerDev": "sports-stg2.coral.co.uk"
                    ],
                    envBetHl            : [
                            "envName"        : "Dev0 envBetHl",
                            "urlWebServerDev": "bet-hl.coral.co.uk"
                    ],
                    envDevOmnidev            : [
                            "envName"        : "Dev Omnidev",
                            "urlWebServerDev": "omnidev-invictus.coral.co.uk"
                    ],
                    envDevOmnitest           : [
                            "envName"        : "Dev Omnitest",
                            "urlWebServerDev": "omnitest-invictus.coral.co.uk"
                    ],
                    envDevOmnipreprod        : [
                            "envName"        : "Dev0 Omnipreprod",
                            "urlWebServerDev": "omni_pre_prod-invictus.coral.co.uk"
                    ],
                    envDevUtkarsh1     : [
                            "envName"        : "Dev Utkarsh1",
                            "urlWebServerDev": "utkarsh1-invictus.coral.co.uk"
                    ],
                    envDevfinalspace4           : [
                            "envName"        : "Dev finalspace4",
                            "urlWebServerDev": "finalspace4-invictus.coral.co.uk"
                    ],
                    envDevfinalspace           : [
                            "envName"        : "Dev finalspace",
                            "urlWebServerDev": "finalspace-invictus.coral.co.uk"
                    ],
                    envDevUtkarsh2     : [
                            "envName"        : "Dev Utkarsh2",
                            "urlWebServerDev": "utkarsh2-invictus.coral.co.uk"
                    ],
		    envDevWarriors1     : [
                            "envName"        : "Dev Warriors1",
                            "urlWebServerDev": "warriors1-invictus.coral.co.uk"
                    ],
                    envDevWarriors2     : [
                            "envName"        : "Dev Warriors2",
                            "urlWebServerDev": "warriors2-invictus.coral.co.uk"
                    ]
            ]
    ]
    return constants
}
