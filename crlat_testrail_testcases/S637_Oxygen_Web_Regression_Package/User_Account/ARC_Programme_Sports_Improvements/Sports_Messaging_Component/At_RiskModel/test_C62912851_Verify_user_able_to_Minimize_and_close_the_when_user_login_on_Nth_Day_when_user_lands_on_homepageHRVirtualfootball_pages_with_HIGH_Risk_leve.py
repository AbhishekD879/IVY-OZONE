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
class Test_C62912851_Verify_user_able_to_Minimize_and_close_the_when_user_login_on_Nth_Day_when_user_lands_on_homepageHRVirtualfootball_pages_with_HIGH_Risk_level_AR(Common):
    """
    TR_ID: C62912851
    NAME: Verify user able to Minimize and close the when user login on Nth Day when user lands on homepage,HR,Virtual&football pages with HIGH Risk level_AR
    DESCRIPTION: This test case verifies user minimize and close message component based on the user category
    PRECONDITIONS: Login to CMS ->
    PRECONDITIONS: Navigate to ARC creation screen->
    PRECONDITIONS: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-> Set Risk level as HIGH , Model as AR,MOH as TBD
    PRECONDITIONS: Frequency 15 Days
    """
    keep_browser_open = True

    def test_001_user_log_into_oxygen_application_and_land_on_homepage(self):
        """
        DESCRIPTION: User log into Oxygen Application and land on Homepage
        EXPECTED: User logged in successfully and landed on Homepage of the application
        """
        pass

    def test_002_navigate_to_homepagefootballhorce_racingvirtual_sports_and_verify_message_component_is_display(self):
        """
        DESCRIPTION: Navigate to Homepage,Football,Horce Racing,Virtual Sports and verify Message component is display
        EXPECTED: Message Component should display on Football , Horce Racing and Virtual landing pages
        """
        pass

    def test_003_verify_user_is_able_to_minimize_the_component_message_in_any_of_the_below_homepagehrvsfb_pages(self):
        """
        DESCRIPTION: Verify user is able to Minimize the component message in any of the below Homepage,HR,VS,FB pages
        EXPECTED: Message component is minimized, and application save the user interaction successfully, which should be displayed (in minimized state) next time.[within 15 Days]
        """
        pass

    def test_004_verify_user_is_able_to_close_the_component_message_in_any_of_the_below_homepagehrvsfb_pages(self):
        """
        DESCRIPTION: Verify user is able to Close the component message in any of the below Homepage,HR,VS,FB pages
        EXPECTED: Message component is closed, and application save the user interaction successfully, and should display next based on frequency.
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: [after 15 Days]
        """
        pass
