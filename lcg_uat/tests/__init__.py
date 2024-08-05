import os
from tests.voltron_settings import VoltronSettings
from voltron.environments.hosts import hosts
import cmd_config
import logging
from voltron.utils.exceptions.voltron_exception import VoltronException

_logger = logging.getLogger('voltron_logger')
HOSTNAME = hosts.LADBROKES_PROD

mobile_default = 'Galaxy S9'
mobile_safari_default = 'iPhone X'
desktop_safari_default = 'Desktop Safari'
tablet_default = 'iPad'
desktop_default = 'Desktop Chrome'
device_name = mobile_default
default_pixel = 'GOOGLE_PIXEL_8_ANDROID_V14.0_ANDROID'

allow_keep_open = None
cmd_line_env = None
write_chromedriver_log = None
visa_card = None
master_card = None
maestro_card = None
voucher_codes_expired = None
voucher_codes_invalid = None

try:
    # HOSTNAME = pytest.config.getoption('hostname')
    HOSTNAME = cmd_config.hostname
    device_name = cmd_config.device_name
    bs_device_name = cmd_config.browser_stack_device
    use_browser_stack = cmd_config.use_browser_stack
    build_name = cmd_config.build_name
except Exception:
    pass

oxygen_hostname = os.getenv('OX_HOSTNAME')
_logger.info(f"oxygen name set to {oxygen_hostname}")

if oxygen_hostname:
    if not HOSTNAME.upper() == oxygen_hostname.upper():
        HOSTNAME = os.getenv('OX_HOSTNAME')

location = os.environ.get('LOCATION_NAME', 'IDE')

# Please Do Not Push With Changes to Below vars
bs_username = None
bs_access_key = None

try:
    device_name = cmd_config.device_name
    # device_name = pytest.config.getoption('device_name')
except Exception:
    pass

if use_browser_stack:
    desktop_default = "WINDOWS_V11_CHROME"
    mobile_default = 'SAMSUNG_GALAXY_S23_ANDROID_V13.0_ANDROID'
    mobile_safari_default = 'IPHONE_15_IOS_V17_IPHONE'
    desktop_safari_default = 'OS_X_VSNOW_LEOPARD_CHROME'
    tablet_default = 'IPAD_PRO_12.9_2022_IOS_V16_IPAD'
    if location == "AWS_GRID":
        # Service Account Creds
        bs_username = 'lcgjenkinsautomaUXRCU'
        bs_access_key = 'kni8y73ACWNyRdMgosq7'

if use_browser_stack:
    if not bs_username or not bs_access_key:
        raise VoltronException("Browser Stack user Name and Access Key not Set For Local Usage Please Set it in "
                               f"{os.path.realpath(__file__)}")

settings = VoltronSettings(environment=HOSTNAME, location=location)
