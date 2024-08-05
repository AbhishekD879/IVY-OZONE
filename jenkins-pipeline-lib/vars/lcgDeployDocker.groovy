def ansible(Map arguments) {

    if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
        lcgCommonFunctions.prettyPrinter(arguments, "lcgDeployDocker.ansible arguments:")
    }

    def envLevel = arguments.envLevel
    def relativePlaybooksDir = lcgCommonFunctions.getGitTargetDirectory(lcgCommonFunctions.getConstantsParameters(arguments.ansiblePlaybooks))
    def relativeInventoriesDir = lcgCommonFunctions.getGitTargetDirectory(lcgCommonFunctions.getConstantsParameters(arguments.ansibleInventories))
    def service = arguments.service
    def deployAnsiblePlaybook = service.deployAnsiblePlaybook
    def deployAnsibleHostsLimit = service.deployAnsibleHostsLimit
    def deployServiceImageTag = service.imageTag
    def deployExtraVarServiceTag = " --extra-vars ${service.deployServiceTag}=${deployServiceImageTag}"
    def deployExtraVars = (service.deployExtraVars.collect { k, v -> "--extra-vars $k=$v" }.join(" ")) + deployExtraVarServiceTag
    def invokeParameters = arguments.invokeParameters ?: false
    def inventoryPath = "${relativeInventoriesDir}/${envLevel}"
    def inventoryPathGlobal = "${relativeInventoriesDir}/global"
    def playbookPath = "${relativePlaybooksDir}/${deployAnsiblePlaybook}"

    if (invokeParameters) {
        this.invokeParameters()
    }

    sh "ansible-playbook -i ./${inventoryPathGlobal}/ -i ./${inventoryPath} ./${playbookPath} -l ${deployAnsibleHostsLimit} ${deployExtraVars}"
}

def invokeParameters() {
    lcgJobParameters.addString("service_image_tag", "", "Service Docker image tag", true)
}

/**
 * Prepare data structure for deploying
 *
 * 1. add to target deployment map info about service into map key service
 * 2. add oxygen-playbooks and lad-ansible-inventories (for Ladbrokes envs) or ansible-inventories for (Coral envs) for SCM pulling
 *    branch name taking from build parameter if it exists or default value from constants
 *
 */

def prepareEnvsList(List deployEnvs, List repositoriesList, Map service) {

    deployEnvs.each {

        if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
            lcgCommonFunctions.prettyPrinter(deployEnvs, "lcgDeployDocker.prepareEnvsList deployEnvs:")
            lcgCommonFunctions.prettyPrinter(repositoriesList, "lcgDeployDocker.prepareEnvsList repositoriesList:")
            lcgCommonFunctions.prettyPrinter(service, "lcgDeployDocker.prepareEnvsList service:")
        }

        it << ["service": service]
        def ansiblePlaybooks = lcgCommonFunctions.getConstantsParameters(it["ansiblePlaybooks"])
        ansiblePlaybooks["branchName"] = params[lcgCommonFunctions.getJobGitRefParameter(ansiblePlaybooks)] ?: lcgCommonFunctions.getGitDefaultBranch(ansiblePlaybooks)
        def ansibleInventories = lcgCommonFunctions.getConstantsParameters(it["ansibleInventories"])
        ansibleInventories["branchName"] = params[lcgCommonFunctions.getJobGitRefParameter(ansibleInventories)] ?: lcgCommonFunctions.getGitDefaultBranch(ansibleInventories)

        repositoriesList << ansiblePlaybooks
        repositoriesList << ansibleInventories
    }
}
