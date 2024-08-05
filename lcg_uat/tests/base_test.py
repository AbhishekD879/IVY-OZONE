import inspect
import json
import logging
import os
import re
import sys
import time
import traceback
import unittest
from inspect import getframeinfo
from inspect import stack
from json import JSONDecodeError

import requests

from voltron.utils.bs_logger import BrowserStackHandler
import pytest
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import translation_lang
from crlat_testrail_integration.utils.exceptions import TestRailAPIError
import tests
from voltron.device.device_manager import DeviceManager
from voltron.pages.shared import get_cms_config, set_has_hostname_opened, get_has_hostname_opened
from voltron.pages.shared import get_device_properties
from voltron.pages.shared import get_platform
from voltron.pages.shared import set_cms_settings
from voltron.resources.test_rail_suite_ids import test_rail_suites
from voltron.resources.test_rail_suite_ids import test_rail_suites_based_on_folder_name
from voltron.utils.exceptions.failure_exception import TestFailure
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.exceptions.soft_assert_exception import SoftAssertException
from voltron.utils.helpers import do_request
from voltron.utils.helpers import string_generator
from voltron.utils.js_functions import get_perf_logs
from voltron.utils.waiters import wait_for_result
from browserstack.local import Local
from voltron.resources.supported_browser_stack_devices import SUPPORTED_BROWSER_STACK_DEVICES


