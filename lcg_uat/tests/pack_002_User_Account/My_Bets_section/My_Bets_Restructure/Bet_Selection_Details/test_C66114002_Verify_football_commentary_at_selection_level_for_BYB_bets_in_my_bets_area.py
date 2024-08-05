import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66114002_Verify_football_commentary_at_selection_level_for_BYB_bets_in_my_bets_area(Common):
    """
    TR_ID: C66114002
    NAME: Verify football commentary at selection level for BYB bets in my bets area
    DESCRIPTION: This test case is to Verify football commentary at selection level for BYB bets in my bets area
    PRECONDITIONS: BYB data should be available to place bets
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_001_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be able to logged in.
        """
        pass

    def test_002_go_to_football_from_sports_ribbon_a_z_menu_and_check_events_which_have_byb_availablity(self):
        """
        DESCRIPTION: Go to Football from Sports ribbon/ A-Z menu and check events which have byb availablity
        EXPECTED: Should be able to find byb available events
        """
        pass

    def test_003_place_a_byb_bet_from_edp(self):
        """
        DESCRIPTION: Place a BYB bet from EDP
        EXPECTED: Should be able to place byb bet from EDP
        """
        pass

    def test_004_go_to_mybets_and_verify_the_location_of_football_commentary_under_open_bets(self):
        """
        DESCRIPTION: Go to mybets and verify the location of football commentary under open bets
        EXPECTED: The location of the football commentary should be displayed below event name as per figma
        EXPECTED: ![](index.php?/attachments/get/d1815734-3307-42f6-833e-a9d3832c22e6)
        """
        pass

    def test_005_go_to_cashout_tab_and_verify_the_location_of_football_commentary_under_cashout_betsif_available(self):
        """
        DESCRIPTION: Go to Cashout tab and verify the location of football commentary under cashout bets(if available)
        EXPECTED: The location of the football commentary should be displayed below event name as per figma
        EXPECTED: ![](index.php?/attachments/get/1ce87558-e294-49f9-8007-235bceba533d)
        """
        pass
