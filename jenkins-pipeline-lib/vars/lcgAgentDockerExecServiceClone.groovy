def call(Map service, String prefixCloneName, String container, String command) {

    def targetDirClone = lcgCommonFunctions.getCloneSourceDir(service, prefixCloneName)
    def serviceClone = service.clone()
    serviceClone['relativeTargetDir'] = targetDirClone
    def fullCommand = lcgCommonFunctions.commandSudoShInDirDockerStyle(serviceClone, command)
    lcgAgentDockerExec(container, fullCommand)
}
