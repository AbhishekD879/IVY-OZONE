import logging

import os
from optparse import OptionParser

from crlat_builder.dockers.alpine_jdk_based import AlpineJDK8Based
from crlat_builder.dockers.proxy_mocker import ProxyMockerPython3Based
from crlat_builder.sources_build.fms_middleware import FMSMiddlewareSources
from crlat_builder.sources_build.quickbet_microservice import QuickbetMicroserviceSources

logger = logging.getLogger(__name__)


def build_gradle_image():
    """
    Build Gradle docker image
    """
    gradle = AlpineJDK8Based(
        image_name='crlat_gradle',
        install_webroot_crt=True,
    )
    gradle.build_docker_file(
        template_name='gradle.jinja2',
        dockerfile_params={
            'jdk_base_image_name': 'openjdk',
            'jdk_base_image_tag': '8-alpine',
            'gradle_version': '2.9'
        }
    )
    gradle.build_image()


def build_featured_microservice_middleware():  # FixMe: should accept args for AlpineJDK8Based and FMSMiddlewareSources __init__
    """
    Build Featured microservice middleware docker image
    """
    fms_middleware_src = FMSMiddlewareSources()
    fms_middleware_src.git_clone()
    fms_middleware_src.create_config_profile(
        profile_name='CRLAT0',
        cms_base_url='https://invictus.coral.co.uk',
        siteserver_base_url='https://backoffice-tst2.coral.co.uk/',
        liveserver_base_url='https://push-tst2.coral.co.uk/push',
        inplay_endpoint='https://oxyms-inplay-dev.symphony-solutions.eu',
        featured_endpoint='https://oxyms-dev.symphony-solutions.eu',
        digital_sports_base_url='https://api.dev.digitalsportstech.com'
    )
    fms_jar_file_path = fms_middleware_src.build_sources()

    logger.info(fms_jar_file_path)
    fms_middleware_image = AlpineJDK8Based(
        image_name='fms_middleware',
        install_webroot_crt=True,
    )
    fms_jar_dkr_local_file_path = fms_middleware_image.append_resource(fms_jar_file_path)
    fms_middleware_image.build_docker_file(
        template_name='fms_dockerfile.jinja2',
        dockerfile_params={
            'jdk_base_image_name': 'openjdk',
            'jdk_base_image_tag': '8-alpine',
            'featured_ms': True,
            'install_web_root': True,
            'src_jar': fms_jar_dkr_local_file_path,
            'dst_jar': '/opt/fms-middleware.jar',
            'docker_cmd': '["java", "-jar", "/opt/fms-middleware.jar"]'
        }
    )
    fms_middleware_image.build_image()
    fms_middleware_image.push_image(tag='latest-tst2')


def build_quickbet_microservice():
    """
    Build QuickBet microservice docker image
    """
    qms_microservice_src = QuickbetMicroserviceSources()
    qms_microservice_src.git_clone_quickbet_repo()
    qms_microservice_src.create_quickbet_config_profile()
    qms_jar_file_path = qms_microservice_src.build_sources()
    logger.info(qms_jar_file_path)
    qms_microservice_image = AlpineJDK8Based(
        image_name='quickbet_microservice',
        install_webroot_crt=True,
    )
    qms_jar_dkr_local_file_path = qms_microservice_image.append_resource(qms_jar_file_path)
    qms_microservice_image.build_docker_file(
        template_name='qms_dockerfile.jinja2',
        dockerfile_params={
            'jdk_base_image_name': 'openjdk',
            'jdk_base_image_tag': '8-alpine',
            'install_web_root': True,
            'quickbet_ms': True,
            'src_jar': qms_jar_dkr_local_file_path,
            'dst_jar': '/opt/application.jar',
            'docker_cmd': '["java", "-jar", "/opt/application.jar"]',
        }
    )


def build_yourcall_proxy_mock():
    """
    Builds Yourcall mock docker image
    """
    mocker = ProxyMockerPython3Based(
        image_name='proxy_mocker'
    )
    #TODO append resource is not resolving src path properly, hardcoded in for now in jinja template
    # /Users/maria_godlevska/Documents/work/proxy_mocker
    proxy_mocker_file_path = mocker.append_resource(src_path='/var/lib/go-agent/pipelines/crlat_proxy_mocker/sources',
                                                    dst_path='proxy_mocker')
    mocker.build_docker_file(
        template_name='base_proxy_mocker.jinja2',
        dockerfile_params={
            'script_to_execute': 'run_yc_mock.py',
            'project_source_dir': proxy_mocker_file_path
        }
    )
    mocker.build_image()
    mocker.push_image(tag='latest')


def build_image(**kwargs):
    image = kwargs.get('image_name')
    if not image:
        raise Exception('No image name specified')
    d = {
        'proxy_mocker': build_yourcall_proxy_mock,
        'fms': build_featured_microservice_middleware}
    try:
        d[image]()
    except KeyError:
        raise Exception('Image "%s" is not found among supported images' % image)


def main():
    parser = OptionParser()
    parser.add_option('-i', '--image', dest='image_name',
                      help='image name', default=os.getenv('IMAGE_NAME', None))

    (options, args) = parser.parse_args()

    build_image(image_name=options.image_name)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
