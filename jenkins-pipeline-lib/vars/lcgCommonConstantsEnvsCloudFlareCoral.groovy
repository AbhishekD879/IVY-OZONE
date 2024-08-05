def call() {

    def constants = [
            cloudFlareCoral: [
                    envOtfHlv0    : [
                            "envName"           : "One-Two-Free UI CloudFlare HLV0",
                            "envLevel"          : "hlv0",
                            "envTypeDeploy"     : "cloudFlareS3",
                            "cloudFlareZone"    : "coral.co.uk",
                            "cloudFlareUrl"     : "otf-hlv0.coral.co.uk",
                            "targetS3Bucket"    : "otf-hlv0.coral.co.uk",
                            "targetRegion"      : "eu-west-2",
                            "acl"               : "--acl public-read",
                    ],
            ]
    ]
    return constants
}
