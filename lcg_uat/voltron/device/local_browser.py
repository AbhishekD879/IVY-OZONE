import datetime
import json
import logging
import os
import re
import socket
import subprocess
import typing
from urllib.parse import urlparse
import tests
from urllib.error import URLError
from appium import webdriver as AppiumDriver
from selenium.common.exceptions import InvalidCookieDomainException, WebDriverException
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Firefox as FirefoxDriver
from selenium.webdriver import Safari as SafariDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver as BrowserStackDriver
from voltron.pages.shared import set_device, set_has_hostname_opened, get_device_properties
from voltron.pages.shared import set_driver
from voltron.utils import mixins
from voltron.utils.exceptions.device_exception import DeviceException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_device_uuid_from_xcode
from voltron.utils.js_functions import set_viewport_size
from voltron.utils.waiters import wait_for_result


class LocalBrowser(mixins.LoggingMixin):
    """
    For running locally on Chrome, Safari, Firefox, Safari on real device
    """
    _preserved_performance_log = []
    _chrome_driver = {'type': ChromeDriver}
    _safari_driver = {'type': SafariDriver}
    _firefox_driver = {'type': FirefoxDriver}
    _safari_appium_driver = {'type': AppiumDriver.Remote, 'command_executor': tests.settings.appium_localhost_url}
    _browser_stack_driver = {'type': BrowserStackDriver.Remote, 'command_executor': tests.settings.browser_stack_remote}
    _browser_stack_mobile_driver = {'type': AppiumDriver.Remote,
                                    'command_executor': tests.settings.browser_stack_remote}

    def __init__(
            self,
            ls_cookies=None,
            session_storage_cookies=None,
            cookies=None,
            proxy=None,
            cmd_line_args=None,
            driver_args=None,
            chrome_profile=None,
            blocked_hosts=None,
            **kwargs
    ):
        super(LocalBrowser, self).__init__()
        self.use_browser_stack = kwargs.get("use_browser_stack", False)
        self.enable_bs_performance_log = kwargs.get("enable_bs_performance_log", False)
        self.bs_log_config = kwargs.get("bs_log_config", {
            "networkLogs": False,
            "debug": False,
            "video": False,
            'seleniumLogs': False,
            'appiumLogs': False,
            'console': 'disable'
        })
        self.device_args = kwargs
        self.name = self.device_args.get('name', 'Galaxy S9') if not self.use_browser_stack else self.device_args.get(
            'device', 'Galaxy S9')
        self.type = self.device_args.get('type', 'mobile')
        self.os = self.device_args.get('os', 'Android')
        self.os_version = self.device_args.get('os_version', None)
        self.bundle_id = self.device_args.get('bundle_id', None)
        self.browser = self.device_args.get('browser', 'Chrome')
        self.width, self.height = self.device_args.get('dp_resolution', '544x1110').split('x')
        self.user_agent = self.device_args.get('user-agent', 'Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) '
                                                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation')
        self.ls_cookies = ls_cookies if ls_cookies is not None else {}
        self.session_storage_cookies = session_storage_cookies if session_storage_cookies is not None else {}
        self.cookies = cookies if cookies is not None else (
            {'name': 'empty_automation_cookie', 'value': 'it_does_nothing'},)
        self.proxy = proxy
        self.chrome_profile = chrome_profile
        self.cmd_line_args = cmd_line_args
        self.browser_opts = None
        self.driver_args = driver_args
        self._driver = None
        self.blocked_hosts = blocked_hosts if blocked_hosts else []
        set_device(self)

    @property
    def driver(self):
        if self._driver is None:
            self.start_browser(maximized=False, browser_stack=self.use_browser_stack, browserstack_local=False)
            if self._driver:
                self._driver.implicitly_wait(0)
        return self._driver

    @driver.setter
    def driver(self, value):
        if self._driver is None:
            self.browser = value

    def start_browser(self, maximized=False, browser_stack=False, browserstack_local=False):
        if browser_stack:
            self._driver = self.__start_browser_stack_w3c(maximized=False)
        elif browserstack_local:
            self._driver = self.__start_browser_stack_local(maximized=maximized)
        elif self.browser.lower() == 'chrome':
            self._driver = self.__start_chrome_browser(maximized)
        elif self.browser.lower() == 'firefox':
            self._driver = self.__start_firefox_browser()
        elif self.browser.lower() == 'safari':
            self._driver = self.__start_safari_browser()
        else:  # currently for Safari on iPhone simulator
            self._driver = self.__start_safari_on_appium_browser()

        self._driver.set_page_load_timeout(tests.settings.page_load_timeout)
        set_driver(self._driver)

        build_info_path = 'buildInfo.json'
        self.navigate_to(f'{tests.HOSTNAME}/{build_info_path}')
        wait_for_result(lambda: build_info_path in self._driver.current_url,
                        name=f'"{build_info_path}" to load',
                        timeout=5)
        self.set_cookies()
        self.set_local_storage_cookies(self.ls_cookies)
        self.set_session_storage_cookies(self.session_storage_cookies)

    def __start_chrome_browser(self, maximized):
        self.browser_opts = ChromeOptions()
        desired = DesiredCapabilities.CHROME
        self.add_browser_args(options=self.cmd_line_args)
        self.add_browser_args(options='user-agent=%s' % self.user_agent)
        self.add_browser_args(options='window-size=%s,%s' % (self.width, self.height))
        all_blocked_hosts = tests.settings.blocked_hosts + self.blocked_hosts
        if all_blocked_hosts:
            self.add_browser_args(options=self.prepare_host_rules_option(all_blocked_hosts))
        self.browser_opts.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        self.browser_opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        if self.device_args['allow_emulation']:
            self.browser_opts.add_experimental_option('mobileEmulation', {
                'deviceName': self.name
            })
        self.add_browser_args(options='loggingPrefs=%s' % str({'browser': 'ALL'}))
        desired['goog:loggingPrefs'] = {'performance': 'ALL'}
        desired['acceptInsecureCerts'] = True
        desired['pageLoadStrategy'] = 'none'
        self.browser_opts.add_argument("--allow-running-insecure-content")
        chrome_service = ChromeService(service_args=self._chrome_driver.get('service_args'))
        for key, val in desired.items():
            self.browser_opts.set_capability(key, val)
        if self.proxy is not None:
            self.add_browser_args(options='proxy-server=%s' % self.proxy)
        if self.chrome_profile is not None:
            self.add_browser_args(options='user-data-dir=%s' % self.chrome_profile)
        if self._chrome_driver.get('command_executor'):
            if tests.location == 'AWS_GRID':
                desired['selenoid:options'] = {
                    "enableLog": True
                }
            driver = self._chrome_driver['type'](command_executor=self._chrome_driver['command_executor'],
                                                 options=self.browser_opts)
            # desired_capabilities = desired
        else:
            driver = self._chrome_driver['type'](options=self.browser_opts,
                                                 service=chrome_service)
            # desired_capabilities = desired
            driver.execute_cdp_cmd('Network.setUserAgentOverride',
                                   {"userAgent": self.user_agent})

        if maximized:
            driver.maximize_window()
        return driver

    def __start_firefox_browser(self):
        profile = FirefoxProfile()
        profile.set_preference('devtools.jsonview.enabled', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        self._driver = self._firefox_driver['type'](firefox_profile=profile, desired_capabilities=desired)
        self._driver.set_window_size(self.width, self.height)
        return self._driver

    def __start_safari_browser(self):
        self.set_safari_user_agent(user_agent=self.user_agent)
        desired = DesiredCapabilities.SAFARI
        if self._safari_driver.get('command_executor'):
            self._driver = self._safari_driver['type'](command_executor=self._safari_driver['command_executor'],
                                                       desired_capabilities=desired)
        else:
            self._driver = self._safari_driver['type'](desired_capabilities=desired)
        self._driver.set_window_size(self.width, self.height)
        return self._driver

    def __start_safari_on_appium_browser(self):
        bundle_id = self.bundle_id if self.bundle_id else get_device_uuid_from_xcode(device_name=self.name)
        desired_caps = {
            'safariInitialUrl': 'about:blank',
            'bundleId': bundle_id,
            'platformVersion': self.os_version,
            'platformName': self.os,
            'deviceName': self.name,
            'browserName': self.browser
        }
        try:
            if self._safari_appium_driver.get('command_executor'):
                driver = self._safari_appium_driver['type'](
                    command_executor=self._safari_appium_driver['command_executor'],
                    desired_capabilities=desired_caps,
                    browser_profile=None,
                    proxy=None,
                    keep_alive=False)
            else:
                raise DeviceException('Command executor is not provided for Safari Appium Driver')
        except URLError as e:
            raise DeviceException('Cannot start appium driver. Error:  "URLError: %s"' % e.reason)
        return driver

    def __start_browser_stack(self, maximized=False):
        os.environ['USE_FW_PROXY'] = "true"
        self.browser_opts = ChromeOptions()
        capabilities_map = {
            "firefox": DesiredCapabilities.FIREFOX,
            "opera": DesiredCapabilities.WEBKITGTK,
            "chrome": DesiredCapabilities.CHROME,
            "ie": DesiredCapabilities.INTERNETEXPLORER,
            "edge": DesiredCapabilities.EDGE,
            "safari": DesiredCapabilities.SAFARI,
            "iphone": DesiredCapabilities.IPHONE,
            "ipad": DesiredCapabilities.IPAD,
            "android": DesiredCapabilities.CHROME,
            "samsung": DesiredCapabilities.CHROME
        }
        desired = capabilities_map.get(self.browser, DesiredCapabilities.CHROME)
        self.add_browser_args(options=self.cmd_line_args)
        if (self.type == 'mobile' and not 'iPhone' in self.device_args.get('device')) or (self.type == 'desktop'):
            self.add_browser_args(options='user-agent=%s' % self.user_agent)
        else:
            if self.bs_log_config.get('networkLogs'):
                desired['browserstack.networkLogs'] = self.bs_log_config.get('networkLogs')
                desired['browserstack.networkLogsOptions'] = {
                    'captureContent': self.bs_log_config.get('networkLogs'),
                }
        # self.add_browser_args(options='window-size=%s,%s' % (self.width, self.height))
        all_blocked_hosts = tests.settings.blocked_hosts + self.blocked_hosts
        if all_blocked_hosts:
            self.add_browser_args(options=self.prepare_host_rules_option(all_blocked_hosts))
        self.browser_opts.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        if (get_device_properties()['browser'].lower() in ['safari', 'chromium'] and
                    'iphone' in get_device_properties()['device'].lower()):
            desired['browserstack.headerParams'] = json.dumps({
                "User-Agent": self.user_agent
            })
        self.browser_opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        desired['acceptSslCerts'] = True
        desired['pageLoadStrategy'] = 'none'
        desired['browserstack.geoLocation'] = 'GB'
        desired['browserstack.idleTimeout'] = '300'
        desired['browserstack.debug'] = self.bs_log_config.get('debug', False)
        desired['browserstack.video'] = self.bs_log_config.get('video', False)
        # Reverting to default
        # desired['browserstack.seleniumLogs'] = self.bs_log_config.get('seleniumLogs', False)
        # desired['browserstack.appiumLogs'] = self.bs_log_config.get('appiumLogs', False)
        desired['browserstack.console'] = self.bs_log_config.get('console', False)
        if self.enable_bs_performance_log:
            desired['enablePerformanceLogging'] = False if self.type == 'mobile' and 'iPhone' in self.device_args.get(
                'device') else True
        desired['disableAndroidSoftKeyboard'] = True
        desired['interactiveDebugging'] = True
        desired['browserName'] = self.device_args.get('browser')
        desired['os'] = self.os.upper()
        desired['os_version'] = self.device_args.get('os_version')
        desired['device'] = self.name
        desired['framework'] = 'pytest'

        if tests.location == "AWS_GRID":
            logging.info(f"Local browser Build name: {tests.build_name}")
            if tests.build_name and tests.build_name != "None":
                ci_run_number = os.environ.get('BUILD_NUMBER', None)
                desired['build'] = f"{tests.build_name} BUILD_NUMBER:{ci_run_number}"
            else:
                ci_run_name = os.environ.get('JOB_NAME', None)
                ci_run_number = os.environ.get('BUILD_NUMBER', None)
                git_branch = os.environ.get('GIT_BRANCH', None)
                hostname = os.environ.get('OX_HOSTNAME', None)
                test_run_name = f'Automation Run {ci_run_name} BUILD_NUMBER:{ci_run_number}{f" [{git_branch}]" if git_branch else ""} @ {hostname}'
                desired['build'] = test_run_name
        else:
            if tests.build_name:
                desired['build'] = tests.build_name
        if self.proxy is not None:
            self.add_browser_args(options='proxy-server=%s' % self.proxy)
        if self.chrome_profile is not None:
            self.add_browser_args(options='user-data-dir=%s' % self.chrome_profile)
        try:
            if self._browser_stack_driver.get('command_executor'):
                desired['resolution'] = '1280x800'
                driver = self._browser_stack_driver['type'](
                    command_executor=self._browser_stack_driver['command_executor'].format(
                        username=tests.bs_username,
                        access_key=tests.bs_access_key),
                    desired_capabilities=desired,
                    options=self.browser_opts,
                    keep_alive=True)
            else:
                raise DeviceException('Command executor is not provided for BrowserStack')
        except URLError as e:
            raise DeviceException('Cannot start appium driver. Error:  "URLError: %s"' % e.reason)
        if maximized:
            driver.maximize_window()
        return driver

    def __start_browser_stack_w3c(self, maximized=False):
        os.environ['USE_FW_PROXY'] = "true"

        options = None

        if self.browser == 'firefox':
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            options = FirefoxOptions()
        elif self.browser in ['chrome', 'chromium']:
            options = ChromeOptions()
        elif self.browser == 'ie':
            from selenium.webdriver.ie.options import Options as IEOptions
            options = IEOptions()
        elif self.browser == 'edge':
            from selenium.webdriver.edge.options import Options as EdgeOptions
            options = EdgeOptions()
        elif self.browser == 'safari':
            from selenium.webdriver.safari.options import Options as SafariOptions
            options = SafariOptions()
        elif self.browser in ['iphone', 'ipad', 'android', 'samsung']:
            options = ChromeOptions()
        else:
            raise DeviceException('Unsupported browser type')

        # Add custom options
        # self.add_browser_args(options=options)
        if (self.type == 'mobile' and 'iPhone' not in self.device_args.get('device')) or (self.type == 'desktop'):
            options.add_argument('user-agent=%s' % self.user_agent)
        else:
            if self.bs_log_config.get('networkLogs'):
                bstack_options = {
                    'networkLogs': self.bs_log_config.get('networkLogs'),
                    'networkLogsOptions': {
                        'captureContent': self.bs_log_config.get('networkLogs'),
                    }
                }
                options.set_capability('bstack:options', bstack_options)

        all_blocked_hosts = tests.settings.blocked_hosts + self.blocked_hosts
        if all_blocked_hosts:
            options.add_argument(self.prepare_host_rules_option(all_blocked_hosts))

        options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })

        if (get_device_properties()['browser'].lower() in ['safari', 'chromium'] and
                'iphone' in get_device_properties()['device'].lower()):
            bstack_options = {
                'headerParams': json.dumps({
                    "User-Agent": self.user_agent
                })
            }
            options.set_capability('bstack:options', bstack_options)

        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # Set BrowserStack capabilities
        bstack_options = {
            'geoLocation': 'GB',
            'idleTimeout': '300',
            'debug': self.bs_log_config.get('debug', False),
            'video': self.bs_log_config.get('video', False),
            'consoleLogs': self.bs_log_config.get('console', False),
            'os': self.os.upper(),
            'osVersion': self.device_args.get('os_version'),
            'browserName': self.device_args.get('browser'),
            'interactiveDebugging': True,
            "telemetryLogs": True,
            'disableCorsRestrictions': True,
            'wsLocalSupport': True,
            "selfHeal": "true",
            "seleniumCdp": True
        }
        if self.type == 'mobile':
            bstack_options['deviceName'] = self.name

        if self.enable_bs_performance_log:
            options.set_capability('chromeOptions', {
                'perfLoggingPrefs': {
                    'enableNetwork': True,
                    'enablePage': True,
                    'enableTimeline': True,
                    'traceCategories': 'devtools.timeline,devtools.network,devtools.cpu'
                }
            })
            options.set_capability('enablePerformanceLogging',
                                   False if self.type == 'mobile' and 'iPhone' in self.device_args.get(
                                       'device') else True)

            options.add_argument(f'loggingPrefs={str({'browser': 'ALL'})}')
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            options.set_capability('acceptInsecureCerts', True)
            options.set_capability('pageLoadStrategy', 'none')
            options.set_capability('ignoreCertificateErrors', True)
            options.add_argument("--allow-running-insecure-content")

        if tests.location == "AWS_GRID":
            if tests.build_name and tests.build_name != "None":
                ci_run_number = os.environ.get('BUILD_NUMBER', None)
                bstack_options['buildName'] = f"{tests.build_name} BUILD_NUMBER:{ci_run_number}"
            else:
                ci_run_name = os.environ.get('JOB_NAME', None)
                ci_run_number = os.environ.get('BUILD_NUMBER', None)
                git_branch = os.environ.get('GIT_BRANCH', None)
                hostname = os.environ.get('OX_HOSTNAME', None)
                test_run_name = f'Automation Run {ci_run_name} BUILD_NUMBER:{ci_run_number}{f" [{git_branch}]" if git_branch else ""} @ {hostname}'
                bstack_options['buildName'] = test_run_name
        else:
            if tests.build_name:
                bstack_options['buildName'] = tests.build_name

        if self.proxy is not None:
            options.add_argument(f'proxy-server={self.proxy}')
        if self.chrome_profile is not None:
            options.add_argument(f'user-data-dir={self.chrome_profile}')

        options.set_capability('bstack:options', bstack_options)

        try:
            if self._browser_stack_driver.get('command_executor'):
                bstack_options['resolution'] = '1280x800'
                driver = self._browser_stack_driver.get('type')(
                    command_executor=self._browser_stack_driver['command_executor'].format(
                        username=tests.bs_username,
                        access_key=tests.bs_access_key
                    ),
                    options=options
                )
                # TODO:Look into bidi and cdp protocol support
                # async with driver.bidi_connection() as connection:
                #     connection.network
                # driver.execute_cdp_cmd('Network.setUserAgentOverride',
                #                        {"userAgent": self.user_agent})
                # driver.execute_cdp_cmd('Network.enable')
            else:
                raise DeviceException('Command executor is not provided for BrowserStack')
        except WebDriverException as e:
            raise DeviceException(f'Cannot start WebDriver. Error: {e}')

        if maximized:
            driver.maximize_window()

        return driver

    def __start_browser_stack_local(self, maximized=False):
        self.browser_opts = ChromeOptions()
        desired = DesiredCapabilities.CHROME
        self.add_browser_args(options=self.cmd_line_args)
        self.add_browser_args(options='user-agent=%s' % self.user_agent)
        # self.add_browser_args(options='window-size=%s,%s' % (self.width, self.height))
        all_blocked_hosts = tests.settings.blocked_hosts + self.blocked_hosts
        if all_blocked_hosts:
            self.add_browser_args(options=self.prepare_host_rules_option(all_blocked_hosts))
        self.browser_opts.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        self.browser_opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        # if self.device_args['allow_emulation']:
        #     self.browser_opts.add_experimental_option('mobileEmulation', {
        #         'deviceName': self.name
        #     })
        self.add_browser_args(options='loggingPrefs=%s' % str({'browser': 'ALL'}))
        desired['goog:loggingPrefs'] = {'performance': 'ALL'}
        desired['acceptSslCerts'] = True
        desired['pageLoadStrategy'] = 'none'
        desired['browserstack.local'] = True
        desired['browserstack.user'] = "avinashmayur_d4Ul2M"
        desired['browserstack.key'] = "wGrAm4TUqDsyWARVx9ac"
        if self.proxy is not None:
            self.add_browser_args(options='proxy-server=%s' % self.proxy)
        if self.chrome_profile is not None:
            self.add_browser_args(options='user-data-dir=%s' % self.chrome_profile)
            # command_executor = 'https://hub-cloud.browserstack.com/wd/hub',
        try:
            driver = self._browser_stack_driver['type'](
                options=self.browser_opts,
                desired_capabilities=desired,
                keep_alive=False)
        except URLError as e:
            raise DeviceException('Cannot start Browser Stack Local driver. Error:  "URLError: %s"' % e.reason)
        if maximized:
            driver.maximize_window()
        return driver

    def set_safari_user_agent(self, user_agent):
        """in case if this is not working, enable full disk access for python3.6 and PyCharm
        https://apple.stackexchange.com/questions/343343/how-can-i-disable-inline-attachment-previews-i-e-view-as-icon-by-default-in-m/343356#343356
        """
        command = f"defaults write com.apple.Safari CustomUserAgent \"\'{user_agent}\'\""
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def return_default_safari_user_agent(self):
        command = "defaults delete com.apple.Safari CustomUserAgent"
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def set_cookies(self):
        try:
            for cookie in self.cookies:
                self._driver.add_cookie(cookie)
        except InvalidCookieDomainException as e:
            self.logger.warning(f'*** Failed to set cookie. Exception: {e}')
            raise VoltronException('Failed to set cookie')

    def set_local_storage_cookies(self, ls_cookies_dict=None):
        if ls_cookies_dict is not None:
            scripts_array = []
            for name, value in ls_cookies_dict.items():
                scripts_array.append(f'localStorage.setItem("{name}", "{value}");')
            if self._driver is not None:
                self._driver.execute_script('\n'.join(scripts_array))
            else:
                raise VoltronException('Trying to set local storage cookies before webdriver initialization')

    def set_session_storage_cookies(self, session_storage_cookies_dict=None):
        if session_storage_cookies_dict is not None:
            scripts_array = []
            for name, value in session_storage_cookies_dict.items():
                scripts_array.append(f'sessionStorage.setItem("{name}", "{value}");')
            if self._driver is not None:
                self._driver.execute_script('\n'.join(scripts_array))
            else:
                raise VoltronException('Trying to set session storage cookies before webdriver initialization')

    def open_url(self, url: str = ''):
        attempt = 1
        max_retries = 3
        timeout_backup = socket.getdefaulttimeout()
        socket.setdefaulttimeout(30)
        while attempt <= max_retries:
            try:
                self.navigate_to(url)
                socket.setdefaulttimeout(timeout_backup)
                break
            except socket.timeout as err:
                self._logger.warning(
                    '%s browser failed to start with error "%s", attempt %s of %s'
                    % (self.browser, err, attempt, max_retries)
                )
                if self._driver is not None:
                    self._driver.quit()
                    self._driver = None
                attempt += 1

    def navigate_to(self, url: str = '', testautomation=True, **kwargs):
        def url_corrector(url_str: str):
            parsed = urlparse(url_str)
            scheme = parsed.scheme
            netloc = parsed.netloc
            path = parsed.path
            query = parsed.query
            final_url = f'{scheme}://{netloc}'
            if path and path != "/":
                final_url = f'{final_url}{path}'
            if query:
                if not path:
                    final_url = f'{final_url}/?{query}'
                else:
                    final_url = f'{final_url}?{query}'
            return final_url

        if self.use_browser_stack:
            if self.enable_bs_performance_log:
                self.get_performance_log(preserve=True) if self.browser.lower() == 'chrome' else self._logger.warning(
                    'Performance logs are available only for Chrome')
        else:
            self.get_performance_log(preserve=True) if self.browser.lower() == 'chrome' else self._logger.warning(
                'Performance logs are available only for Chrome')
        if '/5-a-side/leaderboard/' in url:
            url = url.rstrip('=') + '%3D'
        if not re.match('^https?://.*', url):
            url = 'https://%s' % url
            if url.startswith('http:'):
                url = url.replace('http', 'https', 1)
        if testautomation:
            url = url + '?automationtest=true'
        url = url_corrector(url)
        self._logger.info(f'*** Navigating to "{url}"')
        self.driver.get(url)
        if kwargs.get('event_id'):
            event_id_exist = str(kwargs.get('event_id')) not in url
        else:
            event_id_exist = True
        current_url = self.get_current_url()
        if current_url is not None and current_url not in url and event_id_exist:
            self._logger.info(f'*** Current URL is "{self.get_current_url()}"')
            navigate_script = f"window.location.href = '{url}';return window.location.href"
            js_nav_url = self.driver.execute_script(navigate_script)
            if self.get_current_url() not in url:
                self._logger.info(f'*** Current URL after js navigate is "{self.get_current_url()} '
                                  f'{self.get_current_url() not in url}"')
            else:
                if 'buildInfo' not in url:
                    set_has_hostname_opened(True)
        else:
            if 'buildInfo' not in url:
                set_has_hostname_opened(True)

    def refresh_page(self):
        if self.use_browser_stack:
            if self.enable_bs_performance_log:
                self.get_performance_log(preserve=True) if self.browser.lower() == 'chrome' else self._logger.warning(
                    'Performance logs are available only for Chrome')
        else:
            self.get_performance_log(preserve=True) if self.browser.lower() == 'chrome' else self._logger.warning(
                'Performance logs are available only for Chrome')
        url = self.get_current_url()
        url = url + '?automationtest=true' if 'automationtest=true' not in url else url
        self._logger.info(f'*** Navigating to "{url}"')
        self.driver.get(url)
        if self.get_current_url != url:
            self._logger.info(f'*** Current URL is "{self.get_current_url}"')
            navigate_script = f"""
                   window.location.href = "{url}"
                   """
            self.driver.execute_script(navigate_script)
            if self.get_current_url() != url:
                if self.get_current_url() != url.replace('?automationtest=true', ''):
                    self._logger.info(f'*** Current URL after js navigate is "{self.get_current_url}"')
                    raise VoltronException(f"Cannot navigate to url {url}")

    def get_current_url(self) -> str:
        return self.driver.current_url

    def go_back(self):
        self.driver.back()

    def get_number_of_tabs(self) -> int:
        """
        :return: Number of tabs opened in the browser
        """
        tabs = self.driver.window_handles
        return len(tabs)

    def switch_to_new_tab(self):
        """
        DESCRIPTION: Switch to new opened browser tab
        :return: None
        """
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])

    def open_tab(self, tab_index):
        """
        :param tab_index: starting from 0, because tabs is a list
        """
        if tab_index != 0:
            wait_for_result(lambda: len(self.driver.window_handles) > 1,
                            name='Wait for new opened tab',
                            timeout=2.5)
        tabs = self.driver.window_handles
        if tab_index < len(tabs):
            self.driver.switch_to.window(tabs[tab_index])
        else:
            self._logger.error('Can\'t switch to: %s tab, current browser tabs count is: %s'
                               % (tab_index, len(tabs)))

    def open_new_tab(self):
        self.driver.execute_script('window.open()')
        self.open_tab(tab_index=1)

    def close_current_tab(self):
        self.driver.close()

    def active_tab_title(self):
        return self.driver.title

    @property
    def resolution(self):
        return '%sx%s' % (self.width, self.height)

    @resolution.setter
    def resolution(self, value):
        width, height = value.split('x')
        self._driver.set_window_size(width=width, height=height)
        self.width, self.height = width, height

    def set_viewport_size(self, width, height):
        window_size = set_viewport_size(width, height)
        self._logger.debug(f'Current resolution is: "{window_size}"')
        self._driver.set_window_size(*window_size)

    @property
    def orientation(self):
        if self.width < self.height:
            return 'vertical'
        return 'horizontal'

    @orientation.setter
    def orientation(self, value):
        if value not in ['vertical', 'horizontal']:
            raise VoltronException('Provided orientation value "%s" is unknown, please use one of vertical/horizontal')
        if value != self.orientation:
            self.rotate_90()

    def rotate_90(self):
        self.set_viewport_size(self.height, self.width)

    @staticmethod
    def prepare_host_rules_option(hosts: typing.List[str]) -> str:
        """ Prepare option to disable multiple hosts by mapping it to ~NOTFOUND
        :param hosts: list of hosts to disable
        :returns: prepared option
        """
        rules = [f"MAP {host} ~NOTFOUND" for host in hosts]
        return '--host-resolver-rules=' + ','.join(rules)

    def add_browser_args(self, options=None):
        if options is not None:
            if isinstance(options, str):
                options = [options]
            for option in options:
                self._logger.debug(f'** Added browser option: {option}')
                self.browser_opts.add_argument(option)

    def get_performance_log(self, preserve=True):
        """
        To get performance logs from browser
        :param preserve: (bool) True: if is needed to preserve the logs on navigation
        :return: list of dicts with timestamp, message and level fields for each performance entry
        """
        if self.use_browser_stack and not self.enable_bs_performance_log:
            raise VoltronException("Performance Logging is Not Enabled in Browser Stack please "
                                   "Set 'enable_bs_performance_log' on Test Level to True ")

        try:
            raw_entries = self.driver.get_log('performance')
            entries = [[{record_name: json.loads(record_value) if record_name == 'message' else record_value}
                        for record_name, record_value in entry.items()] for entry in raw_entries]
            if preserve:
                self._preserved_performance_log.extend(entries)
                return self._preserved_performance_log
            return entries
        except Exception as err:
            self._logger.warning(f'Error getting performance logs: {err}')
            return []

    def get_console_log(self):
        if self.browser.lower() == 'chrome':
            try:
                log = self.driver.get_log('browser')
                f = ''
                for entry in log:
                    timestamp = entry['timestamp']
                    message = entry['message']
                    date = datetime.datetime.fromtimestamp(int(timestamp) / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
                    f += '[' + date + ']' + ':    ' + message + ' *** Full Error log entry: ' + str(entry) + '\n'
                return f

            except Exception as err:
                self._logger.error('Error attaching console.log: %s' % err)
        else:
            self._logger.warning(f'No console logs available for browser "{self.browser}"')

    def quit(self):
        if self._driver:
            self._driver.quit()
        if self.browser.lower() == 'safari':
            self.return_default_safari_user_agent()
