/**
 * Deploy to Microsoft IIS through AWS S3 bucket
 */
def awsIisS3(Map arguments) {

    def targetEnv = arguments
    def urlWebServerDev = arguments.urlWebServerDev
    def userWebServerDev = arguments.userWebServerDev
    def pathWebServerDev = arguments.pathWebServerDev
    def artifactS3Bucket = arguments.artifactS3Bucket
    def artifact_name="${env.JOB_NAME}_${env.BUILD_NUMBER}.zip"

    sh """
    cd build/Web/ClientDist/; zip -r ../../../${artifact_name} *; cd -
    aws s3 cp ${artifact_name} s3://${artifactS3Bucket}/\${JOB_NAME}/ --acl bucket-owner-full-control
    """

    def instanceId = lcgAgentAws.getInstanceId(targetEnv)
    def instanceIP = lcgAgentAws.getInstanceIP(targetEnv)
    targetEnv.instanceId = instanceId
    def instancePassword = lcgAgentAws.getInstancePassword(targetEnv)

    sh """
cat <<EOF > deploy.py
import winrm
import sys

commands = [
            "if (test-path \\\$Env:TEMP/${urlWebServerDev}) {rm -r \\\$Env:TEMP/${urlWebServerDev}}",
            "aws s3 cp s3://${artifactS3Bucket}/${env.JOB_NAME}/${artifact_name} \\\$Env:TEMP/",
            "unzip -o -d \\\$Env:TEMP/${urlWebServerDev}/ \\\$Env:TEMP/${artifact_name}",
            "if (!(test-path ${pathWebServerDev}/${urlWebServerDev})) {mkdir ${pathWebServerDev}/${urlWebServerDev}}",
            "if (test-path ${pathWebServerDev}/${urlWebServerDev}) {rm -r ${pathWebServerDev}/${urlWebServerDev}/*}",
            "mv \\\$Env:TEMP/${urlWebServerDev}/* ${pathWebServerDev}/${urlWebServerDev}/",
            "\\\$path = '"'${pathWebServerDev}/${urlWebServerDev}'"'; \\\$acl = Get-Acl -Path \\\$path; \\\$accessrule = New-Object System.Security.AccessControl.FileSystemAccessRule ('Everyone', 'FullControl', 'ContainerInherit', 'ObjectInherit', 'InheritOnly', 'Allow'); \\\$acl.SetAccessRule(\\\$accessrule); Set-Acl -Path \\\$path -AclObject \\\$acl",
            "if (test-path \\\$Env:TEMP/${urlWebServerDev}) {rm -r \\\$Env:TEMP/${urlWebServerDev}}",
            "if (test-path \\\$Env:TEMP/${artifact_name}) {rm \\\$Env:TEMP/${artifact_name}}"
]
            
try:
    session = winrm.Session("${instanceIP}", auth=("${userWebServerDev}", "${instancePassword}"))
    
    for command in commands:    
        run_ps = session.run_ps(command)
        print(command)
        print(run_ps.std_out)
        print(run_ps.status_code)
        
        if run_ps.status_code == 1:
            raise Exception("Deploy failed")
    
except:
    print("Deploy failed")
    sys.exit(1)    
EOF
    """

    sh '''
    cat deploy.py
    python deploy.py
    '''
}

def awsIisRsync(Map arguments) {

    println "lcgDeployIis.directRsync: Env config to deploy: ${arguments}"

    def urlWebServerDev = arguments.urlWebServerDev
    def userWebServerDev = arguments.userWebServerDev
    def hostWebServerDev = lcgAgentAws.getInstanceIP(arguments)
    def pathWebServerDev = arguments.pathWebServerDev
    def artifactName = "${env.JOB_NAME}_${env.BUILD_NUMBER}.zip"

    sh """
    cd build/Web/ClientDist/; zip -r ../../../${artifactName} *; cd -
    """

    sh """
    ssh ${userWebServerDev}@${hostWebServerDev} 'if (test-path \$Env:TEMP/${urlWebServerDev}) {rm -r \$Env:TEMP/${urlWebServerDev}}'
    scp ${artifactName} ${userWebServerDev}@${hostWebServerDev}:\\\$Env:TEMP/${artifactName}
    ssh ${userWebServerDev}@${hostWebServerDev} 'unzip -o -d \$Env:TEMP/${urlWebServerDev}/ \$Env:TEMP/${artifactName}'
    ssh ${userWebServerDev}@${hostWebServerDev} 'if (!(test-path ${pathWebServerDev}/${urlWebServerDev})) {mkdir ${pathWebServerDev}/${urlWebServerDev}}'
    ssh ${userWebServerDev}@${hostWebServerDev} 'if (test-path ${pathWebServerDev}/${urlWebServerDev}) {rm -r ${pathWebServerDev}/${urlWebServerDev}/*}'
    ssh ${userWebServerDev}@${hostWebServerDev} 'mv \$Env:TEMP/${urlWebServerDev}/* ${pathWebServerDev}/${urlWebServerDev}/'
    ssh ${userWebServerDev}@${hostWebServerDev} "\\\$path = '"'${pathWebServerDev}/${urlWebServerDev}'"'; \\\$acl = Get-Acl -Path \\\$path; \\\$accessrule = New-Object System.Security.AccessControl.FileSystemAccessRule ('Everyone', 'FullControl', 'ContainerInherit', 'ObjectInherit', 'InheritOnly', 'Allow'); \\\$acl.SetAccessRule(\$accessrule); Set-Acl -Path \\\$path -AclObject \\\$acl"
    ssh ${userWebServerDev}@${hostWebServerDev} 'if (test-path \$Env:TEMP/${urlWebServerDev}) {rm -r \$Env:TEMP/${urlWebServerDev}}'
    ssh ${userWebServerDev}@${hostWebServerDev} 'if (test-path \$Env:TEMP/${artifactName}) {rm \$Env:TEMP/${artifactName}}'
"""
}
