from voltron.device.aws_browser import AwsBrowser
from voltron.device.aws_grid_browser import AwsGridBrowser
from voltron.device.ios_local_emulator import IosLocalEmulator
from voltron.device.local_browser import LocalBrowser
from voltron.device.mac_mini_grid_browser import MacMiniGridBrowser
from voltron.pages.shared import set_device_properties
from voltron.utils.exceptions.device_exception import DeviceException
from voltron.resources.supported_browser_stack_devices import SUPPORTED_BROWSER_STACK_DEVICES


class DeviceManager(object):
    locations = {
        'IDE': {
            'browsers': ['Chrome', 'Firefox', 'Safari'],
            'device_class': LocalBrowser
        },
        'GRID_IDE': {
            'browsers': ['Chrome', 'Firefox', 'Safari'],
            'device_class': LocalBrowser
        },
        'AWS': {
            'browsers': ['Chrome'],
            'device_class': AwsBrowser
        },
        'AWS_GRID': {
            'browsers': ['Chrome'],
            'device_class': AwsGridBrowser},
        'Mac_Mini_GRID': {
            'browsers': ['Safari'],
            'device_class': MacMiniGridBrowser,
        }
    }
    # dp_resolution https://design.google.com/devices/

    supported_devices = {
        'Nexus 5X': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'Android',
            'browser': 'Chrome',
            'dp_resolution': '412x800',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation'
        },
        'iPhone 6 Plus': {
            'type': 'mobile',
            'allow_emulation': True,
            'os': 'iOs',
            'browser': 'Chrome',
            'dp_resolution': '414x808',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/97.0.4692.72 Mobile/15E148 Safari/604.1 Frontend-Automation'
        },
        'iPhone X': {
            'type': 'mobile',
            'allow_emulation': True,
            'os': 'iOs',
            'browser': 'Safari',
            'dp_resolution': '375x812',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) CriOS/97.0.4692.72 Mobile/15E148 Safari/604.1 Frontend-Automation'
        },
        'iPhone XR': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'iOs',
            'browser': 'Chrome',
            'dp_resolution': '375x812',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) CriOS/97.0.4692.72 Mobile/15E148 Safari/604.1 Frontend-Automation'
        },
        'iPhone XS': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'iOs',
            'browser': 'Chrome',
            'dp_resolution': '375x812',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) CriOS/97.0.4692.72 Mobile/15E148 Safari/604.1 Frontend-Automation'
        },
        'Note 4': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'Android',
            'browser': 'Chrome',
            'dp_resolution': '480x853',
            'user-agent': 'Mozilla/5.0 (Linux; Android 5.0.1; SM-N910V Build/LRX22C) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation'
        },
        'Nexus 7': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'Android',
            'browser': 'Chrome',
            'dp_resolution': '600x960',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Frontend-Automation'
        },
        'Galaxy S9': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'Android',
            'browser': 'Chrome',
            'dp_resolution': '544x1110',
            'user-agent': 'Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation'
        },
        'Pixel 2 XL': {
            'type': 'mobile',
            'allow_emulation': False,
            'os': 'Android',
            'browser': 'Chrome',
            'dp_resolution': '412x823',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation'
        },
        'Nexus 10': {
            'type': 'tablet',
            'allow_emulation': False,
            'os': 'Android',
            'browser': 'Chrome',
            'dp_resolution': '800x1280',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Frontend-Automation'
        },
        'iPad': {
            'type': 'tablet',
            'allow_emulation': True,
            'os': 'iOs',
            'browser': 'Chrome',
            'dp_resolution': '768x1024',
            'user-agent': 'Mozilla/5.0 (iPad; CPU OS 14_8 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) CriOS/97.0.4692.72 Mobile/15E148 Safari/604.1 Frontend-Automation'
        },
        'Desktop Chrome': {
            'type': 'desktop',
            'allow_emulation': False,
            'os': 'Mac OS X',
            'browser': 'Chrome',
            'dp_resolution': '1280x720',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Frontend-Automation'
        },
        'Desktop Safari': {
            'type': 'desktop',
            'allow_emulation': False,
            'os': 'Mac OS X',
            'browser': 'Safari',
            'dp_resolution': '1280x1024',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/97.0.4692.72 Safari/537.36 Frontend-Automation'

        },

        'Native Mobile': {
        },
        'iPhone 7': {
            'allow_emulation': True,
            'type': 'mobile',
            'browser': 'Safari',
            'os': 'iOS',
            'os_version': '11.3',
            'bundle_id': None
        }
    }

    def __init__(self, device_name='Galaxy S9', location='IDE', proxy=None, **kwargs):
        run_on_browser_stack = kwargs.get("use_browser_stack", None)
        self.location_name = location
        if run_on_browser_stack:
            device_args = SUPPORTED_BROWSER_STACK_DEVICES.get(device_name)
            if not device_args:
                raise DeviceException('Unsupported Browserstack device: "%s"' % device_name)
            set_device_properties(properties=device_args)
            device_class = self.locations[location].get('device_class', LocalBrowser)
            self.device = device_class(proxy=proxy, **device_args, **kwargs)
        else:
            if device_name not in self.supported_devices:
                raise DeviceException('Unsupported device: "%s"' % device_name)
            device_args = self.supported_devices[device_name]
            if device_name == 'Native Mobile':
                self.device = IosLocalEmulator()
            else:
                browser = device_args['browser'].lower()
                device_args.update({'name': device_name, 'browser': browser})
                set_device_properties(properties=device_args)
                device_class = self.locations[location].get('device_class', LocalBrowser)
                self.device = device_class(proxy=proxy, **device_args, **kwargs)

    def get_device(self):
        return self.device
