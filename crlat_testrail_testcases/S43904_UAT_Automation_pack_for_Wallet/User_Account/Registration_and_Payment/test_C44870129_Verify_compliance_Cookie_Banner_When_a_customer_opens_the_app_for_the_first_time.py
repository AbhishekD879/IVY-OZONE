import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870129_Verify_compliance_Cookie_Banner_When_a_customer_opens_the_app_for_the_first_time(Common):
    """
    TR_ID: C44870129
    NAME: Verify  compliance Cookie Banner ,When a customer opens the app for the first time
    DESCRIPTION: When a customer opens the app for the first time, compliance cookie message should be displayed to them. Once the browser cache has been cleared the cookie banner will reappear
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: Homepage is opened
        EXPECTED: Cookies Notification Banner is displayed above the Header at the top of the page
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
        EXPECTED: Cookies Notification Banner is closed and no more displayed
        """
        pass

    def test_005_navigate_through_app(self):
        """
        DESCRIPTION: Navigate through app
        EXPECTED: Cookies Notification Banner is NOT displayed
        """
        pass

    def test_006_clear_local_storage_and_refresh_the_page(self):
        """
        DESCRIPTION: Clear local storage and refresh the page
        EXPECTED: Cookies Notification Banner is displayed above the Header at the top of the page
        """
        pass

    def test_007_log_in_and_repeat_steps_steps__1_6(self):
        """
        DESCRIPTION: Log in and repeat steps steps # 1-6
        EXPECTED: 
        """
        pass
