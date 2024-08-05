import json
import logging
import os
import traceback
import unittest
from inspect import getframeinfo
from inspect import stack

import pytest
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import translation_lang

import tests_ios_fully_native_regression as tests
from native_ios.device.device_manager import DeviceManager
from native_ios.environments.Native_Constants import Platform
from native_ios.pages.coral.coral_native_app import CoralNativeApp
from native_ios.pages.ladbrokes.ladbrokes_native_app import LadbrokesNativeApp
from native_ios.pages.shared import get_cms_config
from native_ios.pages.shared import set_cms_settings
from native_ios.utils.exceptions.failure_exception import TestFailure
from native_ios.utils.exceptions.general_exception import GeneralException
from native_ios.utils.helpers import string_generator, run_terminal_command


@pytest.mark.incremental
class BaseTest(unittest.TestCase):
    _logger = logging.getLogger('native_ios_logger')
    brand = tests.settings.brand
    _native_app = None
    logger = None
    _user = ''
    update_tstrail_case = False
    failed_tests = []
    _skipped_steps = []
    _failed_asserts = []
    executed_tests = {}
    __ob_config = None
    _ss_config = None
    delete_events = True
    device_name = tests.device_name  # Needed only for conftest/testrail integration to have same structure as voltron

    failureException = TestFailure
    longMessage = False

    def clisetup(self):
        # Set Up Env Variables
        set_up_env_variable = run_terminal_command("source ~/.bash_profile")
        if not set_up_env_variable.get('success'):
            raise GeneralException("Error While Setting Up Env Variables")
        appium_server_start = run_terminal_command(command="appium")
        if not appium_server_start.get('success'):
            raise GeneralException("Error While Starting Appium Server")

        # Android Specific
        check_avd_devices = run_terminal_command("emulator -list-avds")
        if check_avd_devices.get('success'):
            pass
            check_avd_devices.get('output')
        else:
            raise GeneralException("Error While Getting All Android Devices")

    @classmethod
    def setUpClass(cls):
        steps = sorted((step_name for step_name, step in cls.__dict__.items() if step_name.startswith('test_')))
        cls._test_steps = steps
        # cls.clisetup()
        test_name = cls.__name__
        cls._device = DeviceManager(test_name=test_name).get_device()
        # todo: VOL-6205
        cls._device.start_application()
        cls.setUpNativeApp()

    @classmethod
    def tearDownClass(cls):
        cls._device.close_app()
        cls._device.quit()
        cls.custom_tearDown()
        if cls.__ob_config and tests.settings.backend_env != 'prod':
            ob_config = cls.get_ob_config()
            events = ob_config.CREATED_EVENTS
            if cls.delete_events and (len(events) > 0):
                for event_id in events:
                    ob_config.change_event_state(event_id=event_id)
        cls.cms_tearDown()

    def assertEquals(self, actual, expected, msg=''):
        self.assertEqual(actual, expected, msg=f'{msg},\nActual: [{actual}]\nExpected: [{expected}]')

    def tearDown(self):
        if (self._testMethodName == self._test_steps[-1]) and self._failed_asserts:
            raise TestFailure(message='\n'.join(self._failed_asserts))

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
    def cms_setUp(cls):
        """
        Pre-setup for CMS before browser starts
        """
        pass

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
    def setUpNativeApp(cls):
        brand = cls.brand
        apps = {
            'bma': CoralNativeApp,
            'ladbrokes': LadbrokesNativeApp
        }
        app = apps.get(brand)
        cls._logger.info(f'*** Recognized {app.__name__} for "{brand}" brand and "{cls.device_name}" device')
        cls._native_app = app()

    @property
    def native_app(self):
        return self._native_app

    @property
    def device(self):
        if not self._device:
            self.setUpSite()
        return self._device

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

        event_hubs = cms_config._created_event_hubs
        for event_hub_id in event_hubs:
            cms_config.delete_event_hub_module(event_hub_id)

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
            if tests.platform == Platform.BROWSER_STACK:
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
                self._logger.error(msg=executor_object)
                browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
                self.device.driver.execute_script(browserstack_executor)
        else:
            if tests.platform == Platform.BROWSER_STACK:
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
