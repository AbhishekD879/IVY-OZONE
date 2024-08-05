from crlat_builder.dockers.base_docker_builder import BaseDockerImageBuilder


class ProxyMockerPython3Based(BaseDockerImageBuilder):
    dockerfile_template = 'base_proxy_mocker.jinja2'
