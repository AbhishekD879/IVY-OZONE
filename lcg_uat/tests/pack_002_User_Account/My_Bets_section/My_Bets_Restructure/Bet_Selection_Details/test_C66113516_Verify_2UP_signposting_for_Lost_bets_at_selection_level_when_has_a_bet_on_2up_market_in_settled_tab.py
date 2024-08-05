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
class Test_C66113516_Verify_2UP_signposting_for_Lost_bets_at_selection_level_when_has_a_bet_on_2up_market_in_settled_tab(Common):
    """
    TR_ID: C66113516
    NAME: Verify 2UP signposting  for Lost bets at selection level when has a bet on 2up market in settled tab
    DESCRIPTION: This testcase verifies 2UP signposting  for Lost bets in Settled tab at selection level when has a bet on  2up market
    PRECONDITIONS: Bets which are placed on 2UP market should be avilable in Open, Cashout,Settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_click_settled_tab(self):
        """
        DESCRIPTION: Click settled tab
        EXPECTED: Settled tab is opened
        """
        pass

    def test_004_verify_bets_which_are_placed_on_2_up_market_selections_in_settled_tab(self):
        """
        DESCRIPTION: Verify Bets which are placed on 2 UP market selections in Settled tab
        EXPECTED: 2 UP signposting should be displayed
        """
        pass

    def test_005_verify_the_2up_signposting(self):
        """
        DESCRIPTION: Verify the 2UP signposting
        EXPECTED: It should be displayed with 50% opacity. It should as per figma provided
        EXPECTED: ![](index.php?/attachments/get/8a0940bd-efe7-41e6-9596-b376b8e321de)
        """
        pass
