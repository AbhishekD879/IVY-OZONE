/**
 * senderEmail uses https://wiki.jenkins.io/display/JENKINS/Email-ext+plugin
 * The following plugin provides functionality available through Pipeline-compatible steps.
 * https://jenkins.io/doc/pipeline/steps/email-ext/
 *
 * Map arguments
 * Boolean blueOcean    if true URL Build to BlueOcean
 */

// notifyStarted
def notifyStarted(Map arguments) {
    currentBuild.result = 'STARTED'
    senderEmail(arguments)
}

def notifyStarted(List arguments) {
    currentBuild.result = 'STARTED'
    arguments.each {
        this.setRecipientsListGlobal(it)
        senderEmail(it.notificationsList.email)
    }
}

// notifySuccessful
def notifySuccessful(Map arguments) {
    currentBuild.result = 'SUCCESS'
    senderEmail(arguments)
}

def notifySuccessful(List arguments) {
    currentBuild.result = 'SUCCESS'
    arguments.each {
        this.setRecipientsListGlobal(it)
        senderEmail(it.notificationsList.email)
    }
}

// notifyFailed
def notifyFailed(Map arguments) {
    currentBuild.result = 'FAILURE'
    senderEmail(arguments)
}

def notifyFailed(List arguments) {
    currentBuild.result = 'FAILURE'
    arguments.each {
        this.setRecipientsListGlobal(it)
        senderEmail(it.notificationsList.email)
    }
}

// notifyAborted
def notifyAborted(Map arguments) {
    currentBuild.result = 'ABORTED'
    senderEmail(arguments)
}

def notifyAborted(List arguments) {
    currentBuild.result = 'ABORTED'
    arguments.each {
        this.setRecipientsListGlobal(it)
        senderEmail(it.notificationsList.email)
    }
}

def senderEmail(Map arguments) {

    if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
        lcgCommonFunctions.prettyPrinter(arguments, "lcgNotify.senderEmail: arguments")
    }

    def build_url = env.BUILD_URL
    def blueOcean = arguments.blueOcean ?: true
    def recipientProviders = arguments.recipientProviders ?: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
    def recipientsList = arguments.recipientsList ?: ""

    // deployEnv is deprecated and will be remove in future
    // NEED TO USE envLevel
    def deployEnvDescription = (arguments.deployEnv == null) ? "" : "Environment: ${arguments.deployEnv.toUpperCase()} "
    deployEnvDescription = (arguments.envLevel == null) ? deployEnvDescription : "Environment: ${arguments.envLevel.toUpperCase()} "

    def subject = arguments.subject ?: "${deployEnvDescription}Job: ${currentBuild.fullDisplayName} - ${currentBuild.result}!"
    def build_timestamp = new Date()
    def build_timestamp_string = build_timestamp.format("dd-MMM-yyyy HH:mm:ss")

    if (blueOcean) {
        build_url = env.RUN_DISPLAY_URL
    }

    emailext(
            to: recipientsList,
            subject: subject,
            body: """
                <TABLE>
                <TR><TD align="right">
                </TD><TD valign="center"><B style="font-size: 150%;">BUILD ${currentBuild.result}</B></TD></TR>
                <TR><TD>Build URL</TD><TD><A href="${build_url}">${build_url}</A></TD></TR>
                <TR><TD>Project:</TD><TD>${env.JOB_NAME}</TD></TR>
                <TR><TD>Date of build:</TD><TD>${build_timestamp_string}</TD></TR>
                <TR><TD>Build duration:</TD><TD>${currentBuild.durationString}</TD></TR>
                </TABLE>
            """,
            // recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'CulpritsRecipientProvider'], [$class: 'RequesterRecipientProvider']]
            recipientProviders: recipientProviders
    )
}

/**
 * Set notificationsList.email.recipientsList from common section if it is not defined in environment configuration
 *
 */

def setRecipientsListGlobal(Map arguments) {

    if (lcgCommonFunctions.getConstantsParametersEngine("notificationsList.email.recipientsList", arguments) == null) {
        def recipientsList = lcgCommonFunctions.getEmailRecipientsList(arguments)
        arguments << ["notificationsList": ["email": ["recipientsList": recipientsList]]]
    }

    emailData = arguments.notificationsList.email
    emailData["envLevel"] = arguments.envLevel
    arguments << ["notificationsList": ["email": emailData]]

    if (lcgCommonFunctions.getVerbosityLevel() >= 3) {
        lcgCommonFunctions.prettyPrinter(arguments, "lcgNotify.setRecipientsListGlobal arguments:")
    }

    return arguments
}
