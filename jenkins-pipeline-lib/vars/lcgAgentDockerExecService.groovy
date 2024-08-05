def call(Map parameters, String container, String command) {
    def fullCommand = lcgCommonFunctions.commandSudoShInDirDockerStyle(parameters, command)
    lcgAgentDockerExec(container, fullCommand)
}
