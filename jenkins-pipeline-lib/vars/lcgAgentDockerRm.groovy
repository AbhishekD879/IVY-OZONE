def call(String container) {
    sh """
    docker rm -f ${container} || true
    """
}
