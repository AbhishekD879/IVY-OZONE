import os

from crlat_builder.sources_build.fms_middleware import FMSMiddlewareSources
from crlat_builder.utils.basic_tools import jinja_render


class QuickbetMicroserviceSources(FMSMiddlewareSources):
    base_name = 'quickbet_microservice'
    git_repository = 'git@bitbucket.org:symphonydevelopers/quickbet-microservice.git'
    git_default_branch = 'develop'
    build_command = 'gradle clean build'
    src_configs_path = 'src/main/resources'
    dist_path = 'build/libs'
    dist_name = 'application-81.0.0.jar'

    def git_clone_quickbet_repo(self):
        self.git_clone(repository=self.git_repository, branch=self.git_default_branch, dest_path=None)

    def create_quickbet_config_profile(self,
            profile_name='CRLAT0',
            siteserver_base_url='https://backoffice-tst2.coral.co.uk/',
            remote_betslip_elasticache_host='remote-betslip-dev0.vegjyb.ng.0001.euw1.cache.amazonaws.com',
            remote_betslip_elasticache_port=6379,
            liveserver_base_url='https://push-tst2.coral.co.uk/push',
            bpp_base_url='https://bp-dev-coral.symphony-solutions.eu/Proxy/',
        ):
        jinja_render(
            templates_path='templates/app_configs',
            template_name='quickbet-microservice-application.properties.jinja2',
            destination_path=os.path.join(self.wd, self.src_configs_path),
            # ToDo: decide if we should provide a way to override
            dest_filename='application-%s.properties' % profile_name,
            template_vars={
                'siteserver_base_url': siteserver_base_url,
                'remote_betslip_elasticache_host': remote_betslip_elasticache_host,
                'remote_betslip_elasticache_port': remote_betslip_elasticache_port,
                'liveserver_base_url': liveserver_base_url,
                'bpp_base_url': bpp_base_url,
            },
        )


