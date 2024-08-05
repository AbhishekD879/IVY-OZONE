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
class Test_C62912847_Verify_the_display_of_message_component_HomeHRVirtualfootball_AR_User_Low_Medium_Risk(Common):
    """
    TR_ID: C62912847
    NAME: Verify the display of  message component-Home,HR,Virtual&football_AR User-Low/Medium Risk
    DESCRIPTION: This test case verifies user gets message component based on the user category
    PRECONDITIONS: Login to CMS ->
    PRECONDITIONS: Navigate to ARC creation screen->
    PRECONDITIONS: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-> Set Risk level as LOW, Model as AR ,MOH as TBD
    PRECONDITIONS: Frequency : 30 Days
    """
    keep_browser_open = True

    def test_001_user_log_into_oxygen_application_and_land_on_homepage(self):
        """
        DESCRIPTION: User log into Oxygen Application and land on Homepage
        EXPECTED: User logged in successfully and landed on Homepage of the application
        """
        pass

    def test_002_verify_message_component_display_in_home_page(self):
        """
        DESCRIPTION: Verify Message Component display in home page
        EXPECTED: Message Component should display in homepage
        """
        pass

    def test_003_navigate_to_footballhorce_racingvirtual_sports_and_verify_message_component_is_display(self):
        """
        DESCRIPTION: Navigate to Football,Horce Racing,Virtual Sports and verify Message component is display
        EXPECTED: Message Component should display on Football , Horce Racing and Virtual landing pages
        """
        pass

    def test_004_verify_the_same_functionality_for_medium_risk_level_user_too(self):
        """
        DESCRIPTION: Verify the same functionality for Medium risk level user too
        EXPECTED: Message Component should display on homepage,Football , Horce Racing and Virtual landing pages
        """
        pass
