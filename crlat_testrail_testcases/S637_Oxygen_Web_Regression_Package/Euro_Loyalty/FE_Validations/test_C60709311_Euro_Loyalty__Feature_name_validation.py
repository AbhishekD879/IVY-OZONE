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
class Test_C60709311_Euro_Loyalty__Feature_name_validation(Common):
    """
    TR_ID: C60709311
    NAME: Euro Loyalty - Feature name validation
    DESCRIPTION: This test case verifies displaying feature name in Euro Loyalty  page after login into application
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created,activated and should be in valid date range in CMS special pages - EuroLoyality page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_navigate_to_euro_loyality_page_from_sports_ribbon_or_from_a_z_menu_in_mobile_sub_header_menu_in_desktop(self):
        """
        DESCRIPTION: Navigate to Euro Loyality page from sports ribbon or from A-Z menu in mobile/ Sub Header menu in Desktop
        EXPECTED: Feature name should display "Matchday rewards" on top of the page
        """
        pass

    def test_003_verify_header_section_of_matchday_rewads_page(self):
        """
        DESCRIPTION: Verify header section of matchday rewads page
        EXPECTED: 1.  Back button should present with < icon at top left corner
        EXPECTED: 2.  it should be in disabled mode if any pop up is opened
        EXPECTED: 3.  Click on back button it should navigate to respective page
        EXPECTED: 4.  Top right corner user menu, avaliable balance and betslip should present
        """
        pass
