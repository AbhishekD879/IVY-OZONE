def call(String container) {

    sh """
    id=\$(id -u)
    userName=\$(whoami)

    docker exec ${container} sh -c \
    "if ! which sudo; \
        then \
            which apk && apk --update add bash sudo; \
            which apt-get && apt-get --allow-releaseinfo-change update && apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y sudo; \
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
}
