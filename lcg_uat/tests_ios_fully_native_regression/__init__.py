import os

import pytest

import tests
from tests_ios_fully_native_regression.ios_native_settings import IOSNativeSettings
from voltron.environments.hosts import hosts

HOSTNAME = hosts.LADBROKES_PROD
ios_platform_version = 12.1
device_name = 'iPhone X' if not tests.use_browser_stack else tests.mobile_safari_default
ios_app_path = '/Users/Shared'

try:
    HOSTNAME = pytest.config.getoption('hostname')
except Exception:
    pass

location = os.environ.get('LOCATION_NAME', 'IDE')


try:
    device_name = pytest.config.getoption('device_name')
except Exception:
    pass

try:
    ios_app_path = pytest.config.getoption('ios_app_path')
except Exception:
    pass

settings = IOSNativeSettings(environment=HOSTNAME, location=location)
