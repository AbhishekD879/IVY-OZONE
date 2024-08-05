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
class Test_C62912840_Verify_the_display_of_message_component_on_HomeHRVirtualFootball_PG_User_Risk_Change__Low_to_Medium15_to_7_days(Common):
    """
    TR_ID: C62912840
    NAME: Verify the display of message component on Home,HR,Virtual,Football_PG User-Risk Change - Low to Medium[15 to 7 days]
    DESCRIPTION: This test case verifies user gets message component based on the user category
    PRECONDITIONS: Login to CMS -&gt;
    PRECONDITIONS: Navigate to ARC creation screen-&gt;
    PRECONDITIONS: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-&gt; Set Risk level as LOW, Model as PG,MOH as TBD and Frequency is 15 days
    PRECONDITIONS: Frequency: 7 Days for Medium Risk user
    PRECONDITIONS: Frequency : 15 days for Low Risk user
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

    def test_004_login_to_cms__gt(self):
        """
        DESCRIPTION: Login to CMS -&gt;
        EXPECTED: CMS data saved
        """
        pass

    def test_005_navigate_to_arc_creation_screen_gt(self):
        """
        DESCRIPTION: Navigate to ARC creation screen-&gt;
        EXPECTED: 
        """
        pass

    def test_006_in_cms_populate_all_fields_with_valid_data_modelrisk_levelmoh_type_and_user_profile_gt_set_risk_level_as_medium_model_as_pgmoh_as_tbd_and_frequency_to_7_days(self):
        """
        DESCRIPTION: In CMS Populate all fields with valid data (Model,Risk Level,MoH type and user profile)-&gt; Set Risk level as Medium, Model as PG,MOH as TBD and Frequency to 7 days
        EXPECTED: 
        """
        pass

    def test_007_logout_from_oxygen_application(self):
        """
        DESCRIPTION: Logout from Oxygen application
        EXPECTED: User logged out
        """
        pass

    def test_008_again_user_log_into_oxygen_application_and_land_on_homepage(self):
        """
        DESCRIPTION: Again User log into Oxygen Application and land on Homepage
        EXPECTED: User logged in successfully and landed on Homepage of the application
        """
        pass

    def test_009_verify_message_component_display_in_home_page(self):
        """
        DESCRIPTION: Verify Message Component display in home page
        EXPECTED: Message Component should display in homepage
        """
        pass

    def test_010_navigate_to_footballhorce_racingvirtual_sports_and_verify_message_component_is_display(self):
        """
        DESCRIPTION: Navigate to Football,Horce Racing,Virtual Sports and verify Message component is display
        EXPECTED: Message Component should display on Football , Horce Racing and Virtual landing pages
        """
        pass
