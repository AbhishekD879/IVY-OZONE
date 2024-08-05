import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.pages.shared import get_driver


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_account
@pytest.mark.remember_me
@pytest.mark.multisession
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.timeout(850)
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C352446_Log_out_during_multiple_log_in_when_Remember_me_option_is_set(BaseUserAccountTest):
    """
    TR_ID: C352446
    NAME: Log out during multiple log in when Remember me option is set
    DESCRIPTION: This test case verifies log out during multiple log in when 'Remember me' option is set
    PRECONDITIONS: 1. User should have 'Not defined' session limits
    """
    keep_browser_open = True
    username = None
    driver_backup = None
    site2 = None

    def test_001_load_oxygen_app_and_log_in_from_device_1_with_remember_me_option_set(self):
        """
        DESCRIPTION: Load Oxygen app and log in from Device 1 with 'Remember me' option set
        EXPECTED: User is logged in successfully with permanent session
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username, remember_me=True, async_close_dialogs=False)

    def test_002_load_oxygen_app_and_log_in_with_the_same_credentials_on_device_2(self, remember_me=False):
        """
        DESCRIPTION: Load Oxygen app and log in with the same credentials on Device 2
        EXPECTED: User is logged in successfully without permanent session
        """
        self.__class__.driver_backup = get_driver()
        self.__class__.device_backup = self.device
        self.__class__.site2 = self.create_new_browser_instance()
        self.site2.login(username=self.username, remember_me=remember_me,
                         timeout_wait_for_dialog=3, async_close_dialogs=False)

    def test_003_log_out_from_device_2(self):
        """
        DESCRIPTION: Log out from Device 2
        EXPECTED: User is logged out
        """
        self.site2.logout()

    def test_004_navigate_through_device_1(self):
        """
        DESCRIPTION: Navigate through Device 1
        EXPECTED: User stays logged in
        EXPECTED: Session is NOT expired on Device 1
        """
        self.set_driver(driver=self.driver_backup, device=self.device_backup)

        self.navigate_to_page(name='sport/football')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        logged_in = self.site.wait_logged_in()
        self.assertTrue(logged_in, msg='User is not logged in')
        self.site.logout()

    def test_005_repeat_steps_1_4_but_on_step_2_log_in_with_remember_me_option_set(self):
        """
        DESCRIPTION: Repeat steps #1-4 but on step 2 log in with 'Remember me' option set
        EXPECTED: Repeated previous steps
        """
        self.test_001_load_oxygen_app_and_log_in_from_device_1_with_remember_me_option_set()
        self.test_002_load_oxygen_app_and_log_in_with_the_same_credentials_on_device_2(remember_me=True)
        self.test_003_log_out_from_device_2()
        self.test_004_navigate_through_device_1()
