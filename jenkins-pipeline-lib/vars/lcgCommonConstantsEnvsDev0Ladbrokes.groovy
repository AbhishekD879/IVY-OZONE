def call() {

    def constants = [
            nginxLadbrokesDev0: [
                    default         : [
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
                    envDevExcalibur : [
                            "envName"        : "Dev0 Ladbrokes Excalibur",
                            "urlWebServerDev": "excalibur.ladbrokes.com"
                    ],
                    envDevWizards1  : [
                            "envName"        : "Dev0 Ladbrokes Wizards1",
                            "urlWebServerDev": "wizards1-excalibur.ladbrokes.com"
                    ],
                    envDevWizards2  : [
                            "envName"        : "Dev0 Ladbrokes Wizards2",
                            "urlWebServerDev": "wizards2-excalibur.ladbrokes.com"
                    ],
                    envDevWizards3  : [
                            "envName"        : "Dev0 Ladbrokes Wizards3",
                            "urlWebServerDev": "wizards3-excalibur.ladbrokes.com"
                    ],
                    envDevDragons1  : [
                            "envName"        : "Dev0 Ladbrokes Dragons1",
                            "urlWebServerDev": "dragons1-excalibur.ladbrokes.com"
                    ],
                    envDevDragons2  : [
                            "envName"        : "Dev0 Ladbrokes Dragons2",
                            "urlWebServerDev": "dragons2-excalibur.ladbrokes.com"
                    ],
                    envDevDragons3  : [
                            "envName"        : "Dev0 Ladbrokes Dragons3",
                            "urlWebServerDev": "dragons3-excalibur.ladbrokes.com"
                    ],
                    envDevMustang   : [
                            "envName"        : "Dev0 Ladbrokes Mustang",
                            "urlWebServerDev": "mustang-excalibur.ladbrokes.com"
                    ],
                    envDevAvengers  : [
                            "envName"        : "Dev0 Ladbrokes Avengers",
                            "urlWebServerDev": "avengers-excalibur.ladbrokes.com"
                    ],
                    envDevKorali    : [
                            "envName"        : "Dev0 Ladbrokes Korali",
                            "urlWebServerDev": "korali-excalibur.ladbrokes.com"
                    ],
                    envDevFantom    : [
                            "envName"        : "Dev0 Ladbrokes Fantom",
                            "urlWebServerDev": "fantom-excalibur.ladbrokes.com"
                    ],
                    envDevRooney    : [
                            "envName"        : "Dev0 Ladbrokes Rooney",
                            "urlWebServerDev": "rooney-excalibur.ladbrokes.com"
                    ],
                    envDevVoyager   : [
                            "envName"        : "Dev0 Ladbrokes Voyager",
                            "urlWebServerDev": "voyager-excalibur.ladbrokes.com"
                    ],
                    envDevMuckers2  : [
                            "envName"        : "Dev0 Ladbrokes Muckers2",
                            "urlWebServerDev": "muckers2-excalibur.ladbrokes.com"
                    ],
                    envDevMuckers3  : [
                            "envName"        : "Dev0 Ladbrokes Muckers3",
                            "urlWebServerDev": "muckers3-excalibur.ladbrokes.com"
                    ],
                    envDevMuckers4  : [
                            "envName"        : "Dev0 Ladbrokes Muckers4",
                            "urlWebServerDev": "muckers4-excalibur.ladbrokes.com"
                    ],
                    envDevMuckers5  : [
                            "envName"        : "Dev0 Ladbrokes Muckers5",
                            "urlWebServerDev": "muckers5-excalibur.ladbrokes.com"
                    ],
                    envDevMuckers6  : [
                            "envName"        : "Dev0 Ladbrokes Muckers6",
                            "urlWebServerDev": "muckers6-excalibur.ladbrokes.com"
                    ],
                    envDevMustangNew: [
                            "envName"        : "Dev0 Ladbrokes MustangNew",
                            "urlWebServerDev": "mustang-new-excalibur.ladbrokes.com"
                    ],
                    envDevMustang2  : [
                            "envName"        : "Dev0 Ladbrokes Mustang2",
                            "urlWebServerDev": "mustang2-excalibur.ladbrokes.com"
                    ],
                    envDevMustang3  : [
                            "envName"        : "Dev0 Ladbrokes Mustang3",
                            "urlWebServerDev": "mustang3-excalibur.ladbrokes.com"
                    ],
                    envDevMustang4  : [
                            "envName"        : "Dev0 Ladbrokes Mustang4",
                            "urlWebServerDev": "mustang4-excalibur.ladbrokes.com"
                    ],
                    envDevMustang5  : [
                            "envName"        : "Dev0 Ladbrokes Mustang5",
                            "urlWebServerDev": "mustang5-excalibur.ladbrokes.com"
                    ],
                    envDevExpress   : [
                            "envName"        : "Dev0 Ladbrokes Express",
                            "urlWebServerDev": "express-excalibur.ladbrokes.com"
                    ],
                    envDevAvengers2 : [
                            "envName"        : "Dev0 Ladbrokes Avengers2",
                            "urlWebServerDev": "avengers2-excalibur.ladbrokes.com"
                    ],
                    envDevAvengers3 : [
                            "envName"        : "Dev0 Ladbrokes Avengers3",
                            "urlWebServerDev": "avengers3-excalibur.ladbrokes.com"
                    ],
                    envDevHulk      : [
                            "envName"        : "Dev0 Ladbrokes Hulk",
                            "urlWebServerDev": "hulk-excalibur.ladbrokes.com"
                    ],
                    envDevMarvel    : [
                            "envName"        : "Dev0 Ladbrokes Marvel",
                            "urlWebServerDev": "marvel-excalibur.ladbrokes.com"
                    ],
                    envDevFantom1   : [
                            "envName"        : "Dev0 Ladbrokes Fantom1",
                            "urlWebServerDev": "fantom1-excalibur.ladbrokes.com"
                    ],
                    envDevFantom2   : [
                            "envName"        : "Dev0 Ladbrokes Fantom2",
                            "urlWebServerDev": "fantom2-excalibur.ladbrokes.com"
                    ],
                    envDevFantom3   : [
                            "envName"        : "Dev0 Ladbrokes Fantom3",
                            "urlWebServerDev": "fantom3-excalibur.ladbrokes.com"
                    ],
                    envDevFantom4   : [
                            "envName"        : "Dev0 Ladbrokes Fantom4",
                            "urlWebServerDev": "fantom4-excalibur.ladbrokes.com"
                    ],
                    envDevFantom5   : [
                            "envName"        : "Dev0 Ladbrokes Fantom5",
                            "urlWebServerDev": "fantom5-excalibur.ladbrokes.com"
                    ],
                    envDevFantom6   : [
                            "envName"        : "Dev0 Ladbrokes Fantom6",
                            "urlWebServerDev": "fantom6-excalibur.ladbrokes.com"
                    ],
                    envDevCherry    : [
                            "envName"        : "Dev0 Ladbrokes Cherry",
                            "urlWebServerDev": "cherry-invictus.ladbrokes.com"
                    ],
                    envDevSunny     : [
                            "envName"        : "Dev0 Ladbrokes Sunny",
                            "urlWebServerDev": "sunny-invictus.ladbrokes.com"
                    ],
                    envDevRainy     : [
                            "envName"        : "Dev0 Ladbrokes Rainy",
                            "urlWebServerDev": "rainy-invictus.ladbrokes.com"
                    ],
                    envDevSnowy     : [
                            "envName"        : "Dev0 Ladbrokes Snowy",
                            "urlWebServerDev": "snowy-invictus.ladbrokes.com"
                    ],
                    envDevGrim      : [
                            "envName"        : "Dev0 Ladbrokes Grim",
                            "urlWebServerDev": "grim-invictus.ladbrokes.com"
                    ],
                    envDevBrave     : [
                            "envName"        : "Dev0 Ladbrokes Brave",
                            "urlWebServerDev": "brave-invictus.ladbrokes.com"
                    ],
                    envDevPineapple : [
                            "envName"        : "Dev0 Ladbrokes Pineapple",
                            "urlWebServerDev": "pineapple-invictus.ladbrokes.com"
                    ],
                    envDevStrawberry: [
                            "envName"        : "Dev0 Ladbrokes Strawberry",
                            "urlWebServerDev": "strawberry-invictus.ladbrokes.com"
                    ],
                    envDevRaspberry : [
                            "envName"        : "Dev0 Ladbrokes Raspberry",
                            "urlWebServerDev": "raspberry-invictus.ladbrokes.com"
                    ],
                    envDevWatermelon: [
                            "envName"        : "Dev0 Ladbrokes Watermelon",
                            "urlWebServerDev": "watermelon-invictus.ladbrokes.com"
                    ],
                    envDevNitro     : [
                            "envName"        : "Dev0 Ladbrokes Nitro",
                            "urlWebServerDev": "nitro-excalibur.ladbrokes.com"
                    ],
                    envDevNitro2    : [
                            "envName"        : "Dev0 Ladbrokes Nitro2",
                            "urlWebServerDev": "nitro2-excalibur.ladbrokes.com"
                    ],
                    envDevNitro3    : [
                            "envName"        : "Dev0 Ladbrokes Nitro3",
                            "urlWebServerDev": "nitro3-excalibur.ladbrokes.com"
                    ],
                    envDevNitro4    : [
                            "envName"        : "Dev0 Ladbrokes Nitro4",
                            "urlWebServerDev": "nitro4-excalibur.ladbrokes.com"
                    ],
                    envDevNitro5    : [
                            "envName"        : "Dev0 Ladbrokes Nitro5",
                            "urlWebServerDev": "nitro5-excalibur.ladbrokes.com"
                    ],
                    envDevNitro6    : [
                            "envName"        : "Dev0 Ladbrokes Nitro6",
                            "urlWebServerDev": "nitro6-excalibur.ladbrokes.com"
                    ],
                    envDevDevops        : [
                            "envName"        : "Dev0 Ladbrokes Devops",
                            "urlWebServerDev": "devops-excalibur.ladbrokes.com"
                    ],
                    envSportsRedTst1        : [
                            "envName"        : "Dev0 envSportsRedTst1",
                            "urlWebServerDev": "sports-red-tst1.ladbrokes.com"
                    ],
                    envDevOmnidev            : [
                            "envName"        : "Dev Omnidev",
                            "urlWebServerDev": "omnidev-excalibur.ladbrokes.com"
                    ],
                    envDevOmnitest           : [
                            "envName"        : "Dev Omnitest",
                            "urlWebServerDev": "omnitest-excalibur.ladbrokes.com"
                    ],
                    envDevOwebperf           : [
                            "envName"        : "Dev webperf",
                            "urlWebServerDev": "webperf-excalibur.ladbrokes.com"
                    ],
                    envDevfinalspace           : [
                            "envName"        : "Dev finalspace",
                            "urlWebServerDev": "finalspace-excalibur.ladbrokes.com"
                    ],
                    envDevfinalspace1           : [
                            "envName"        : "Dev finalspace1",
                            "urlWebServerDev": "finalspace1-excalibur.ladbrokes.com"
                    ],
                    envDevfinalspace2         : [
                            "envName"        : "Dev finalspace2",
                            "urlWebServerDev": "finalspace2-excalibur.ladbrokes.com"
                    ],
                    envDevfinalspace3           : [
                            "envName"        : "Dev finalspace3",
                            "urlWebServerDev": "finalspace3-excalibur.ladbrokes.com"
                    ],
                    envDevfinalspace4           : [
                            "envName"        : "Dev finalspace4",
                            "urlWebServerDev": "finalspace4-excalibur.ladbrokes.com"
                    ],
                    envDevOmnipreprod        : [
                            "envName"        : "Dev0 Omnipreprod",
                            "urlWebServerDev": "omni_pre_prod-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers           : [
                            "envName"        : "Dev Pepper",
                            "urlWebServerDev": "peppers-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers2           : [
                            "envName"        : "Dev Pepper2",
                            "urlWebServerDev": "peppers2-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers3           : [
                            "envName"        : "Dev Pepper3",
                            "urlWebServerDev": "peppers3-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers4           : [
                            "envName"        : "Dev Pepper4",
                            "urlWebServerDev": "peppers4-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers5           : [
                            "envName"        : "Dev Pepper5",
                            "urlWebServerDev": "peppers5-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers6           : [
                            "envName"        : "Dev Pepper6",
                            "urlWebServerDev": "peppers6-excalibur.ladbrokes.com"
                    ],
                    envDevPeppers7           : [
                            "envName"        : "Dev Pepper7",
                            "urlWebServerDev": "peppers7-excalibur.ladbrokes.com"
                    ],
                    envDevAmigos1            : [
                            "envName"        : "Dev Amigos1",
                            "urlWebServerDev": "amigos1-excalibur.ladbrokes.com"
                    ],
                    envDevAmigos2            : [
                            "envName"        : "Dev Amigos2",
                            "urlWebServerDev": "amigos2-excalibur.ladbrokes.com"
                    ],
                    envDevSpartans1            : [
                            "envName"        : "Dev Spartans1",
                            "urlWebServerDev": "spartans1-excalibur.ladbrokes.com"
                    ],
                    envDevSpartans2            : [
                            "envName"        : "Dev Spartans2",
                            "urlWebServerDev": "spartans2-excalibur.ladbrokes.com"
                    ],
                    envDevPioneers1            : [
                            "envName"        : "Dev Pioneers1",
                            "urlWebServerDev": "pioneers1-excalibur.ladbrokes.com"
                    ],
                    envDevPioneers2            : [
                            "envName"        : "Dev Pioneers2",
                            "urlWebServerDev": "pioneers2-excalibur.ladbrokes.com"
                    ],
                    envDevUtkarsh1            : [
                            "envName"        : "Dev Utkarsh1",
                            "urlWebServerDev": "utkarsh1-excalibur.ladbrokes.com"
                    ],
                    envDevUtkarsh2            : [
                            "envName"        : "Dev Utkarsh2",
                            "urlWebServerDev": "utkarsh2-excalibur.ladbrokes.com"
                    ],
		    envDevWarriors1            : [
                            "envName"        : "Dev Warriors1",
                            "urlWebServerDev": "warriors1-excalibur.ladbrokes.com"
                    ],
                    envDevWarriors2            : [
                            "envName"        : "Dev Warriors2",
                            "urlWebServerDev": "warriors2-excalibur.ladbrokes.com"
                    ]
            ]
    ]
    return constants
}
