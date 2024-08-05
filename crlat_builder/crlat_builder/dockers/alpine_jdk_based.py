from crlat_builder.dockers.base_docker_builder import BaseDockerImageBuilder


class AlpineJDK8Based(BaseDockerImageBuilder):
    dockerfile_template = 'openjdk8.jinja2'
    pass
