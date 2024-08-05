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
class Test_C60709317_Euro_Loyalty_Go_betting_button(Common):
    """
    TR_ID: C60709317
    NAME: Euro Loyalty -Go betting button
    DESCRIPTION: This test case is to validate display of badge in FE
    DESCRIPTION: This test case is to validate display of badge in FE
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created,activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyality_page(self):
        """
        DESCRIPTION: Navigate to Euro Loyality page
        EXPECTED: Matchday rewards page should display with all the details
        """
        pass

    def test_003_verify_go_betting_button(self):
        """
        DESCRIPTION: Verify Go betting button
        EXPECTED: Green Go betting button should display below to the content area
        """
        pass

    def test_004_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on Go betting button
        EXPECTED: User should navigate to respective EDP
        """
        pass

    def test_005_repeat_above_steps_for_users_with_different_tiers(self):
        """
        DESCRIPTION: Repeat above steps for users with different tiers
        EXPECTED: Should work as expected
        """
        pass

    def test_006_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_007_navigate_to_euro_loyality_page(self):
        """
        DESCRIPTION: Navigate to Euro Loyality page
        EXPECTED: Matchday rewards page should display with all the details
        """
        pass

    def test_008_verify_go_betting_button(self):
        """
        DESCRIPTION: Verify Go betting button
        EXPECTED: Green Go betting button should display below to the content area
        """
        pass

    def test_009_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on Go betting button
        EXPECTED: User should navigate to respective EDP
        """
        pass

    def test_010_repeat_above_steps_for_users_with_different_tiers(self):
        """
        DESCRIPTION: Repeat above steps for users with different tiers
        EXPECTED: Should work as expected
        """
        pass
