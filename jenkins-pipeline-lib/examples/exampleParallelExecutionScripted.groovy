def call() {

    def stringsToEcho = ["a", "b", "c", "d"]

    def stepsForParallel = stringsToEcho.collectEntries {
        ["echoing ${it}" : transformIntoStep(it)]
    }
    parallel stepsForParallel
}

def transformIntoStep(inputString) {
    return {
        node ('Build Slave 4'){
            echo inputString
        }
    }
}
