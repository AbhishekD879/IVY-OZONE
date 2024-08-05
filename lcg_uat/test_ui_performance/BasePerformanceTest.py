import datetime
import json
import os
import re
from time import sleep
from time import time
from urllib.parse import urlencode

import requests
from influxdb import InfluxDBClient
from requests.auth import HTTPBasicAuth

import tests
import voltron.utils.performance_utils
from tests.Common import Common
from voltron.device.device_manager import DeviceManager
from voltron.pages.coral.mobile_site import MobileSite
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class BasePerformanceTest(Common):
    db_name = 'ui_performance'
    site = None
    proxy = None
    device = None
    env = None
    test_hostname = tests.HOSTNAME
    network = os.getenv('NETWORK_TYPE', 'reset')
    measurement_name = 'UI_performance'
    update_tstrail_case = False

    @classmethod
    def reset_network(cls):
        os.system('sudo simulate_connection.sh reset')

    @classmethod
    def custom_setUp(cls, **kwargs):
        os.system(f'sudo simulate_connection.sh {cls.network}')
        cls.load_invictus_application()

    @classmethod
    def custom_tearDown(cls):
        cls.reset_network()
        cls.device.quit()

    @classmethod
    def load_invictus_application(cls):
        if cls.site is None:
            sleep(5)

            cls.device = DeviceManager(device_name=tests.device_name, location=tests.location).get_device()
            cls.device.ls_cookies = {'OX.tutorial': 'true', 'OX.footballTutorial': 'true', 'OX.cookieBanner': 'true',
                                     'OX.cookieBannerVersion': 12347}
            cls.device.cookies = ({'name': 'cookieBanner', 'value': 'true'},)
            cls.device.start_browser(maximized=cls.maximized_browser, browser_stack=cls.use_browser_stack,
                                      browserstack_local=cls.use_browser_stack_local)
            cls.test_start_time = time()
            cls.site = MobileSite()
            cls.env = re.findall('(.*)\.coral\.co\.uk.*', cls.test_hostname)[0]
            cls.device.open_url(url=f'{cls.test_hostname}/buildInfo.json')

    def post_har(self, har):
        har_json = json.dumps(har)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Automated": "true"}
        body = urlencode({"file": har_json})
        resp = requests.post(
            url='http://coral-allure.symphony-solutions.eu/harstorage/results/upload',
            data=body,
            headers=headers,
            auth=HTTPBasicAuth('guest', 'qawsed')
        )
        self._logger.debug(f'Harstorage response. Status code: "{resp.status_code}", reason: "{resp.reason}"')

    def navigate_to_url(self, url):
        self.device.navigate_to(url)
        self.execute_js_function('measure_splash_screen_hidden')
        self.site.wait_splash_to_hide()
        wait_for_result(
            lambda: len(self.device.driver.execute_script('return performance.getEntriesByName("splash_hidden")')) > 0,
            name='Performance mark "splash_hidden" present',
            timeout=30,
        )

    def execute_js_function(self, js_function, path=None):
        path = path if path else voltron.utils.performance_utils.__file__
        driver = self.device.driver
        driver.set_script_timeout(10)
        try:
            js_file = open(os.path.join(os.path.split(path)[0], f'{js_function}.js')).read()
            return driver.execute_script(js_file)
        except Exception as error:
            raise VoltronException(f'Error calling "{js_function}" function. "{error}"')

    def post_to_influxdb(self):
        driver = self.device.driver
        data = driver.execute_script('return performance.getEntries();')
        bundle_size = 0
        script_data = 0
        css_data = 0
        link_data = 0
        xmlhttprequest_data = 0
        selenium_accessible = None
        splash_screen_hidden = None
        unload_event_end = None
        dom_complete = None
        time_value = datetime.datetime.utcfromtimestamp(self.test_start_time).isoformat('T') + 'Z'
        metrics = {}
        for item in data:
            if re.findall('^https:\/\/(invictus|sports|sports-hl)\.coral\.co\.uk\/'
                          '(styles|bundle.bma|bundle.vendor)\.(\w+)\.(js|css)', item.get('name')):
                bundle_size += item.get('decodedBodySize')
            if item.get('initiatorType') == 'script':
                script_data = script_data + item.get('decodedBodySize')
            elif item.get('initiatorType') == 'css':
                css_data = css_data + item.get('decodedBodySize')
            elif item.get('initiatorType') == 'link':
                link_data = link_data + item.get('decodedBodySize')
            elif item.get('initiatorType') == 'xmlhttprequest':
                xmlhttprequest_data = xmlhttprequest_data + item.get('decodedBodySize')
            elif item.get('name') == 'selenium_accessible':
                selenium_accessible = item.get('startTime')
            elif item.get('name') == 'splash_hidden':
                splash_screen_hidden = item.get('startTime')
            elif item.get('initiatorType') == 'navigation':
                dom_complete = item.get('domComplete')
                unload_event_end = item.get('unloadEventEnd')
            if item.get('entryType') == 'resource':
                metrics.update({"number_requests": metrics.get("number_requests", 0) + 1})

            name = item.get('name')
            if re.match('.*_navigation$', name):
                metrics.update({name: item.get('duration')})
        measurement = {
            'measurement': self.measurement_name,
            'time': time_value,
            'tags': {
                'net_type': self.network,
                'test_name': self.__class__.__name__,
                'host_name': self.test_hostname,
            },
            'fields': {
                'bundle_size': bundle_size,
                'script_data': script_data,
                'css_data': css_data,
                'link_data': link_data,
                'xmlhttprequest_data': xmlhttprequest_data,
                'selenium_accessible': selenium_accessible,
                'splash_screen_hidden': splash_screen_hidden,
                'domComplete': dom_complete,
                'unloadEventEnd': float(unload_event_end),
            },
        }
        measurement['fields'].update(metrics)
        self._logger.debug(f'Influxdb data measurement: "{json.dumps([measurement], indent=2)}"')
        client = InfluxDBClient(
            host='oxygen-monitor.crlat.net',
            port=8086,
            database='_internal')
        client.create_database(self.db_name)
        client.write_points([measurement], database=self.db_name)
