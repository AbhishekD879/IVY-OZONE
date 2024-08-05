import os

DOCKER_REPOSITORY = 'docker-registry.crlat.net'

PACKAGE_ROOT_ABS_PATH = os.path.abspath(os.path.dirname(__file__))
DEFAULT_BUILD_ROOT = './tmp'
WEB_ROOT = os.path.join(PACKAGE_ROOT_ABS_PATH, 'certificates/crlat-web-root.crt')