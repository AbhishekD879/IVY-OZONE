import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66067966_Verify_Toggle_ON_OFF_for_Show_Bets_Based_on_your_team_and_Show_bets_based_on_other_Fanzone_team_in_Fanzone_configurations(Common):
    """
    TR_ID: C66067966
    NAME: Verify Toggle ON/OFF for Show Bets Based on your team and Show bets based on other Fanzone team in Fanzone configurations
    DESCRIPTION: This test case is to verify the Toggle ON/OFF for Show Bets Based On Your Team and Show bets based on other Fanzone team module in Fanzone Configurations
    PRECONDITIONS: CMS is launched and login with Valid Credentials
    """
    keep_browser_open = True

    def test_000_launch_the_cms_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the CMS and login with valid credentials
        EXPECTED: Able to launch CMS and login successfully
        """
        pass

    def test_000_navigate_to_the_fanzone_in_the_sports_categories__ampgt_fanzone__ampgt_fanzones__ampgt_fanzone_configurations(self):
        """
        DESCRIPTION: Navigate to the Fanzone in the Sports Categories -&amp;gt; Fanzone -&amp;gt; Fanzones -&amp;gt; Fanzone Configurations
        EXPECTED: Able to navigate to the Fanzone page
        """
        pass

    def test_000_verify_the_toggle_displaying_for_show_bets_based_on_your_team_and_show_bets_based_on_other_fanzone_team_modules(self):
        """
        DESCRIPTION: Verify the Toggle displaying for Show Bets Based On Your Team and Show bets based on other Fanzone team modules
        EXPECTED: Able to see the Toggle for Show Bets Based On Your Team and Show bets based on other Fanzone team modules
        """
        pass

    def test_000_onoff_the_toggle_and_verify(self):
        """
        DESCRIPTION: ON/OFF the Toggle and verify
        EXPECTED: Able to Turn on/off the Toggle successfully
        """
        pass

    def test_000_click_on_save_changes_and_verify(self):
        """
        DESCRIPTION: Click on Save Changes and Verify
        EXPECTED: Able to save the changes
        """
        pass
