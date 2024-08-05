import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.pages.shared import get_driver
from voltron.pages.shared import set_driver


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.account
@pytest.mark.multisession
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C16268987_Vanilla_Verify_multiple_log_in_from_different_devices_at_the_same_time(BaseUserAccountTest):
    """
    TR_ID: C16268987
    NAME: [Vanilla] Verify multiple log in from different devices at the same time
    DESCRIPTION: This test case verifies multiple login in from different devices at the same time.
    PRECONDITIONS: A user should be able to log into their Sportbook account from as multiple devices with the same IP address
    """
    keep_browser_open = True
    driver_backup, driver_backup2 = None, None
    site2 = None
    sport_name = vec.sb.FOOTBALL if tests.settings.brand == 'ladbrokes' else vec.sb.FOOTBALL.upper()

    def test_001_load_oxygen_and_log_in_from_device_1(self):
        """
        DESCRIPTION: Load Oxygen and log in from Device 1
        EXPECTED: User is logged in
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username, async_close_dialogs=False)
        self.assertTrue(self.site.wait_logged_in(timeout=1), msg='User is not logged in on site 1')

    def test_002_load_oxygen_and_log_in_the_same_account_from_device_2(self):
        """
        DESCRIPTION: Load Oxygen and log in the same account from Device 2
        EXPECTED: User is logged in
        """
        self.__class__.driver_backup = get_driver()
        self.__class__.device_backup = self.device
        self.__class__.site2 = self.create_new_browser_instance()
        self.site2.wait_splash_to_hide()
        self.site2.wait_content_state('HomePage', timeout=10)
        self.site2.login(username=self.username)

    def test_003_reload_app_via_browser_refresh_button_and_check_whether_user_stays_logged_in_from_device_1(self):
        """
        DESCRIPTION: Reload app via browser refresh button and check whether User stays logged in from Device 1
        EXPECTED: User stays logged in
        """
        self.__class__.driver_backup2 = get_driver()
        self.__class__.device_backup2 = self.device
        self.set_driver(driver=self.driver_backup, device=self.device_backup)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(timeout=1), msg='User is not logged in on site 1')

    def test_004_navigate_through_the_application_from_device_1(self):
        """
        DESCRIPTION: Navigate through the application from Device 1
        EXPECTED: User stays logged in
        """
        self.site.open_sport(name=self.sport_name.upper()) if self.brand == "bma" else \
            self.site.open_sport(name=self.sport_name)
        self.assertTrue(self.site.wait_logged_in(timeout=1), msg='User is not logged in on site 1')

    def test_005_navigate_through_the_application_from_device_2(self):
        """
        DESCRIPTION: Navigate through the application from Device 2
        EXPECTED: User stays logged in
        """
        set_driver(self.driver_backup2)
        self.site2.open_sport(name=self.sport_name)
        self.site2.wait_content_state(state_name='Football')
        self.assertTrue(self.site2.wait_logged_in(timeout=1), msg='User is not logged in on site 2')

    def test_006_make_logout_from_device_1(self):
        """
        DESCRIPTION: Make logout from Device 1
        EXPECTED: User is logged out
        """
        self.set_driver(driver=self.driver_backup, device=self.device_backup)
        self.site.logout()

    def test_007_check_whether_user_is_logged_out_from_device_2(self):
        """
        DESCRIPTION: Check whether User is logged out from Device 2
        EXPECTED: User is logged in
        """
        set_driver(self.driver_backup2)
        self.assertTrue(self.site2.wait_logged_in(timeout=1), msg='User is not logged in on site 2')
