def call() {

    def constants = [
            awsLadbrokes: [
                    default: [
                            envTypeDeploy     : "dockerAnsible",
                            ansiblePlaybooks  : "common.repoOxygenPlaybook",
                            ansibleInventories: "common.repoLadbrokesAnsibleInventories",
                    ],
                    dev0   : [
                            envName : "AWS Ladbrokes dev0",
                            envLevel: "dev0"
                    ],
                    dev1   : [
                            envName : "AWS Ladbrokes dev1",
                            envLevel: "dev1"
                    ],
                    dev2   : [
                            envName : "AWS Ladbrokes dev2",
                            envLevel: "dev2"
                    ],
                    tst0   : [
                            envName : "AWS Ladbrokes tst0",
                            envLevel: "tst0"
                    ],
                    tst1   : [
                            envName : "AWS Ladbrokes tst1",
                            envLevel: "tst1"
                    ],
                    stg0   : [
                            envName : "AWS Ladbrokes stg0",
                            envLevel: "stg0"
                    ],
                    hlv0   : [
                            envName : "AWS Ladbrokes hlv0",
                            envLevel: "hlv0"
                    ],
                    prd0   : [
                            envName : "AWS Ladbrokes prd0",
                            envLevel: "prd0"
                    ]
            ]
    ]
    return constants
}
