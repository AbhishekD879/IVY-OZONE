#!/usr/bin/env groovy

def call(Map arguments = [:]) {

    def primaryAgentLabel = arguments.primaryAgentLabel
    def deploymentTimeout = arguments.deploymentTimeout ?: 3600
    def brandOrigin = arguments.brandOrigin ?: ""
    def switchPostCleanUpWs = params.clean_ws ?: true
    def versionTag = params.version_tag
    def bmaEnvProfile = params.env_profile ?: ""
    def cmsEnvProfile = params.cms_env_profile ?: ""
    def cmsAot = params.cms_aot ?: false
    def jobsList = [:]

    params.each { key, value ->
        if (value && key =~ /.*-Deployment$|.*-Build$/ ) {
            jobsList.put("${key}", {
                timeout(time: deploymentTimeout, unit: 'SECONDS') {
                    build job: "${key}",
                            parameters: [
                                    string(name: "brand", value: brandOrigin),
                                    string(name: "service_image_tag", value: versionTag),
                                    string(name: "Container_tag", value: versionTag),
                                    string(name: "ref_bma", value: versionTag),
                                    string(name: "env_profile", value: bmaEnvProfile),
                                    string(name: "ref_oxygen_cms_ui", value: versionTag),
                                    string(name: "cms_env_profile", value: cmsEnvProfile),
                                    booleanParam(name: "aot", value: cmsAot)
                            ]
                }
            }
            )
        }
    }

    println "Build parameters:\n================="
    println("Version Tag: ${versionTag}")
    println("Jobs list for deploying: ${jobsList}")

    pipeline {
        agent {
            node {
                label primaryAgentLabel
            }
        }
        stages {
            stage("Deploy") {
                steps {
                    script {
                        currentBuild.description = "Version tag: ${versionTag}"
                        parallel(jobsList)
                    }
                }
            }
        }
        post {
            cleanup {
                script {
                    if (switchPostCleanUpWs) {
                        cleanWs()
                    }
                }
            }
        }
    }
}
