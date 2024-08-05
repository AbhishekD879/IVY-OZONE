def call(String operation) {

    def allModules = ['module1', 'module2', 'module3', 'module4', 'module11']

    allModules.each { module ->
        String action = "${operation}:${module}"

        echo("---- ${action.toUpperCase()} ----")
        String command = "echo ${action}"

        script {
            stage(module) {
                sh(command)
            }
        }
    }
}
