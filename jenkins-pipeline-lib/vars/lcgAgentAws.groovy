def getInstanceIP(Map parameters) {

    def awsTagName = parameters.awsTagName
    def awsTagInstance = parameters.awsTagInstance
    def awsTagEcosystem = parameters.awsTagEcosystem
    def awsRegion = parameters.awsRegion

    def instanceIP = sh(returnStdout: true, script: """
        aws ec2 describe-instances --filters "Name=tag:sName,Values=${awsTagName}"  "Name=tag:Environment,Values=${awsTagInstance}" \
        "Name=tag:Ecosystem,Values=${awsTagEcosystem}" --region ${awsRegion} --query 'Reservations[].Instances[].PrivateIpAddress' | \
        jq -r .[0]
    """
    ).trim()
    return instanceIP
}

def getInstanceId(Map parameters) {
    def awsTagName = parameters.awsTagName
    def awsTagInstance = parameters.awsTagInstance
    def awsTagEcosystem = parameters.awsTagEcosystem
    def awsRegion = parameters.awsRegion

    def instanceId = sh(returnStdout: true, script: """
        aws ec2 describe-instances --filters "Name=tag:sName,Values=${awsTagName}"  "Name=tag:Environment,Values=${awsTagInstance}" \
        "Name=tag:Ecosystem,Values=${awsTagEcosystem}" --region ${awsRegion} --query 'Reservations[].Instances[].InstanceId' | \
        jq -r .[0]
    """
    ).trim()
    return instanceId
}

def getInstancePassword(Map parameters) {

    def instanceId = parameters.instanceId
    def deploymentKey = parameters.deploymentKey
    def awsRegion = parameters.awsRegion

    def instancePassword = sh(returnStdout: true, script: """
        aws ec2 get-password-data --instance-id ${instanceId} --priv-launch-key ${deploymentKey} --region ${awsRegion} \
        --query 'PasswordData' | jq -r .
    """
    ).trim()
    return instancePassword
}
