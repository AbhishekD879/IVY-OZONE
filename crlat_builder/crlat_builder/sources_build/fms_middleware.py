import logging
import os

import docker

from crlat_builder.constants import DEFAULT_BUILD_ROOT
from crlat_builder.utils.basic_tools import jinja_render
from crlat_builder.utils.git_repo_helper import clone_repository


class FMSMiddlewareSources(object):
    base_name = 'fms_middleware'
    git_repository = 'git@bitbucket.org:symphonydevelopers/oxygen-middleware.git'
    git_default_branch = 'dev'
    build_command = 'gradle clean build'
    src_configs_path = 'src/main/resources'
    dist_path = 'build/libs'
    dist_name = 'oxygen-middleware.jar'

    def __init__(
            self,
            build_root=DEFAULT_BUILD_ROOT,
            git_branch=None
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.wd = os.path.join(build_root, self.base_name, 'sources')
        self.git_branch = git_branch if git_branch else self.git_default_branch

    def git_clone(
            self,
            repository=None,
            branch=None,
            dest_path=None
    ):
        repository = repository if repository else self.git_repository
        branch = branch if branch else self.git_branch
        dest_path = dest_path if dest_path else self.wd
        clone_repository(
            repository,
            branch=branch,
            dest_path=dest_path
        )

    def create_config_profile(
            self,
            profile_name='CRLAT0',
            cms_base_url='https://invictus.coral.co.uk',
            siteserver_base_url='https://backoffice-tst2.coral.co.uk/',
            liveserver_base_url='https://push-tst2.coral.co.uk/push',
            inplay_endpoint='https://oxyms-inplay-dev.symphony-solutions.eu',
            featured_endpoint='https://oxyms-dev.symphony-solutions.eu',
            digital_sports_base_url='https://api.dev.digitalsportstech.com'
    ):
        jinja_render(
            templates_path='templates/app_configs',
            template_name='fms-middleware-application.properties.jinja2',
            destination_path=os.path.join(self.wd, self.src_configs_path),
            # ToDo: decide if we should provide a way to override
            dest_filename='application-%s.properties' % profile_name,
            template_vars={
                'cms_base_url': cms_base_url,
                'siteserver_base_url': siteserver_base_url,
                'liveserver_base_url': liveserver_base_url,
                'inplay_endpoint': inplay_endpoint,
                'featured_endpoint': featured_endpoint,
                'digital_sports_base_url': digital_sports_base_url
            }
        )

    def build_sources(self):
        client = docker.from_env()
        local_path = os.path.abspath(self.wd)
        path_in_docker = '/opt/gradle/sources'
        self.logger.warning('Going to mount "%s" as "%s"' % (local_path, path_in_docker))
        docker_output = client.containers.run(
            'crlat_gradle',
            name='%s_builder' % self.base_name,
            command='gradle clean build',
            volumes={
                local_path: {
                    'bind': path_in_docker
                }
            },
            working_dir=path_in_docker,
            auto_remove=True,
            stream=True,
            stdout=True,
            stderr=True
        )
        for line in docker_output:
            self.logger.debug('Build Output: %s' % line)
        return self.find_dist()

    def find_dist(self):
        dist_absolute_path = os.path.abspath(os.path.join(self.wd, self.dist_path))
        self.logger.debug('Searching for "%s" in "%s"' % (self.dist_name, dist_absolute_path))
        for file in os.listdir(dist_absolute_path):
            if file == self.dist_name:
                return os.path.abspath(os.path.join(dist_absolute_path, self.dist_name))
        raise ValueError('Build distribution not found')
