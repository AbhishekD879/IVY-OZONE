def call() {

    def constants = [
            awsCoral: [
                    default: [
                            envTypeDeploy     : "dockerAnsible",
                            ansiblePlaybooks  : "common.repoOxygenPlaybook",
                            ansibleInventories: "common.repoAnsibleInventories",
                    ],
                    dev0   : [
                            envName : "AWS Coral dev0",
                            envLevel: "dev0"
                    ],
                    dev1   : [
                            envName : "AWS Coral dev1",
                            envLevel: "dev1"
                    ],
                    dev2   : [
                            envName : "AWS Coral dev2",
                            envLevel: "dev2"
                    ],
                    dev3   : [
                            envName : "AWS Coral dev3",
                            envLevel: "dev3"
                    ],
                    tst0   : [
                            envName : "AWS Coral tst0",
                            envLevel: "tst0"
                    ],
                    tst1   : [
                            envName : "AWS Coral tst1",
                            envLevel: "tst1"
                    ],
                    stg0   : [
                            envName : "AWS Coral stg0",
                            envLevel: "stg0"
                    ],
                    hlv0   : [
                            envName : "AWS Coral hlv0",
                            envLevel: "hlv0"
                    ],
                    hlv1   : [
                            envName : "AWS Coral hlv1",
                            envLevel: "hlv1"
                    ],
                    prd0   : [
                            envName : "AWS Coral prd0",
                            envLevel: "prd0"
                    ]
            ]
    ]
    return constants
}