@pytest.mark.incremental
class BaseTest(unittest.TestCase):
    _logger = logging.getLogger('voltron_logger')
    _site = None
    _device = None
    _device_type = None
    _platform = None
    device_name = None
    maximized_browser = False

    use_chrome_profile = False
    _chrome_profile_path = None
    proxy, proxy_port = None, None
    record_har = False

    _cookies = ({'name': 'cookieBanner', 'value': 'true'},
                {'name': 'onboarding', 'value': 'true'},
                {'name': 'euconsent', 'value': 'a'},
                {'name': 'OptanonAlertBoxClosed', 'value': 'true'})
    _ls_cookies = {'OX.tutorial': 'true', 'OX.footballTutorial': 'true', 'OX.cookieBanner': 'true',
                   'OX.oddsBoostSeen': 'true', 'OX.cookieBannerVersion': 12347}
    _qubit_cookie_coral = {
        '__qubitCookieState': {
            'state': {
                'biscottiPermanent': 'q040vpnfgcw-0k2os4vsr-c2tj6so:2:2:1:1:0::0:1:0:BdxCPB:BdxCPL::::::::::::::::migrated|1573135309046:ELzV=Ck=B=B7Ug=Bw::W5GK9j2:W5GK6gA:0:0:0::0:0:.coral.co.uk:0',
                'biscottiGeneric': 'Coral-pageViewOnLogin-pre=1=%&rgWeek=cl_testgvccl-BO157-cor=%:W5GK+Kf:.coral.co.uk'
            }
        }
    }
    _qubit_cookie_ladbrokes = {
        '__qubitCookieState': {
            'state': {
                'biscottiPermanent': 'mbf7cyytr8w-0k2otcrb4-1kyqz6w:2:2:1:1:0::0:1:0:BdxCu9:BdxCw3:::::77.52.194.150:lviv:25313:ukraine:UA:49.8347:24.0173:unknown:unknown:lvivska%20oblast:12248:migrated|1573137463802:ELP6=Ik=B=B7Su=ML::W5GTLn6:W5GStio:0:0:0::0:0:msports.ladbrokes.com:0',
                'biscottiGeneric': 'Android-Roxanne-pageViewOnLogin=1=%&Android-Roxanne-initialSession=1=XWEPhhW&rgWeek=43610083-lad=%:W5GV+r4:msports.ladbrokes.com'
            }
        }
    }

    _session_storage_cookies = {'coralsports.host-closedCounter': '1'}

    executed_tests = {}
    failed_tests = []
    _failed_asserts = []
    _skipped_steps = []
    _test_steps = []
    skip_next = False

    keep_browser_open = False
    delete_events = True
    update_tstrail_case = True
    brand = tests.settings.brand
    proxy_admin_hostname = tests.settings.proxy_admin
    __ob_config = None
    _ss_config = None
    __change_ob_item = None
    __gvc_wallet_user_client = None
    blocked_hosts = []
    use_browser_stack = tests.use_browser_stack
    bs_local = Local()
    bs_local_args = {"key": None}
    use_browser_stack_local = False
    _bs_session_id = None
    _bs_session_details = None
    _stack_trace = {}
    enable_bs_performance_log = False  # Switch to ON/OFF Perf Logs in Browserstack
    bs_log_config = {
        "networkLogs": True,
        "debug": False,
        "video": True,
        'seleniumLogs': True,
        'appiumLogs': False,
        'console': 'disable'
    }

    def assertEquals(self, first, second, msg=None):
        self.assertEqual(first=first, second=second, msg=msg)

    def assertNotEquals(self, first, second, msg=None):
        self.assertNotEqual(first=first, second=second, msg=msg)

    def assertAlmostEquals(self, first, second, msg=None):
        self.assertAlmostEqual(first=first, second=second, msg=msg)

    def assertNotAlmostEquals(self, first, second, msg=None):
        self.assertNotAlmostEqual(first=first, second=second, msg=msg)

    def assertRegexpMatches(self, text, expected_regex, msg=None):
        self.assertRegex(text=text, expected_regex=expected_regex, msg=msg)
        # self.assertCountEqual()
        # self.assertDictEqual(expected_regex, self.assertRegex(expected))
        # self.assertDictEqual(self.assertRegex())
        # self.ass

    @staticmethod
    def browserstack_session_details(driver):
        # get details of the session
        response = driver.execute_script('browserstack_executor: {"action": "getSessionDetails"}')
        json_response = json.loads(response)

        # print the session ID in the IDE's console
        return json_response

    @property
    def is_safari(self):
        if get_platform() == 'ios':
            return True
        else:
            return (get_device_properties()['browser'].lower() in ['safari', 'chromium'] and
                    'iphone' in get_device_properties()['device'].lower())

    @property
    def ss_query_builder(self):
        return query_builder().add_filter(translation_lang())

    @classmethod
    def get_cms_config(cls):
        if not get_cms_config():
            set_cms_settings(env=tests.settings.cms_env, brand=cls.brand)
        return get_cms_config()

    @property
    def cms_config(self):
        self.get_cms_config()
        return get_cms_config()

    @classmethod
    def get_ob_config(cls):
        if not cls.__ob_config:
            from crlat_ob_client.openbet_config import OBConfig
            cls.__ob_config = OBConfig(env=tests.settings.backend_env, ss_version='2.31', brand=cls.brand)
        return cls.__ob_config

    @property
    def ob_config(self):
        self.get_ob_config()
        return self.__ob_config

    @classmethod
    def get_ss_config(cls):
        if not cls._ss_config:
            cls._ss_config = SiteServeRequests(env=tests.settings.backend_env, brand=cls.brand)
        return cls._ss_config

    @property
    def ss_req(self):
        self.get_ss_config()
        return self._ss_config

    @classmethod
    def get_gvc_wallet_user_client(cls):
        if not cls.__gvc_wallet_user_client:
            from crlat_gvc_wallet_client.client import GVCUserClient
            if 'qa' in tests.HOSTNAME:
                env_host = tests.HOSTNAME[0:3]
                cls.__gvc_wallet_user_client = GVCUserClient(env=tests.settings.gvc_wallet_env,
                                                             brand=cls.brand, env_host=env_host)
            else:
                cls.__gvc_wallet_user_client = GVCUserClient(env=tests.settings.gvc_wallet_env,
                                                             brand=cls.brand)
        return cls.__gvc_wallet_user_client

    @property
    def gvc_wallet_user_client(self):
        self.get_gvc_wallet_user_client()
        return self.__gvc_wallet_user_client

    failureException = TestFailure
    longMessage = False

    @classmethod
    def cms_setUp(cls):
        """
        Pre-setup for CMS before browser starts
        """
        cms = cls.get_cms_config()

        # enable right menu button
        from crlat_core.request import InvalidResponseException
        try:
            system_config = cls.get_initial_data_system_configuration()
        except InvalidResponseException as e:
            cls._logger.warning(f'*** Exception: "{e}" was received')
            return
        except JSONDecodeError:
            system_config = cls.get_initial_data_system_configuration()
        layouts = system_config.get('Layouts')
        if not layouts:
            layouts = cls.get_cms_config().get_system_configuration_item('Layouts')
        if layouts:
            show_right_menu_button = layouts.get('ShowRightMenu', 'true')
            if show_right_menu_button != 'true':
                cms.update_system_configuration_structure(config_item='Layouts',
                                                          field_name='ShowRightMenu',
                                                          field_value='true')
                wait_for_result(lambda: cls.get_initial_data_system_configuration(cached=False).get('Layouts').get(
                    'ShowRightMenu') == 'true',
                                timeout=30,
                                name='[CMS][System Config] ShowRightMenu status to be True')

    @classmethod
    def get_initial_data_system_configuration(cls, cached=True):
        """
        Method to get System Configuration from initial-data
        By default returns cached data
        :param cached:
        :return:
        """
        return cls.get_cms_config().get_initial_data(cached=cached).get('systemConfiguration', {})

    @classmethod
    def openHomePage(cls):
        if cls._site is None:
            cls.start_har_recorder()
            cls.setUpSite()
            cls._device.open_url(url=tests.HOSTNAME)
            set_has_hostname_opened(True)
            cls._site.wait_splash_to_hide()
        elif cls.site and not get_has_hostname_opened():
            cls._device.open_url(url=tests.HOSTNAME)
            set_has_hostname_opened(True)
            cls._site.wait_splash_to_hide()

    @classmethod
    def custom_site_setup(cls):
        pass

    @property
    def is_browser_opened(self):
        return self._site is not None

    @property
    def site(self):
        self.openHomePage()
        self._site.close_all_banners()
        # TODO: Method causing problem in UI
        # if self.enable_bs_performance_log:
        #     get_perf_logs()
        return self._site

    @classmethod
    def get_profile_path(cls):
        if cls.use_chrome_profile:
            if cls._chrome_profile_path is None:
                cls._chrome_profile_path = '/tmp/%s' % time.time()
            return cls._chrome_profile_path

    @classmethod
    def set_device_name(cls):
        """
        User to set actual device name needed for run
        Method is added to handle CI runs
        :return:
        """
        if cls.use_browser_stack:
            if not cls.device_name:
                cmd_line_device_arg = next((arg.split('=')[1] for arg in sys.argv if 'browser_stack_device' in arg),
                                           tests.bs_device_name)
                cls.device_name = cmd_line_device_arg
        else:
            cmd_line_device_arg = next((arg.split('=')[1] for arg in sys.argv if 'device_name' in arg),
                                       tests.device_name)
            if cls.device_name is not None and 'desktop' not in cmd_line_device_arg.lower():
                return
            if cls.device_name is not None and tests.mobile_safari_default.lower() in cmd_line_device_arg.lower():
                cls.device_name = cmd_line_device_arg
            elif 'desktop' in cmd_line_device_arg.lower():
                cls.device_name = cmd_line_device_arg
            else:
                cls.device_name = tests.device_name

    @classmethod
    def start_har_recorder(cls):
        if cls.record_har:
            url = f'{cls.proxy_admin_hostname}/plugins/start/SocksHttpSpy?ttl=300'
            r = do_request(method='GET', url=url)
            cls.proxy = r['client_data']['url'].replace('socks', 'socks5')
            cls.proxy_port = r['client_data']['port']

    def get_har(self):
        if self.record_har:
            url = f'{tests.settings.proxy_admin_har_recorder}{self.proxy_port}/get_har'
            r = do_request(method='GET', url=url)
            return r

    def delete_har(self):
        if self.record_har:
            url = f'{tests.settings.proxy_admin_har_recorder}{self.proxy_port}/delete_har'
            r = do_request(method='GET', url=url)
            return r

    @classmethod
    def stop_har_recorder(cls):
        if cls.record_har:
            url = f'{cls.proxy_admin_hostname}/plugins/stop/SocksHttpSpy/{cls.proxy_port}'
            do_request(method='GET', url=url)

    @classmethod
    def setUpSite(cls):
        brand = cls.brand
        if cls._device is None:
            chrome_profile = cls.get_profile_path() if DeviceManager.supported_devices.get(cls.device_name, {}).get(
                'browser', '') == 'chrome' \
                else None
            cls._device = DeviceManager(device_name=cls.device_name, location=tests.location,
                                        proxy=cls.proxy, chrome_profile=chrome_profile,
                                        use_browser_stack=cls.use_browser_stack,
                                        enable_bs_performance_log=cls.enable_bs_performance_log,
                                        bs_log_config=cls.bs_log_config).get_device()
            cls._device.blocked_hosts = cls.blocked_hosts
            cls._ls_cookies = cls._ls_cookies if cls._ls_cookies else {}
            if brand == 'ladbrokes':
                cls._ls_cookies.update(cls._qubit_cookie_ladbrokes)
            else:
                cls._ls_cookies.update(cls._qubit_cookie_coral)
            cls._device.ls_cookies = cls._ls_cookies
            cls._device.cookies = cls._cookies
            cls._device.session_storage_cookies = cls._session_storage_cookies
            if cls.use_browser_stack_local:
                if not cls.bs_local_args.get("key"):
                    raise Exception("BS Local key not set")
                cls.bs_local.start(**cls.bs_local_args)
            cls._device.start_browser(maximized=cls.maximized_browser, browser_stack=cls.use_browser_stack,
                                      browserstack_local=cls.use_browser_stack_local)
            if cls.use_browser_stack:
                executor_object = {
                    'action': 'setSessionName',
                    'arguments': {
                        'name': f"{cls.__name__}"
                    }
                }
                browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
                cls._device.driver.execute_script(browserstack_executor)
                bs_handler = BrowserStackHandler(driver=cls._device.driver)
                cls._logger.addHandler(bs_handler)

        if brand == 'bma':
            from voltron.pages.coral.desktop_site import DesktopSite
            from voltron.pages.coral.mobile_site import MobileSite
            from voltron.pages.coral.tablet_site import TabletSite
            sites = {
                'mobile': MobileSite,
                'tablet': TabletSite,
                'desktop': DesktopSite
            }
        elif brand == 'ladbrokes':
            from voltron.pages.ladbrokes.ladbrokes_desktop_site import LadbrokesDesktopSite
            from voltron.pages.ladbrokes.ladbrokes_mobile_site import LadbrokesMobileSite
            from voltron.pages.ladbrokes.ladbrokes_tablet_site import LadbrokesTabletSite
            sites = {
                'mobile': LadbrokesMobileSite,
                'tablet': LadbrokesTabletSite,
                'desktop': LadbrokesDesktopSite
            }
        try:
            cls._device_type = cls._device.device_args['type']
            site = sites[cls._device_type]
        except KeyError:
            raise GeneralException(f'No device type specified for "{cls.device_name}" device "{brand}" brand')
        cls._logger.info(f'*** Recognized {site.__name__} for "{brand}" brand and "{cls._device_type}" device')
        cls._site = site(brand=brand)
        cls._platform = get_platform()
        cls.custom_site_setup()

    @property
    def device(self):
        if not self._device:
            self.setUpSite()
        return self._device

    @property
    def device_type(self):
        if not self._device_type:
            self.set_device_name()
            name = self.device_name
            if self.use_browser_stack:
                if name in SUPPORTED_BROWSER_STACK_DEVICES:
                    self.__class__._device_type = SUPPORTED_BROWSER_STACK_DEVICES[name]['type']
                    return self._device_type
                else:
                    raise Exception(f'Device name "{self.device_name}" '
                                    f'is not found in list of supported Browsers stack devices')
            if name not in DeviceManager.supported_devices.keys():
                raise Exception(f'Device name "{self.device_name}" was not found in list of supported devices')
            self.__class__._device_type = DeviceManager.supported_devices[name]['type']
        return self._device_type

    @classmethod
    def setUpClass(cls):
        cls.current_test_name = cls.__name__
        steps = sorted((step_name for step_name, step in cls.__dict__.items() if step_name.startswith('test_')))
        cls._test_steps = steps

        if cls.record_har and not cls.proxy:
            cls.start_har_recorder()
        cls.custom_setUp()
        cls.cms_setUp()

    @classmethod
    def custom_setUp(cls, **kwargs):
        pass

    @property
    def test_name(self):
        return self._testMethodDoc.strip() \
            if self._testMethodDoc is not None and self._testMethodDoc.strip() != '' \
            else self._testMethodName

    def setUp(self):
        if set(self.failed_tests) - set(self._skipped_steps):
            self._logger.info('')
            self._logger.info('*********************************************************************')
            self._logger.info(f'*** SKIPPING test step: "{self.test_name}"')
            self._logger.info('*********************************************************************')
            self.skipTest(f'Skipping test due to previously failed and skipped tests {self.failed_tests}')
            if self.use_browser_stack:
                executor_object = {
                    'action': 'setSessionStatus',
                    'arguments': {
                        'status': "failed",
                        'reason': f"{self.failed_tests}"
                    }
                }
                browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
                self.device.driver.execute_script(browserstack_executor)
        else:
            self._logger.info('*********************************************************************')
            self._logger.info(f'*** EXECUTING test step: "{self.test_name}"')
            go_job_name = os.environ.get('GO_JOB_NAME', None)
            if go_job_name:
                self._logger.info(f'*** CI JOB: "{go_job_name}"')
            self._logger.info('*********************************************************************')

    def softAssert(self, assert_method, *arguments, **keywords):
        """
        Asserts the specified comparison
        and stores any raised failureException stack traces
        for later reporting.

        @param assert_method: the method definition for the desired assert call, ex: self.assert
        usage from test:
        >>> self.softAssert(self.assertTrue, self.inplay.is_enabled(), msg='Inplay is not enabled')
        >>> self.softAssert(self.assertIn, 1, [1,2,3,4,5], msg='Number is not present in list')
        """
        try:
            assert_method(*arguments, **keywords)

        except self.failureException:
            exception_trace = traceback.format_exc()

            caller = getframeinfo(stack()[1][0])
            caller_traceback = f'{caller.filename}:{caller.lineno}\n{self._testMethodName}\n{caller.code_context[0].strip()}'
            full_trace = f'{caller_traceback}\n\n{exception_trace}'
            self.__class__._failed_asserts.append(full_trace)
            self.__class__._skipped_steps.append(self._testMethodName)
            self._logger.warning(msg=f'*** Skipped step "{self.test_name}" due to exception: \n{full_trace}')
            self.skipTest(reason=full_trace)

    def tearDown(self):
        if (self._testMethodName == self._test_steps[-1]) and self._failed_asserts:
            report = [f'\n\nNumber of Failed asserts: {len(self._failed_asserts)}\n']

            for i, failure in enumerate(self._failed_asserts, start=1):
                report.append(f'{i}: {failure}')
                if self.use_browser_stack:
                    executor_object = {
                        'action': 'setSessionStatus',
                        'arguments': {
                            'status': "failed",
                            'reason': f"{failure}"
                        }
                    }
                    browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
                    self.device.driver.execute_script(browserstack_executor)

            raise SoftAssertException(message='\n'.join(report))

    @classmethod
    def tearDownClass(cls):
        cls.custom_tearDown()
        if cls.__ob_config and tests.settings.backend_env != 'prod':
            ob_config = cls.get_ob_config()
            events = ob_config.CREATED_EVENTS
            if cls.delete_events and (len(events) > 0):
                for event_id in events:
                    ob_config.change_event_state(event_id=event_id)
        cls.cms_tearDown()
        device = cls._device
        if device:
            if cls.use_browser_stack and device._driver:
                session_details = cls.browserstack_session_details(device._driver)
                cls._bs_session_details = session_details
                cls._bs_session_id = session_details.get("hashed_id")
                if tests.location == "AWS_GRID":
                    cls.upload_terminal_logs(session_id=session_details.get("hashed_id"), log_data=cls._stack_trace,
                                             file_format="json")
                device.quit()
                return
            if not cls.keep_browser_open:
                device.quit()
                return
            elif not tests.settings.allow_keep_open:
                device.quit()
        if cls.record_har:
            cls.stop_har_recorder()
        if cls.bs_local:
            if cls.bs_local.isRunning():
                cls.bs_local.stop()

    @classmethod
    def cms_tearDown(cls):
        if not get_cms_config():
            return
        cms_config = cls.get_cms_config()

        featured_tab_modules = cms_config._created_featured_tab_modules
        for module_id in featured_tab_modules:
            cms_config.delete_featured_tab_module(module_id)

        promotions = cms_config._created_promotions
        for promotion_id in promotions:
            cms_config.delete_promotion(promotion_id)

        offer_modules = cms_config._created_offer_module
        for offer_module_id in offer_modules:
            cms_config.delete_offer_modules(offer_module_id)

        offers = cms_config._created_offers
        for offer_id in offers:
            cms_config.delete_offer(offer_id)

        banners = cms_config._created_banners
        for banner_id in banners:
            cms_config.delete_banner(banner_id)

        module_ribbon_tabs = cms_config.module_ribbon_tabs._created_tabs
        for module_ribbon_tab_id in module_ribbon_tabs:
            cms_config.module_ribbon_tabs.delete_tab_by_id(module_ribbon_tab_id)

        highlights_carousels = cms_config._created_highlights_carousels
        for highlights_carousel_id in highlights_carousels:
            cms_config.delete_highlights_carousel(highlights_carousel_id)

        surface_bets = cms_config._created_surface_bets
        for surface_bet_id in surface_bets:
            cms_config.delete_surface_bet(surface_bet_id)

        quick_links = cms_config._created_quick_links
        for quick_link_id in quick_links:
            cms_config.delete_quick_link(quick_link_id)

        coupon_segments = cms_config._created_coupon_segment
        for coupon_segment_id in coupon_segments:
            cms_config.delete_coupon_segment(coupon_segment_id)

        super_buttons = cms_config._created_super_buttons
        for super_button_id in super_buttons:
            cms_config.delete_mobile_super_button(super_button_id)

        special_super_buttons = cms_config._created_special_super_buttons
        for super_button_id in special_super_buttons:
            cms_config.delete_mobile_special_super_button(super_button_id)

        event_hubs = cms_config._created_event_hubs
        for event_hub_id in event_hubs:
            cms_config.delete_event_hub_module(event_hub_id)

        racing_edp_markets = cms_config._created_racing_edp_markets
        for market in racing_edp_markets:
            cms_config.delete_markets_with_description(name=market)

        timeline_posts = cms_config._created_timeline_post
        for post in timeline_posts:
            cms_config.delete_timeline_post(post_id=post)

        timeline_templates = cms_config._created_timeline_template
        for template in timeline_templates:
            cms_config.delete_timeline_template(template_id=template)

        contests = cms_config._created_five_a_side_show_down
        for contest in contests:
            cms_config.delete_five_a_side_show_down(contestId=contest)

        sport_categories = cms_config._created_sport_category
        for sport_category in sport_categories:
            cms_config.delete_sport_category(sport_category_id=sport_category)

        big_competitions = cms_config._created_big_competitions
        for big_competition in big_competitions:
            cms_config.delete_big_competition(big_competition_id=big_competition)

        footer_menus = cms_config._created_footer_menu
        for footer_menu in footer_menus:
            cms_config.delete_footer_menu(id=footer_menu)

        inplay_sports = cms_config._created_inplay_module
        for inplay_sport in inplay_sports:
            cms_config.delete_inplay_sport_module(sport_name=inplay_sport)

        rgy_modules = cms_config._created_rgy_modules
        for rgy_module in rgy_modules:
            cms_config.delete_rgy_module(rgy_module_id=rgy_module)

        rgy_bonus_suppression_modules = cms_config._created_rgy_bonus_suppression_modules
        for rgy_bonus_suppression_module in rgy_bonus_suppression_modules:
            cms_config.delete_rgy_bonus_suppression_module(rgy_bonus_suppression_module_id=rgy_bonus_suppression_module)

        desktop_quick_links = cms_config._created_desktop_quick_links
        for desktop_quick_link in desktop_quick_links:
            cms_config.delete_desktop_quick_lnk(desktop_quick_link_id=desktop_quick_link)

        qe_quizs = cms_config._created_question_engine_quiz
        for quiz_id in qe_quizs:
            cms_config.delete_quiz(quiz_id=quiz_id)

        seo_pages = cms_config._created_seo_page
        for seo_page in seo_pages:
            cms_config.delete_seo_page(seo_page_id=seo_page)

    @classmethod
    def custom_tearDown(cls, **kwargs):
        pass

    def _get_executed_tests(self):
        return self.executed_tests.keys()

    def run(self, result=None):
        current_result = result

        super(BaseTest, self).run(result=result)
        passed = True
        if hasattr(current_result, '_excinfo') and current_result._excinfo:
            self.__class__.failed_tests.append(self._testMethodName)
            passed = False

            if self.use_browser_stack:
                def get_exception_info(test_case_function_obj):
                    try:
                        exc_info_list = getattr(test_case_function_obj, "_excinfo", [])
                        if exc_info_list:
                            for exc_info in exc_info_list:
                                exception = exc_info.value
                                exception_type = type(exception).__name__
                                stack_trace = "".join(
                                    traceback.format_exception(type(exception), exception, exc_info.tb))
                                # Do whatever you need with the exception type and stack trace
                                return exception_type, stack_trace
                        else:
                            return None, "No exception information available."
                    except Exception as e:
                        return "Error", f"Error occurred while retrieving exception info: {e}"

                exception_type, stack_trace = get_exception_info(current_result)
                executor_object = {
                    'action': 'setSessionStatus',
                    'arguments': {
                        'status': "failed",
                        'reason': f"""
                {self._testMethodName}
                Exception Type :{exception_type}
                Stack Trace : {traceback.format_exception(type(current_result._excinfo[-1].value), current_result._excinfo[-1].value, current_result._excinfo[-1].tb)[-1]}"""
                    }
                }
                browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
                self.device.driver.execute_script(browserstack_executor)
                self._stack_trace[self._testMethodName] = {
                    "ExceptionType": exception_type,
                    "Stack Trace": stack_trace
                }
        else:
            if self.use_browser_stack:
                executor_object = {
                    'action': 'setSessionStatus',
                    'arguments': {
                        'status': "passed",
                        'reason': f"{self._testMethodName}"
                    }
                }
                browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
                self.device.driver.execute_script(browserstack_executor)
        self.__class__.executed_tests.update(
            {
                self._testMethodName: {'passed': passed}
            }
        )
        if self._testMethodDoc is not None and self._testMethodDoc.strip() != '':
            self.__class__.executed_tests.update(
                {
                    self._testMethodName: {
                        'testMethodDoc': self._testMethodDoc.strip(),
                        'passed': passed
                    }
                }
            )

    @staticmethod
    def generate_user():
        return f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[:15]

    @staticmethod
    def upload_terminal_logs(session_id=None, log_data=None, file_format="txt"):
        """
        Upload terminal logs to BrowserStack.

        Parameters:
        - session_id (str): ID of the session available on the Automate dashboard.
        - log_data (str): Log data to be uploaded.
        - file_format (str): File format for the log data (default is "txt").

        Returns:
        - bool: True if the upload is successful, False otherwise.
        """

        # Replace with your BrowserStack credentials
        browserstack_username = tests.bs_username
        browserstack_access_key = tests.bs_access_key

        # URL for uploading terminal logs
        url = f'https://api-cloud.browserstack.com/automate/sessions/{session_id}/terminallogs'
        # HTTP Basic Authentication
        auth = (browserstack_username, browserstack_access_key)

        log = os.path.join(f"{session_id}.txt")
        with open(log, 'w') as f:
            for test_method, info in log_data.items():
                f.write(f"{test_method}\n")
                f.write(f"ExceptionType: {info['ExceptionType']}\n")
                f.write(f"\"Stack Trace\":\n")
                f.write(f"{info['Stack Trace']}\n\n")

        files = {'file': open(log, 'rb')}

        try:
            response = requests.post(url=url, files=files, auth=auth)
            if response.status_code == 200:
                # Upload successful, close and delete the file
                os.remove(log)
                return True
            else:
                print("Upload failed")
                os.remove(log)
                return False
        except Exception as e:
            print(f"Error uploading file: {e}")
            os.remove(log)
            return False


