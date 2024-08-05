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
class Test_C60709316_Euro_Loyalty__Content_area_and_navigation_competition_hub(Common):
    """
    TR_ID: C60709316
    NAME: Euro Loyalty - Content area and navigation competition hub
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

    def test_003_verify_content_area(self):
        """
        DESCRIPTION: Verify content area
        EXPECTED: Content are should contain white background
        EXPECTED: Label Next matches should display and the link to respective compitition should display
        """
        pass

    def test_004_click_on_the_link_provided_for_the_compitition(self):
        """
        DESCRIPTION: Click on the link provided for the compitition
        EXPECTED: User should navigate to respective compitition hub
        """
        pass

    def test_005_repeat_above_steps_for_users_with_different_tiers(self):
        """
        DESCRIPTION: Repeat above steps for users with different tiers
        EXPECTED: Should work as expected
        """
        pass
