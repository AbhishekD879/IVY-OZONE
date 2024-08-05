/**
 * Get Git ID commit
 *
 * @param service Map service parameters
 * @return String Git ID commit
 */

def getGitIdCommit(Map service) {
    def targetDir = lcgCommonFunctions.getGitTargetDirectory(service)
    def IdCommit = powershell(returnStdout: true, script: """
        cd ${targetDir}
        \$commitString = git log -1 | Select-String -Pattern ^commit
        \$commitId = (\$commitString -split(" "))[1]
        Write-Output \$commitId  
    """
    ).trim()
    return IdCommit
}
