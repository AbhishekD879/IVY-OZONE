import logging

from tests.base_test import BaseTest
from voltron.device.device_manager import DeviceManager
from voltron.native.oxygen_app import OxygenApp
from voltron.utils.exceptions.failure_exception import TestFailure


class NativeBaseTest(BaseTest):
    oxygen_app = None
    logger = None
    _user = ''
    update_tstrail_case = False

    @classmethod
    def setUpClass(cls):
        steps = sorted((step_name for step_name, step in cls.__dict__.items() if step_name.startswith('test_')))
        cls._test_steps = steps
        cls.logger = logging.getLogger('voltron_logger')
        cls._device = DeviceManager(device_name=cls.device_name).get_device()
        cls._device.start_application()
        if cls.oxygen_app is None:
            cls.oxygen_app = OxygenApp()

    @property
    def site(self):
        return OxygenApp().web_content

    @classmethod
    def tearDownClass(cls):
        cls._device.close_app()
        cls._device.quit()

    def assertEquals(self, actual, expected, msg=''):
        self.assertEqual(actual, expected, msg=f'{msg},\nActual: [{actual}]\nExpected: [{expected}]')

    @classmethod
    def set_device_name(cls):
        """
        User to set actual device name needed for run
        Method is added to handle CI runs
        :return:
        """
        cls.device_name = 'Native Mobile'

    def tearDown(self):
        if (self._testMethodName == self._test_steps[-1]) and self._failed_asserts:
            raise TestFailure(message='\n'.join(self._failed_asserts))
