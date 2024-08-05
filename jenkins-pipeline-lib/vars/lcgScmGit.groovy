def call(Map config) {

    def ignoreNotifyCommit = config.ignoreNotifyCommit ?: false
    def credentialsId = lcgCommonFunctions.getConstantsParameters("common.${config.credentialsId}")
    def branchDefault = config.branchDefault ?: config.branch_default
    def branchName = config.branchName ?: branchDefault

    def scmParameters = [$class           : 'GitSCM',
                         branches         : [[name: branchName]],
                         extensions       : [
                                 [$class: 'RelativeTargetDirectory', relativeTargetDir: config.relativeTargetDir],
                                 [$class: 'CheckoutOption', timeout: 60]
                         ],
                         submoduleCfg     : [],
                         userRemoteConfigs: [[url: config.url, credentialsId: credentialsId]]
    ]

    if (ignoreNotifyCommit) {
        scmParameters["extensions"] << [$class: 'IgnoreNotifyCommit']
    }

    if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
        lcgCommonFunctions.prettyPrinter(scmParameters, "lcgScmGit scmParameters:")
    }

    checkout scm: scmParameters
}

def InvokeParameters(List repositories) {
    repositories.each {

        def branchDefault = it.branchDefault ?: it.branch_default
        def jobParameterDescription = it.jobParameterDescription ?: it.job_parameter_description

        lcgJobParameters.addString(lcgCommonFunctions.getJobGitRefParameter(it), branchDefault,
                jobParameterDescription, true)
    }
}
