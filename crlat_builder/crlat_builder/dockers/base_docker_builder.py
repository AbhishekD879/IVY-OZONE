import logging
import os

import shutil

import docker

from crlat_builder.constants import WEB_ROOT, DEFAULT_BUILD_ROOT
from crlat_builder.utils.basic_tools import jinja_render, _resources_path


class BaseDockerImageBuilder(object):
    def __init__(
            self,
            image_name='crlat_hello_world',
            build_root=DEFAULT_BUILD_ROOT,
            install_webroot_crt=False,
            dockerfile_params=None,
            clear_destination=True
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.image_name = image_name
        self.__docker_client = None
        self.sources_build_directory = os.path.join(build_root, image_name, 'sources')
        self.docker_build_directory = os.path.join(build_root, image_name, 'docker')
        self.dockerfile_params = dockerfile_params if dockerfile_params else {}
        self.dockerfile_params['install_web_root'] = install_webroot_crt
        self.prepare_docker_dir(clear_destination=clear_destination)

    @property
    def docker_client(self):
        if not self.__docker_client:
            self.__docker_client = docker.from_env()
        return self.__docker_client

    def prepare_docker_dir(self, clear_destination=True):
        """
        Ensure working directory for docker build exists
        :param clear_destination: do recursive delete of WD content
        :type clear_destination: bool
        :returns None
        """
        self.logger.debug('Provision "%s" directory' % self.docker_build_directory)
        if clear_destination and os.path.isdir(self.docker_build_directory):
            shutil.rmtree(self.docker_build_directory, ignore_errors=True)
            os.makedirs(self.docker_build_directory)
        if self.dockerfile_params.get('install_web_root', False):
            os.makedirs(os.path.join(self.docker_build_directory, 'certificates'))
            shutil.copyfile(
                os.path.join(_resources_path(), WEB_ROOT),
                os.path.join(self.docker_build_directory, WEB_ROOT),
            )

    def build_docker_file(
            self,
            template_name=None,
            destination_path=None,
            dockerfile_params=None
    ):
        """
        Builds a Dockerfile based on jinja template
        :param template_name: jinja template name
        :type template_name: str
        :param destination_path: path for to Dockerfile, live unset so the object default docker dir will be used
        :type destination_path: str
        :param dockerfile_params: dict with variables for Jinja template
        :type dockerfile_params: dict
        """
        if template_name is None:
            raise ValueError('Missed "template_name" argument')
        destination_path = destination_path if destination_path else self.docker_build_directory
        dockerfile_params = dockerfile_params if dockerfile_params else {}
        jinja_render(
            template_name=template_name,
            destination_path=destination_path,
            template_vars=dockerfile_params
        )

    def append_resource(self, src_path, dst_path=None):
        """
        Adds a resource and returns a path relative to docker root
        :param src_path: source path
        :type src_path: str
        :param dst_path: destination path
        :type dst_path: str
        :return destination path relative to docker build dir
        :rtype str
        """
        dst_path = os.path.join(self.docker_build_directory, dst_path) if dst_path else self.docker_build_directory
        self.logger.debug('Adding "%s" to docker wd "%s"' % (src_path, dst_path))
        shutil.copytree(
            src_path,
            dst_path,
        )
        local_path = os.path.abspath(dst_path).lstrip(os.path.abspath(self.docker_build_directory)).strip('/')
        dist_filename = os.path.split(src_path)[-1]
        if not local_path.endswith(dist_filename):
            local_path = os.path.join(local_path, dist_filename)
        return local_path

    def build_image(self):
        image = self.docker_client.images.build(
            path=os.path.abspath(self.docker_build_directory),
            tag=self.image_name,
        )
        return image

    def push_image(self, image_name=None, tag=None, repository='docker-registry.crlat.net'):
        """
        Push image to docker repository
        :param image_name: local image name that pushed to docker repository if not provided fallback to self.image_name
        :type image_name: str
        :param tag: tag to push image with, default None value handled by docker lib
        :type tag: str
        :param repository: docker repository name
        :type repository: str
        """
        image_name = image_name if image_name else self.image_name
        image = self.docker_client.images.get(image_name)
        image.tag('%s/%s' % (repository, image_name), tag=tag)
        docker_output = self.docker_client.images.push(
            '%s/%s' % (repository, image_name),
            tag=tag,
            stream=True,
            decode=True
        )
        for line in docker_output:
            self.logger.debug('Push output: %s' % line)
