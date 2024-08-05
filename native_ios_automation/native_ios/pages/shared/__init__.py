from native_ios.utils.dialog_action import DialogAction
from appium.webdriver import Remote as WebDriver

_global_driver = None
_global_device = None
_platform = None
_device_properties = None
actions = DialogAction()
_is_iframe_active = None
_cms_config = None


def set_driver_in_main_page():
    global _is_iframe_active
    _is_iframe_active = False


def set_driver_in_iframe():
    global _is_iframe_active
    _is_iframe_active = True


def get_is_driver_in_iframe():
    return _is_iframe_active


def set_device(device):
    global _global_device
    _global_device = device


def get_device():
    return _global_device


def set_driver(driver):
    global _global_driver
    _global_driver = driver


def get_driver() -> WebDriver:
    return _global_driver


def set_platform(platform):
    global _platform
    _platform = platform


def get_platform():
    return _platform


def set_device_properties(properties):
    global _device_properties
    _device_properties = properties


def get_device_properties():
    return _device_properties


def set_cms_settings(env, brand):
    global _cms_config
    from crlat_cms_client.cms_client import CMSClient
    cms_client = CMSClient(env=env, brand=brand)
    _cms_config = cms_client


def get_cms_config():
    return _cms_config
