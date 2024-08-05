from crlat_builder.dockers.base_docker_builder import BaseDockerImageBuilder
from crlat_builder.utils.basic_tools import jinja_render

class HelloWorld(BaseDockerImageBuilder):

    def build_docker_file(self):
        self.prepare_docker_dir(clear_destination=True)
        jinja_render(
            template_name=self.dockerfile_template,
            destination_path=self.docker_build_directory,
            template_vars=self.dockerfile_params
        )

