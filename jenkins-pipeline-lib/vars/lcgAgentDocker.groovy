def bootstrapExec(Map parameters, String paramExec) {

    def build_image = lcgCommonFunctions.getServiceBuildImage(parameters)
    def exportVarsCommand = lcgCommonFunctions.getBuildEnvVarsDockerStyle(parameters)

    sh "docker pull ${build_image}"

    def build_container = sh(returnStdout: true, script: """
        cd sources

        id=\$(id -u)
        userName=\$(whoami)
        image=${build_image}
        workDir=\$(pwd)
        docker run --rm ${exportVarsCommand} -v \${workDir}:/opt/workDir -w /opt/workDir \${image} ${paramExec} /bin/sh -c \
        "if ! which sudo; \
        then \
            which apk && apk --update add bash sudo; \
            which apt-get && apt-get update && apt-get install -y sudo; \
        fi;
        if which apk; \
        then \
            adduser -u \${id} -S \${userName}; \
            adduser \${userName} wheel; \
        else \
            adduser --uid \${id} --system \${userName}; \
            adduser \${userName} sudo; \
        fi;
        echo \${userName}' ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers;"
    """
    ).trim()

    return build_container
}

def build(Map argument) {

    def registry = env.REGISTRY ?: argument.registry
    def runtimeImage = env.SERVICE_RUNTIME_IMAGE ?: argument.runtimeImage
    def branch = env.BRANCH ?: argument.branch
    def tagId = env.TAG_ID ?: argument.tagId
    def relativeTargetDir = lcgCommonFunctions.getGitTargetDirectory(argument)
    relativeTargetDir = (relativeTargetDir.length() > 0) ? relativeTargetDir : "./"

    sh """
cd ${relativeTargetDir}
docker build -t ${registry}/${runtimeImage}:${tagId} --build-arg Revision=${tagId} --build-arg Branch=${branch} .
"""
}

def push(Map argument) {

    def branch = env.BRANCH ?: argument.branch
    def tagId = env.TAG_ID ?: argument.tagId
    def registry = env.REGISTRY ?: argument.registry
    def runtimeImage = env.SERVICE_RUNTIME_IMAGE ?: argument.runtimeImage

    sh """
for IMAGE_TAG in ${branch} ${tagId}
    do     
        docker tag ${registry}/${runtimeImage}:${tagId} ${registry}/${runtimeImage}:\${IMAGE_TAG}
        docker push ${registry}/${runtimeImage}:\${IMAGE_TAG}
        docker rmi ${registry}/${runtimeImage}:\${IMAGE_TAG}
    done
"""
}
