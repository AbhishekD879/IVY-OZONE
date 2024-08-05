def s3Sync(Map arguments) {

    def targetS3Bucket = arguments.targetS3Bucket
    def targetRegion = arguments.targetRegion
    def service = arguments.service
    def sourcesDir = service.sourcesDir
    def relativeTargetDir = service.relativeTargetDir
    def acl = arguments.acl ?: ""

    sh "aws s3 sync ./${relativeTargetDir}/${sourcesDir}/ s3://${targetS3Bucket}/ --region ${targetRegion} ${acl}"
}

def cloudFrontInvalidation(Map arguments) {

    def distributionId = arguments.distributionId

    sh "echo CloudFront Invalidate"
    sh """
    DISTRIBUTION_ID="${distributionId}"

    echo "Requesting CloudFront cache invalidation, please wait for a while..."
    aws configure set preview.cloudfront true
    INVALIDATION_ID=\$(aws cloudfront create-invalidation --distribution-id \${DISTRIBUTION_ID} --paths '/*' --query 'Invalidation.Id' --output text)
    
    INVALIDATION_STATUS=""
    while [ "\${INVALIDATION_STATUS}" != "Completed" ]; do
        sleep 10
        INVALIDATION_STATUS=\$(aws cloudfront get-invalidation --id \${INVALIDATION_ID} --distribution-id \${DISTRIBUTION_ID} --output text --query Invalidation.Status)
        echo "Invalidation is in a progress INVALIDATION_ID: \${INVALIDATION_ID} DISTRIBUTION_ID:\${DISTRIBUTION_ID}"
    done
    
    aws cloudfront wait invalidation-completed --id \${INVALIDATION_ID} --distribution-id \${DISTRIBUTION_ID} && echo "Invalidation for \${DISTRIBUTION_ID} completed";                    
    """
}

/**
 * Prepare data structure for deploying
 *
 * add to target envs deployment map info about service
 *
 */

def prepareEnvsList(List deployEnvs, Map service) {

    deployEnvs.each {

        if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
            lcgCommonFunctions.prettyPrinter(deployEnvs, "lcgDeployAws.prepareEnvsList deployEnvs:")
            lcgCommonFunctions.prettyPrinter(service, "lcgDeployAws.prepareEnvsList service:")
        }

        it << ["service": service]
    }
}
