import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C46726_Verify_Cookies_Notification_Banner_Functionality(Common):
    """
    TR_ID: C46726
    NAME: Verify Cookies Notification Banner Functionality
    DESCRIPTION: This test case verifies Cookies Notification Banner functionality
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: - BMA-14778 Cookie Notifications On All Platforms
    DESCRIPTION: - BMA-16450 Cookie banner: Cookies are set for 5 days
    DESCRIPTION: - BMA-16483[OCC-41372] - [Oxygen][OCC] Android/iOS Wrapper - Cookie notification is shown after accepting the notification
    DESCRIPTION: - BMA-46701 Coral IOS app - please remove the cookie banner
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: 2. User is logged out
    PRECONDITIONS: 3. Make sure that Cookie Banner **is NOT DISPLAYED** on Coral iOS wrapper v.5.1.1 build 1157 and higher regardless of the CMS configuration.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: - Homepage is opened
        EXPECTED: - Cookies Notification Banner is displayed above the Header at the top of the page
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

    def test_004_click__tap_acceptclose_button_on_cookies_notification_banner(self):
        """
        DESCRIPTION: Click / tap 'Accept&close' button on Cookies Notification Banner
        EXPECTED: - Cookies Notification Banner is closed and no more displayed
        """
        pass

    def test_005__open_development_tool___application___local_storage_check_value_setting(self):
        """
        DESCRIPTION: * Open Development tool -> Application -> Local Storage
        DESCRIPTION: * Check value setting
        EXPECTED: - **'OX.cookieBaner=true'**  is set after accepting the cookie usage policy
        """
        pass

    def test_006_navigate_through_app(self):
        """
        DESCRIPTION: Navigate through app
        EXPECTED: Cookies Notification Banner is NOT displayed
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Cookies Notification Banner is still NOT displayed
        """
        pass

    def test_008_clear_local_storage_and_refresh_the_page(self):
        """
        DESCRIPTION: Clear local storage and refresh the page
        EXPECTED: Cookies Notification Banner is displayed above the Header at the top of the page
        """
        pass

    def test_009_log_in_and_repeat_steps_steps__1_7(self):
        """
        DESCRIPTION: Log in and repeat steps steps # 1-7
        EXPECTED: 
        """
        pass
