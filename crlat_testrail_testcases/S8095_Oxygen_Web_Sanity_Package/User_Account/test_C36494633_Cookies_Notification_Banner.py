import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C36494633_Cookies_Notification_Banner(Common):
    """
    TR_ID: C36494633
    NAME: Cookies Notification Banner
    DESCRIPTION: This test case verifies Cookies Notification Banner functionality
    DESCRIPTION: AUTOMATED [C45730013]
    PRECONDITIONS: **Cookie Banner is handled on GVC side (Enabling/Disabling, Text configuration, URL navigation )**
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: 2. User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: - Homepage is opened
        EXPECTED: - Cookies Notification Banner is displayed at the Bottom
        EXPECTED: ![](index.php?/attachments/get/17649891)
        """
        pass

    def test_002_navigate_through_app(self):
        """
        DESCRIPTION: Navigate through app
        EXPECTED: Cookies Notification Banner is displayed within app
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Cookies Notification Banner is still displayed
        """
        pass

    def test_004_click__tap_ok_button_on_cookies_notification_banner(self):
        """
        DESCRIPTION: Click / tap 'OK' button on Cookies Notification Banner
        EXPECTED: - Cookies Notification Banner is closed and no more displayed
        EXPECTED: (Note: 'euconsent' parameter is set with value 'a' and expiry date for a year in future)
        EXPECTED: ![](index.php?/attachments/get/17649960)
        """
        pass

    def test_005_navigate_through_app(self):
        """
        DESCRIPTION: Navigate through app
        EXPECTED: Cookies Notification Banner is NOT displayed
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Cookies Notification Banner is NOT displayed
        """
        pass

    def test_007_clear_cookies_and_refresh_the_page(self):
        """
        DESCRIPTION: Clear Cookies and refresh the page
        EXPECTED: Cookies Notification Banner is again displayed at the Bottom of page
        """
        pass