def vtest(Cls):
    absolute_path = inspect.getsourcefile(Cls)
    absolute_path = absolute_path.replace('\\', '/')  # for Windows machines
    Cls.set_device_name()
    device_name = Cls.device_name
    doc = Cls.__doc__.strip().replace('NAME:', 'NAME: [%s]' % device_name.upper())
    if Cls.update_tstrail_case and tests.location in ['IDE']:
        from crlat_testrail_integration.testrail import TestRailAPIClient

        tr = TestRailAPIClient()
        tr_suites = test_rail_suites()

        test_name = tr.get_testcase_name(string=doc)
        Cls._logger.info(f'*** Current test name: "{test_name}"')

        try:
            test_case_id = tr.get_testcase_id(string=doc)
            tr_test_case = tr.get_case(case_id=test_case_id)
            tr_test_case_qa_suite_id = tr_test_case.get('suite_id')
            tr.suite_id = tr_suites.get(tr_test_case_qa_suite_id, tr.suite_id)
        except TestRailAPIError:
            # For cases where TR_ID is not specified folder name detection way will be used
            # E.g. test case Test_AT_004_verify_right_column_favorites_widget and similar
            folder_name = absolute_path.split('voltron/')[-1].split('/')[0]
            tr.suite_id = test_rail_suites_based_on_folder_name().get(folder_name)
        vol_id = tr.get_voltron_testcase_id(string=doc)
        if vol_id:
            current_test = tr.get_case(case_id=vol_id.replace('C', ''))
            suite_id = current_test.get('suite_id')
            if suite_id != tr.suite_id:
                raise GeneralException(
                    f'Please provide correct VOL_ID. "{vol_id}" is from suite "{suite_id}" not "{tr.suite_id}"')
            if test_name != current_test['title']:
                tr.update_case(case_id=vol_id, data={'title': test_name})
        else:
            path = re.search('(tests.+)', absolute_path).group(1)

            # current_section = tr.get_current_section_for_case(path=path)
            # current_test = tr.get_current_case_from_section(current_section=current_section, test_name=test_name)
            current_section = ''
            current_test = tr.get_current_case_from_section(current_section=current_section, test_name=test_name,
                                                            path=path)
        Cls._logger.info(f'*** Voltron TestRail id for test "{test_name}" is: C{current_test["id"]}')

        steps = sorted((step for step_name, step in Cls.__dict__.items() if step_name.startswith('test_')),
                       key=lambda x: x.__name__)

        # read from absolute path
        F = open(absolute_path, encoding='utf8')
        priority_id = None
        for line in F:
            strip_line = line.strip()
            if strip_line.startswith('@pytest.mark.minimal'):
                priority_id = 5
            elif strip_line.startswith('@pytest.mark.low'):
                priority_id = 1
            elif strip_line.startswith('@pytest.mark.medium'):
                priority_id = 2
            elif strip_line.startswith('@pytest.mark.high'):
                priority_id = 3
            elif strip_line.startswith('@pytest.mark.critical'):
                priority_id = 4
            if strip_line.startswith('class') or priority_id:
                break
        if priority_id and current_test['priority_id'] != priority_id:
            tr.update_case(current_test['id'], data={'priority_id': priority_id})

        tr.update_steps(steps=steps, current_test=current_test)

    return Cls
