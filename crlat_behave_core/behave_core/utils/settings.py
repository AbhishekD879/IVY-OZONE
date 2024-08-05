import os
import yaml
import logging
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_logging(env_key: str = 'LOCATION_NAME') -> None:
    """Setup logging configuration

    :param env_key: Name of the environtment key
    """
    location = os.getenv(env_key, 'IDE')
    if location:
        config_file_name = 'dev.yaml' if 'AWS' not in location else 'default.yaml'
        path = os.path.join(BASE_DIR, 'resources/logging/', config_file_name)

    try:
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    except Exception:
        default_path = os.path.join(BASE_DIR, 'resources/logging/default.yaml')
        with open(default_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
