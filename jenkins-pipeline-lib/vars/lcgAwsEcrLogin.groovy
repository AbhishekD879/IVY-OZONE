def call (String region = 'eu-west-2', String registry = '740335462382') {
    sh("eval \$(aws ecr get-login --region ${region} --registry-ids ${registry})")
}
