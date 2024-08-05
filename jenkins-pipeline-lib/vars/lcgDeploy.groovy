/*
*   Main deploy function
*/

def deploy(List parameters) {

    def stepsForParallel = [:]

    parameters.each {
        switch (it["envTypeDeploy"]) {
            case "nginxRsync":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepNginxRsync(it)]
                break
            case "nginxRsyncAwsDiscoveryHost":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepNginxRsyncAwsDiscoveryHost(it)]
                break
            case "nginxRsyncParallelAwsDiscoveryHost":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepNginxRsyncParallelAwsDiscoveryHost(it)]
                break
            case "nginxRsyncJumpNode":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepNginxRsyncJumpNode(it)]
                break
            case "akamaiCms":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAkamaiCms(it)]
                break
            case "akamaiRsync":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAkamaiRsync(it)]
                break
            case "akamaiRsyncParallel":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAkamaiRsyncParallel(it)]
                break
            case "akamaiAspera":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAkamaiAspera(it)]
                break
            case "akamaiAsperaParallel":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAkamaiAsperaParallel(it)]
                break
            case "dockerAnsible":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAnsibleDocker(it)]
                break
            case "awsCloudFront":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAwsCloudFront(it)]
                break
            case "awsIisS3":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAwsIisS3(it)]
                break
            case "awsIisRsync":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepAwsIisRsync(it)]
                break
            case "cloudFlareS3":
                stepsForParallel << ["Deploy ${it['envName']}": transformIntoStepCloudFlareS3(it)]
                break
        }
    }
    parallel stepsForParallel
}

def transformIntoStepNginxRsync(Map deployEnv) {
    return {
        lcgDeployNginx.directRsync(deployEnv)
    }
}

def transformIntoStepNginxRsyncAwsDiscoveryHost(Map deployEnv) {
    return {
        lcgDeployNginx.directRsyncAwsDiscoveryHost(deployEnv)
    }
}

def transformIntoStepNginxRsyncParallelAwsDiscoveryHost(Map deployEnv) {
    return {
        lcgDeployNginx.directRsyncParallelAwsDiscoveryHost(deployEnv)
    }
}

def transformIntoStepNginxRsyncJumpNode(Map deployEnv) {
    return {
        lcgDeployNginx.jumpNodeRsync(deployEnv)
    }
}

def transformIntoStepAkamaiCms(Map deployEnv) {
    return {
        lcgDeployAkamai.directCms(deployEnv)
    }
}

def transformIntoStepAkamaiRsync(Map deployEnv) {
    return {
        lcgDeployAkamai.directRsync(deployEnv)
    }
}

def transformIntoStepAkamaiRsyncParallel(Map deployEnv) {
    return {
        lcgDeployAkamai.directRsyncParallel(deployEnv)
    }
}

def transformIntoStepAkamaiAspera(Map deployEnv) {
    return {
        lcgDeployAkamai.directAspera(deployEnv)
    }
}

def transformIntoStepAkamaiAsperaParallel(Map deployEnv) {
    return {
        lcgDeployAkamai.directAsperaParallel(deployEnv)
    }
}

def transformIntoStepAnsibleDocker(Map deployEnv) {
    return {
        lcgDeployDocker.ansible(deployEnv)
    }
}

def transformIntoStepAwsCloudFront(Map deployEnv) {
    return {
        lcgDeployAws.s3Sync(deployEnv)
    }
}

def transformIntoStepAwsIisS3(Map deployEnv) {
    return {
        lcgDeployIis.awsIisS3(deployEnv)
    }
}

def transformIntoStepAwsIisRsync(Map deployEnv) {
    return {
        lcgDeployIis.awsIisRsync(deployEnv)
    }
}

def transformIntoStepCloudFlareS3(Map deployEnv) {
    return {
//        lcgDeployCloudFlare.s3Sync(deployEnv)
        lcgDeployAws.s3Sync(deployEnv)
    }
}

/*
*   Post deploy actions
*/

def post(List parameters) {

    def stepsForParallel = [:]

    parameters.each {
        switch (it["envTypeDeploy"]) {
            case "akamaiCms":
                stepsForParallel << ["Purge Akamai cache ${it['envName']}": transformIntoStepAkamaiPostPurgeCache(it)]
                if (it["artifactUpload"]) {
                    stepsForParallel << ["Upload artifact ${it['envName']}": transformIntoStepAkamaiPostUploadArtifact(it)]
                }
                break
            case "akamaiRsync":
                stepsForParallel << ["Purge Akamai cache ${it['envName']}": transformIntoStepAkamaiPostPurgeCache(it)]
                if (it["artifactUpload"]) {
                    stepsForParallel << ["Upload artifact ${it['envName']}": transformIntoStepAkamaiPostUploadArtifact(it)]
                }
                break
            case "akamaiRsyncParallel":
                stepsForParallel << ["Purge Akamai cache ${it['envName']}": transformIntoStepAkamaiPostPurgeCache(it)]
                if (it["artifactUpload"]) {
                    stepsForParallel << ["Upload artifact ${it['envName']}": transformIntoStepAkamaiPostUploadArtifact(it)]
                }
                break
            case "akamaiAspera":
                stepsForParallel << ["Purge Akamai cache ${it['envName']}": transformIntoStepAkamaiPostPurgeCache(it)]
                if (it["artifactUpload"]) {
                    stepsForParallel << ["Upload artifact ${it['envName']}": transformIntoStepAkamaiPostUploadArtifact(it)]
                }
                break
            case "akamaiAsperaParallel":
                stepsForParallel << ["Purge Akamai cache ${it['envName']}": transformIntoStepAkamaiPostPurgeCache(it)]
                if (it["artifactUpload"]) {
                    stepsForParallel << ["Upload artifact ${it['envName']}": transformIntoStepAkamaiPostUploadArtifact(it)]
                }
                break
            case "awsCloudFront":
                stepsForParallel << ["Invalidate ${it['envName']}": transformIntoStepPostAwsCloudFront(it)]
                break
            case "cloudFlareS3":
                stepsForParallel << ["Purge Cloud Flare cache ${it['envName']}": transformIntoStepPostCloudFlare(it)]
                break
        }
    }
    parallel stepsForParallel

}

def transformIntoStepAkamaiPostPurgeCache(Map deployEnv) {
    return {
        lcgDeployAkamai.purgeCache(deployEnv)
    }
}

def transformIntoStepAkamaiPostUploadArtifact(Map deployEnv) {
    return {
        lcgDeployAkamai.uploadArtifact(deployEnv)
    }
}

def transformIntoStepPostAwsCloudFront(Map deployEnv) {
    return {
        lcgDeployAws.cloudFrontInvalidation(deployEnv)
    }
}

def transformIntoStepPostCloudFlare(Map deployEnv) {
    return {
        lcgDeployCloudFlare.purgeCache(deployEnv)
    }
}
