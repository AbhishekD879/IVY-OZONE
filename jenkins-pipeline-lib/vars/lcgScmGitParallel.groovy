def call(List repositories, boolean invokeParameters = true) {

    // Set Job parameters
    if (invokeParameters) {
        lcgScmGit.InvokeParameters(repositories)
    }

    /* Set branch_name based on job parameter or predefined parameters "branchName"
    *  Predefined parameters use for Multibranch job type
    */

    repositories.each {
        if (!it.containsKey("branchName")) {
            it["branchName"] = lcgCommonFunctions.cleanString(env.getProperty(lcgCommonFunctions.getJobGitRefParameter(it)))
        }
    }

    def steps = repositories.collectEntries { [(it['stageName']): { lcgScmGit(it) }] }
    parallel(steps)
}
