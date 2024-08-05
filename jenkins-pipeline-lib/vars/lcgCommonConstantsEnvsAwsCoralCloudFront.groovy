def call() {

    def constants = [
            awsCoralCloudFront: [
                    cmsUi: [
                            default: [
                                    envTypeDeploy: "awsCloudFront",
                            ],
                            dev0   : [
                                    envName       : "AWS Coral CloudFront dev0",
                                    distributionId: "EYB07VBUYLE6P",
                                    envLevel      : "dev0",
                                    targetS3Bucket: "cms-api-ui-dev0",
                                    targetRegion  : "eu-west-2"
                            ],
                            dev1   : [
                                    envName       : "AWS Coral CloudFront dev1",
                                    distributionId: "E3Q8D1E866JZW8",
                                    envLevel      : "dev1",
                                    targetS3Bucket: "cms-api-ui-dev1",
                                    targetRegion  : "eu-west-2"
                            ],
                            dev2   : [
                                    envName       : "AWS Coral CloudFront dev2",
                                    distributionId: "E2S32XPXNPOSUY",
                                    envLevel      : "dev2",
                                    targetS3Bucket: "cms-api-ui-dev2",
                                    targetRegion  : "eu-west-2"
                            ],
                            dev3   : [
                                    envName       : "AWS Coral CloudFront dev3",
                                    distributionId: "E89H85QE82N9C",
                                    envLevel      : "dev3",
                                    targetS3Bucket: "cms-api-ui-dev3",
                                    targetRegion  : "eu-west-2"
                            ],
                            tst0   : [
                                    envName       : "AWS Coral CloudFront tst0",
                                    distributionId: "EEPK96PBCALQQ",
                                    envLevel      : "tst0",
                                    targetS3Bucket: "cms-api-ui-tst0",
                                    targetRegion  : "eu-west-2"
                            ],
                            tst1   : [
                                    envName       : "AWS Coral CloudFront tst1",
                                    distributionId: "E3MWND10WIBA9B",
                                    envLevel      : "tst1",
                                    targetS3Bucket: "cms-api-ui-tst1",
                                    targetRegion  : "eu-west-2"
                            ],
                            stg0   : [
                                    envName       : "AWS Coral CloudFront stg0",
                                    distributionId: "E10KUZ1H07EU26",
                                    envLevel      : "stg0",
                                    targetS3Bucket: "cms-api-ui-stg0",
                                    targetRegion  : "eu-west-2"
                            ],
                            hlv0   : [
                                    envName       : "AWS Coral CloudFront hlv0",
                                    distributionId: "E2Q9SNDK3AV4Q2",
                                    envLevel      : "hlv0",
                                    targetS3Bucket: "cms-api-ui-hlv0",
                                    targetRegion  : "eu-west-2"
                            ],
                            hlv1   : [
                                    envName       : "AWS Coral CloudFront hlv1",
                                    distributionId: "E3SKASUS6T64IG",
                                    envLevel      : "hlv1",
                                    targetS3Bucket: "cms-api-ui-hlv1",
                                    targetRegion  : "eu-west-2"
                            ],
                            prd0   : [
                                    envName       : "AWS Coral CloudFront prd0",
                                    distributionId: "EMSC2JFRGL1JS",
                                    envLevel      : "prd0",
                                    targetS3Bucket: "cms-api-ui-prd0",
                                    targetRegion  : "eu-west-2"
                            ]
                    ],
                    sdmFrontendApp: [
                            default: [
                                    envTypeDeploy: "awsCloudFront",
                            ],
                            dev0   : [
                                    envName       : "AWS Coral SDM FrontEnd App CF dev0",
                                    distributionId: "EOHZQYVK5O9YW",
                                    envLevel      : "dev0",
                                    targetS3Bucket: "sdm-frontend-app-dev0/\${CONTEXT}",
                                    targetRegion  : "eu-west-2"
                            ]
                    ]
            ]
    ]
    return constants
}
