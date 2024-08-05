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
class Test_C62912843_Verify_message_component_display_Login_between_Nth_to_last_frequency_day_PG_User_Low_Risk(Common):
    """
    TR_ID: C62912843
    NAME: Verify message component display -Login between Nth to last frequency day-PG User -Low Risk
    DESCRIPTION: This test case verifies user minimize and close message component based on the user category
    PRECONDITIONS: Login to CMS ->
    PRECONDITIONS: Navigate to ARC creation screen->
    PRECONDITIONS: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-> Set Risk level as LOW, Model as PG,MOH as TBD
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

    def test_003_verify_user_is_able_to_minimize_and_close_component_message(self):
        """
        DESCRIPTION: Verify user is able to Minimize and Close component message
        EXPECTED: Message component is minimized and Closed,and application saved the user interaction successfully
        """
        pass

    def test_004_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen application
        EXPECTED: User logged out
        """
        pass

    def test_005_login_in_again_with_same_user_and_verify_message_component_display(self):
        """
        DESCRIPTION: Login in again with Same User and verify Message Component display
        EXPECTED: User should not get any Messaging component until next frequency. [after 15 days for Low risk User]
        """
        pass
