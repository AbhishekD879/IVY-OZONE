import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60709310_Euro_Loyalty__display_order_of_UI_elements(Common):
    """
    TR_ID: C60709310
    NAME: Euro Loyalty - display order of UI elements
    DESCRIPTION: This test case verifies display order of UI components
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - EuroLoyality page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyalty_page_and_verify_ui(self):
        """
        DESCRIPTION: Navigate to Euro Loyalty page and verify UI
        EXPECTED: UI should contain following elements in the order
        EXPECTED: 1.  Feature Name
        EXPECTED: 2.  How it Works
        EXPECTED: 3.  Yellow Line
        EXPECTED: 4.  Messaging
        EXPECTED: 5.  Badges display (enable/disable)
        EXPECTED: 6.  Free Bet value
        EXPECTED: 7.  Content Area
        EXPECTED: 8.  Go Betting Link
        EXPECTED: 9.  Terms & Conditions
        EXPECTED: 10.  Badges Display - Desktop and Mobile
        """
        pass

    def test_003_repeat_above_step_for_loggedin_user(self):
        """
        DESCRIPTION: Repeat above step for loggedin user
        EXPECTED: Should work as expected
        """
        pass
