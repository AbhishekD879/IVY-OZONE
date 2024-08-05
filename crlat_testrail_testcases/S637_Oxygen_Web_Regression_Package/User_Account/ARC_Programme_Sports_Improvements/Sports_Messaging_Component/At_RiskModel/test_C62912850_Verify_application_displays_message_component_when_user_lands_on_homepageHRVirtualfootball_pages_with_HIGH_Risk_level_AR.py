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
class Test_C62912850_Verify_application_displays_message_component_when_user_lands_on_homepageHRVirtualfootball_pages_with_HIGH_Risk_level_AR(Common):
    """
    TR_ID: C62912850
    NAME: Verify application displays message component when user lands on homepage,HR,Virtual&football pages with HIGH  Risk level_AR
    DESCRIPTION: This test case verifies user gets message component based on the user category
    PRECONDITIONS: Login to CMS ->
    PRECONDITIONS: Navigate to ARC creation screen->
    PRECONDITIONS: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-> Set Risk level as HIGH , Model as AR ,MOH as TBD
    PRECONDITIONS: Frequency : 15 Days
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
