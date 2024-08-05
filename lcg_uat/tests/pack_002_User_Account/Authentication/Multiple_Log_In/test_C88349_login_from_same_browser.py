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
@pytest.mark.multisession
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C88349_Login_From_Same_Browser(BaseUserAccountTest):
    """
    TR_ID: C88349
    NAME:  Verify login from same device/ip/browser
    """
    keep_browser_open = True
    driver_backup = None

    def test_001_login_in_first_browser(self):
        """
        DESCRIPTION: Login as default user
        EXPECTED: User is logged in
        EXPECTED: Driver backup is saved
        """
        self.__class__.user = tests.settings.betplacement_user
        self.site.login(self.user, async_close_dialogs=False, timeout_close_dialogs=10)
        self.__class__.driver_backup = get_driver()
        self.__class__.device_backup = self.device

    def test_002_create_new_instance(self):
        """
        DESCRIPTION: Create new instance of the browser with backup
        EXPECTED: Created new browser instance
        """
        self.__class__.site2 = self.create_new_browser_instance()

    def test_003_login_in_second_browser(self):
        """
        DESCRIPTION: Login as default user in second browser
        EXPECTED: User logged in the second browser
        """
        self.site2.login(self.user, async_close_dialogs=False, timeout_close_dialogs=10)

    def test_004_logout_from_site2(self):
        """
        DESCRIPTION: Logout from site 2. Browser would be closed
        EXPECTED: Logout out site 2
        EXPECTED: Browser is closed
        """
        self.site2.logout()
        self.device.driver.quit()
        self.set_driver(driver=self.driver_backup, device=self.device_backup)

    def test_005_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        EXPECTED: User remains logged in
        EXPECTED: Content state Tennis is opened
        """
        self.site.wait_logged_in(timeout=2)
        self.site.open_sport(name='TENNIS')
        self.site.wait_logged_in(timeout=2)
