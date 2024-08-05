def call(Map parameters, String relativeTargetDir, String otherParameters = "") {

    def s3Bucket = parameters.s3Bucket
    def s3Region = parameters.s3Region
    def command = parameters.defaultEntrypoint
    parameters["relativeTargetDir"] = relativeTargetDir
    def fullCommand = "${command} ${otherParameters}"

    stage("Fortify Code Analysis") {
        try {
            lcgAwsEcrLogin()
            containerFortify = lcgAgentDockerRun(parameters)
            lcgAgentDockerBootstrap(containerFortify)
            lcgAgentDockerExecService(parameters, containerFortify, fullCommand )
            sh """
            cd ${relativeTargetDir}
            BRANCH=\$(git name-rev --name-only HEAD)
            BRANCH=\${BRANCH##*/}
            PROJECT_NAME=\$(git config --local remote.origin.url | sed -n 's#.*/\\([^.]*\\)\\.git#\\1#p')
            S3_REGION="${s3Region}"
            S3_BUCKET="${s3Bucket}"
            aws s3 sync --region \${S3_REGION} reports/ s3://\${S3_BUCKET}/\${PROJECT_NAME}/\${BRANCH} --acl public-read --delete
            """
        }
        finally {
            lcgAgentDockerRm(containerFortify)
        }
    }

    if (otherParameters =~ /^upload_reports*/) {
        stage("Fortify Status Check") {
            def fortify360ServerAddOn = lcgCommonFunctions.getDefaultForifyEndpoint()
            def failJobIfFortifyNotPassed = true
            sh """
            cd ${relativeTargetDir}
            GR='\\033[0;32m'
            RD='\\033[0;31m'
            NC='\\033[0m'
            BRANCH=\$(git name-rev --name-only HEAD)
            BRANCH=\${BRANCH##*/}
            PROJECT_NAME=\$(git config --local remote.origin.url | sed -n 's#.*/\\([^.]*\\)\\.git#\\1#p')
            S3_REGION="${s3Region}"
            S3_BUCKET="${s3Bucket}"
            FAIL_JOB="${failJobIfFortifyNotPassed}"

               (echo "\${BRANCH}" | grep -Eq  release.*) && BUILD_TYPE="release" || BUILD_TYPE="dev"
           
               PROJECT_ID=\$(curl -s "$fortify360ServerAddOn/Fortify360ServerAddOn?action=GetProjectVersionID&project_name=oxy.\${PROJECT_NAME}_\${BUILD_TYPE}&projectversion_name=oxy.\${PROJECT_NAME}_\${BUILD_TYPE}" | grep -oPm1 "(?<=<ProjectID>)[^<]+")
               FORTIFY_ACTION="CheckCriticalIssues"
               FORTIFY_STATUS=\$(curl -s "$fortify360ServerAddOn/Fortify360ServerAddOn?action=\${FORTIFY_ACTION}&project_id=\${PROJECT_ID}" | grep -oPm1 "(?<=<ErrorCode>)[^<]+")
           
               case \${FORTIFY_STATUS} in
                   0)
                       echo -e "\${GR}Fortify: Policy OK!\${NC}"
                   ;;
                   1)
                       echo -e "\${RD}Fortify: ERROR: Policy violation!\${NC}"
                   ;;
                   -1)
                       echo -e "\${RD}Fortify: Still processing!\${NC}"
                       _fortify_check_status
                   ;;
                   -2)
                       echo -e "\${RD}Fortify: Approval needed!\${NC}"
                   ;;
                   -3)
                       echo -e "\${RD}Fortify: ERROR: No upload file or processing error!\${NC}"
                   ;;    
                   -4)
                       echo -e "\${RD}Fortify: ERROR: Server side error, see tomcat log!\${NC}" 
                   ;;    
                   *)
                       echo -e "\${RD}Fortify: ERROR: Unknown exit code: \${FORTIFY_STATUS}\${NC}"
                   ;;
               esac                  
               
               if [ "\${FORTIFY_STATUS}" -ne 0 ] && [ \${FAIL_JOB} = true ]; then
                   aws s3 sync --region \${S3_REGION} reports/ s3://\${S3_BUCKET}/\${PROJECT_NAME}/\${BRANCH} --acl public-read --delete
                   echo "!!! You can find reports there http://\${S3_BUCKET}.s3-website.eu-west-2.amazonaws.com/?prefix=\${PROJECT_NAME}/\${BRANCH} !!!" 
                   exit 1; 
               fi
            """
        }
    }
}
