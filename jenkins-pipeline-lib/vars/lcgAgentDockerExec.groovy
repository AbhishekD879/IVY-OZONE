def call(String container, String command) {
    sh """
    docker exec ${container} sh -c \"${command}\"
    """
}
