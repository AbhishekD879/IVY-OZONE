from native_ios.device.android_local_emulator import AndroidLocalEmulator
from native_ios.device.browserstack_emulator import BrowserStackLocalEmulator
from native_ios.device.ios_local_emulator import IosLocalEmulator
import tests_ios_fully_native_regression as tests


class DeviceManager(object):

    def __init__(self, location='IDE', proxy=None, **kwargs):
        self.location_name = location
        if tests.platform.upper() == "ANDROID":
            self.device = AndroidLocalEmulator()
        elif tests.platform.upper() == "IOS":
            self.device = IosLocalEmulator()
        elif tests.platform.upper() == "BROWSER_STACK":
            self.device = BrowserStackLocalEmulator(test_name=kwargs.get('test_name'))

    def get_device(self):
        return self.device
