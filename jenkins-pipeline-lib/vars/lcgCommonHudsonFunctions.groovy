import hudson.model.Result
import hudson.model.Run
import jenkins.model.CauseOfInterruption.UserInterruption

/**
 * Aborted previous build
 * Based on https://stackoverflow.com/questions/40760716/jenkins-abort-running-build-if-new-one-is-started
 */

def abortPreviousBuilds() {
    Run previousBuild = currentBuild.rawBuild.getPreviousBuildInProgress()

    while (previousBuild != null) {
        if (previousBuild.isInProgress()) {
            def executor = previousBuild.getExecutor()
            if (executor != null) {
                echo ">> Aborting older build #${previousBuild.number}"
                executor.interrupt(Result.ABORTED, new UserInterruption(
                        "Aborted by newer build #${currentBuild.number}"
                ))
                previousBuild.description = "Aborted by newer build #${currentBuild.number}"
            }
        }
        previousBuild = previousBuild.getPreviousBuildInProgress()
    }
}

/**
 * Cancel the jobs queue except the last one
 * @param jobPatterns
 * example: jobPatterns = '(.*)OXYGEN-UI-DEV-PIPELINE(.*)SDO-(.*)'
 */

def cancelQueueBuilds(List jobPatterns) {

    def queueInstance = Jenkins.instance.queue

    jobPatterns.each { jobName ->
        queue = queueInstance.items.findAll { it.task.name.matches(jobName) }
        println "${jobName}: ${queue}"

        def queueIdsList = []
        queue.each { queueIdsList.add(it.getId()) }
        println "Queue Ids List: ${queueIdsList}"

        if (queueIdsList.size > 1) {
            queueIdsList.sort().take(queueIdsList.size() - 1).each {
                queueInstance.doCancelItem(it)
                println "Build cancel: ${it}"
            }
        } else {
            println "Nothing items in queue to cancel"
        }
    }
}

/**
 * Set allowing concurrent builds
 * @param concurrentKey
 * @return
 */
def jobSetConcurrentBuild(boolean concurrentKey)  {
    println "Set concurent build ${concurrentKey}"
    Job job = $build().getParent()
    job.setConcurrentBuild(concurrentKey)
}

/**
 * Set trigger build when a change is pushed to BitBucket
 *
 */
def jobSetTriggerBitBucket(boolean triggerKey) {
    println "Build when a change is pushed to BitBucket ${triggerKey}"

    def currentProperties = currentBuild.rawBuild.getParent().getProperties()

    if (triggerKey) {
        properties([pipelineTriggers([bitbucketPush()])])
    }
    /*
    else {
        //properties( [pipelineTriggers([])] )
        properties([
                parameters(currentProperties)
        ])
    }
    */
}
