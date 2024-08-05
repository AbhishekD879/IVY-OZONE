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
class Test_C62912846_Verify_minimize_option_for_message_component_on_Nth_Day_Login_PG_User_HighVery_High_Risk_Permanent(Common):
    """
    TR_ID: C62912846
    NAME: Verify minimize option for message component on Nth Day Login- PG User -High,Very High Risk_Permanent
    DESCRIPTION: This test case verifies user minimize message component based on the user category
    PRECONDITIONS: Login to CMS ->
    PRECONDITIONS: Navigate to ARC creation screen->
    PRECONDITIONS: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-> Set Risk level as High, Model as PG,MOH as TBD
    PRECONDITIONS: Frequency : Permanent Display
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

    def test_003_verify_user_is_able_to_minimize_the_component_message(self):
        """
        DESCRIPTION: Verify user is able to Minimize the component message
        EXPECTED: Message component is minimized, and application save the user interaction successfully which should be displayed next time.[Permanent]
        """
        pass

    def test_004_verify_the_same_functionality_for_very_high_level_user_too(self):
        """
        DESCRIPTION: Verify the same functionality for Very High level user too
        EXPECTED: Message component is minimized, and application save the user interaction successfully which should be displayed next time.[Permanent]
        """
        pass
