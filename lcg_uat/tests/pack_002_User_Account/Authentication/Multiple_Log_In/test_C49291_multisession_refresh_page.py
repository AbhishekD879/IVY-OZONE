import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.pages.shared import get_driver


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.multisession
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C49291_Multisession_Refresh_Page(BaseUserAccountTest, BaseSportTest):
    """
    TR_ID: C49291
    NAME: Check that user still logged in both browsers after refreshed page
    """
    keep_browser_open = True

    def test_001_login_in_first_browser(self):
        """
        DESCRIPTION: Login as default user
        EXPECTED: Logged in as default user
        """
        self.__class__.user = tests.settings.betplacement_user
        self.site.login(self.user, async_close_dialogs=False)
        self.__class__.driver_backup = get_driver()
        self.__class__.device_backup = self.device

    def test_002_create_new_instance(self):
        """
        DESCRIPTION: Create new instance of the browser with backup
        EXPECTED: New browser instance is created
        """
        self.__class__.site2 = self.create_new_browser_instance()

    def test_003_login_in_second_browser(self):
        """
        DESCRIPTION: Login as default user in second browser
        EXPECTED: Logged in as default user in second browser
        """
        self.site2.wait_splash_to_hide()
        self.site2.wait_content_state('HomePage', timeout=10)
        self.site2.login(self.user)

    def test_004_refresh_page(self):
        """
        DESCRIPTION: Make refresh of the page
        EXPECTED: Page was refreshed
        """
        self.device.refresh_page()
        self.site2.wait_splash_to_hide()

    def test_005_verify_user_is_still_logged_in_browser2(self):
        """
        DESCRIPTION: Verify that user still logged in
        EXPECTED: User still logged in
        """
        self.site2.wait_content_state('HomePage', timeout=10)
        self.site2.wait_logged_in()

    def test_006_close_site2(self):
        """
        DESCRIPTION: Turn off from site 2. Browser would be closed
        EXPECTED: Browser 2 is closed
        """
        self.device.driver.quit()
        self.set_driver(self.driver_backup, device=self.device_backup)

    def test_007_refresh_page_browser1(self):
        """
        DESCRIPTION: Make refresh of the page
        EXPECTED: Home page is opened
        """
        self.site.wait_content_state('HomePage')

    def test_008_verify_user_is_still_logged_in_browser1(self):
        """
        DESCRIPTION: Verify that user still logged in browser1
        """
        self.site.wait_content_state('HomePage', timeout=10)
        self.site.wait_logged_in()
