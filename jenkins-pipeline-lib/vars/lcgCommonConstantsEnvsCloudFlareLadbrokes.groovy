def call() {

    def constants = [
            cloudFlareLadbrokes: [
                    envOtfRedHlv0    : [
                            "envName"           : "One-Two-Free UI CloudFlare HLV0",
                            "envLevel"          : "hlv0",
                            "envTypeDeploy"     : "cloudFlareS3",
                            "cloudFlareZone"    : "ladbrokes.com",
                            "cloudFlareUrl"     : "otf-hlv0.ladbrokes.com",
                            "targetS3Bucket"    : "otf-hlv0.ladbrokes.com",
                            "targetRegion"      : "eu-west-2",
                            "acl"               : "--acl public-read",
                    ],
                    envOtfRedHlv1    : [
                            "envName"           : "One-Two-Free UI CloudFlare HLV1",
                            "envLevel"          : "hlv1",
                            "envTypeDeploy"     : "cloudFlareS3",
                            "cloudFlareZone"    : "ladbrokes.com",
                            "cloudFlareUrl"     : "otf-hlv1.ladbrokes.com",
                            "targetS3Bucket"    : "otf-hlv1.ladbrokes.com",
                            "targetRegion"      : "eu-west-2",
                            "acl"               : "--acl public-read",
                    ],
                    envOtfRedPrd0    : [
                            "envName"           : "One-Two-Free UI CloudFlare PRD0",
                            "envLevel"          : "prd0",
                            "envTypeDeploy"     : "cloudFlareS3",
                            "cloudFlareZone"    : "ladbrokes.com",
                            "cloudFlareUrl"     : "otf.ladbrokes.com",
                            "targetS3Bucket"    : "otf.ladbrokes.com",
                            "targetRegion"      : "eu-west-2",
                            "acl"               : "--acl public-read",
                    ],
            ]
    ]
    return constants
}
