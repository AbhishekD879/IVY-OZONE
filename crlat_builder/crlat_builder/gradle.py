import os
import shutil

import docker
from jinja2 import Environment
from jinja2 import FileSystemLoader


class GradleImage(object):
    def __init__(
            self,
            template_path='./resources/templates/dockerfiles',
            template_name='Dockerfile.jinja2',
            jdk_base_image_name='openjdk',
            jdk_base_image_tag='8-alpine',
            gradle_version='2.9'
    ):
        self.template_path = template_path
        self.template_name = template_name
        self.jdk_base_image_name = jdk_base_image_name
        self.jdk_base_image_tag = jdk_base_image_tag
        self.gradle_version = gradle_version

    def create_dockerfile(
            self,
            dest_path='./tmp',
            clear_dest=True,
            dockerfile_name='Dockerfile'
    ):
        if clear_dest:
            shutil.rmtree(dest_path, ignore_errors=True)
        os.makedirs(dest_path)
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template(self.template_name)
        dockerfile_data = template.render(
            jdk_base_image_name=self.jdk_base_image_name,
            jdk_base_image_tag=self.jdk_base_image_tag,
            gradle_version=self.gradle_version
        )
        file_path = os.path.join(dest_path, dockerfile_name)
        with open(file_path, "w") as fh:
            fh.write(dockerfile_data)
        return file_path

    def build_docker_image(
            self,
            docker_wd='./tmp',
            image_name='crlat_openjdk_gradle'
    ):
        client = docker.from_env()

        image = client.images.build(
            path=docker_wd,
            tag='%s:%s-jdk%s' % (image_name, self.gradle_version, self.jdk_base_image_tag),
            # dockerfile='./tmp/Dockerfile'
        )
        return image