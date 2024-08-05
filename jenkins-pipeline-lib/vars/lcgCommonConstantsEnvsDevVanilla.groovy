def call() {

    def constants = [
            iisVanillaDev: [
                    default      : [
                            envTypeDeploy   : "awsIisS3",
                            userWebServerDev: "Administrator",
                            pathWebServerDev: "c:/inetpub",
                            deploymentKey   : "~/.ssh/ansible",
                            awsRegion       : "eu-west-2",
                            awsTagName      : "iis-ui",
                            awsTagEcosystem : "dev",
                            awsTagInstance  : "dev0",
                            artifactS3Bucket: "vanilla-ui-dev"

                    ],
                    envVanilla   : [
                            envName           : "Vanilla",
                            urlWebServerDev   : "vanilla-dev0.coral.co.uk",
                            iisPort           : "8080",
                            iisPortHealthcheck: "7080"
                    ],
                    envAmazing   : [
                            envName           : "Vanilla Amazing",
                            urlWebServerDev   : "amazing-vanilla.coral.co.uk",
                            iisPort           : "8081",
                            iisPortHealthcheck: "7081"
                    ],
                    envBright    : [
                            envName           : "Vanilla Bright",
                            urlWebServerDev   : "bright-vanilla.coral.co.uk",
                            iisPort           : "8082",
                            iisPortHealthcheck: "7082"
                    ],
                    envAvengers  : [
                            envName           : "Vanilla Avengers",
                            urlWebServerDev   : "avengers-vanilla.coral.co.uk",
                            iisPort           : "8083",
                            iisPortHealthcheck: "7083"
                    ],
                    envFantom    : [
                            envName           : "Vanilla Fantom",
                            urlWebServerDev   : "fantom-vanilla.coral.co.uk",
                            iisPort           : "8084",
                            iisPortHealthcheck: "7084"
                    ],
                    envHelium    : [
                            envName           : "Vanilla Helium",
                            urlWebServerDev   : "helium-vanilla.coral.co.uk",
                            iisPort           : "8085",
                            iisPortHealthcheck: "7085"
                    ],
                    envSherwood  : [
                            envName           : "Vanilla Sherwood",
                            urlWebServerDev   : "sherwood-vanilla.coral.co.uk",
                            iisPort           : "8086",
                            iisPortHealthcheck: "7086"
                    ],
                    envUnicorns  : [
                            envName           : "Vanilla Unicorns",
                            urlWebServerDev   : "unicorns-vanilla.coral.co.uk",
                            iisPort           : "8087",
                            iisPortHealthcheck: "7087"
                    ],
                    envCatalyst  : [
                            envName           : "Vanilla Catalyst",
                            urlWebServerDev   : "catalyst-vanilla.coral.co.uk",
                            iisPort           : "8088",
                            iisPortHealthcheck: "7088"
                    ],
                    envKorali    : [
                            envName           : "Vanilla Korali",
                            urlWebServerDev   : "korali-vanilla.coral.co.uk",
                            iisPort           : "8089",
                            iisPortHealthcheck: "7089"
                    ],
                    envMustang   : [
                            envName           : "Vanilla Mustang",
                            urlWebServerDev   : "mustang-vanilla.coral.co.uk",
                            iisPort           : "8090",
                            iisPortHealthcheck: "7090"
                    ],
                    envNative    : [
                            envName           : "Vanilla Native",
                            urlWebServerDev   : "native-vanilla.coral.co.uk",
                            iisPort           : "8091",
                            iisPortHealthcheck: "7091"
                    ],
                    envFinalspace: [
                            envName           : "Vanilla Finalspace",
                            urlWebServerDev   : "finalspace-vanilla.coral.co.uk",
                            iisPort           : "8092",
                            iisPortHealthcheck: "7092"
                    ],
                    envVoltron   : [
                            envName           : "Vanilla Voltron",
                            urlWebServerDev   : "voltron-vanilla.coral.co.uk",
                            iisPort           : "8093",
                            iisPortHealthcheck: "7093"
                    ],
                    envSunny     : [
                            envName           : "Vanilla Sunny",
                            urlWebServerDev   : "sunny-vanilla.coral.co.uk",
                            iisPort           : "8094",
                            iisPortHealthcheck: "7094"
                    ],
                    envSnowy     : [
                            envName           : "Vanilla Snowy",
                            urlWebServerDev   : "snowy-vanilla.coral.co.uk",
                            iisPort           : "8095",
                            iisPortHealthcheck: "7095"
                    ],
                    envPineapple : [
                            envName           : "Vanilla Pineapple",
                            urlWebServerDev   : "pineapple-vanilla.coral.co.uk",
                            iisPort           : "8096",
                            iisPortHealthcheck: "7096"
                    ],
                    /*
                    envBeta    : [
                            envName        : "Vanilla Beta",
                            urlWebServerDev: "beta-vanilla.coral.co.uk",
                            iisPort        : "808222",
                    ],
                    envCatalist: [
                            envName        : "Vanilla Catalist",
                            urlWebServerDev: "catalist-vanilla.coral.co.uk",
                            iisPort        : "8083333",
                    ],
                    envDragons : [
                            envName        : "Vanilla Dragons",
                            urlWebServerDev: "dragons-vanilla.coral.co.uk",
                            iisPort        : "80833333",
                    ]
                    */
            ]
    ]
    return constants
}
