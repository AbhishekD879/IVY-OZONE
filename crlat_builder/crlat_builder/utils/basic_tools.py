import os


import logging
from jinja2 import Environment, FileSystemLoader

from crlat_builder.constants import PACKAGE_ROOT_ABS_PATH

logger = logging.getLogger(__name__)

def _resources_path():
    path = os.path.join(PACKAGE_ROOT_ABS_PATH, 'resources')
    return path

def jinja_render(
        templates_path='templates/dockerfiles',
        template_name='gradle.jinja2',
        destination_path='./tmp',
        dest_filename='Dockerfile',
        template_vars=None
):
    if template_vars is None:
        template_vars = {}
    template_env = os.path.join(_resources_path(), templates_path)
    env = Environment(loader=FileSystemLoader(template_env))
    template = env.get_template(template_name)
    dest_data = template.render(**template_vars)
    file_path = os.path.join(destination_path, dest_filename)

    logger.info(
        'Built a file "%s" based on template "%s"' % (
            file_path,
            os.path.join(template_env, template_name)
        )
    )
    logger.debug('Template vars: %s' % '; '.join(['%s=%s' % (k, v) for k, v in template_vars.items()]))
    with open(file_path, "w") as fh:
        fh.write(dest_data)
    return file_path
