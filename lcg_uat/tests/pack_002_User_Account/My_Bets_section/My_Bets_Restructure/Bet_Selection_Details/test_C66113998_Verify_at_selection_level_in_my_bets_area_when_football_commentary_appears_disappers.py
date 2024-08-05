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
class Test_C66113998_Verify_at_selection_level_in_my_bets_area_when_football_commentary_appears_disappers(Common):
    """
    TR_ID: C66113998
    NAME: Verify at selection level in my bets area when football commentary appears/disappers
    DESCRIPTION: This testcase verifies at selection level in my bets area when football commentary appears/disappers
    PRECONDITIONS: Football bets on inplay events should be available in Open,Cashout,Settled tabs. Commentary should be available for the events showing in Open,Cash out,Settled tabs
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_football_bets_for_which_commentary_is_available_in_open_tab(self):
        """
        DESCRIPTION: Verify football bets for which commentary is available in open tab
        EXPECTED: Commentary should be displayed at bet selection area as per figma
        """
        pass

    def test_004_verify_when_commentary_disappears_at_bet_selection_area(self):
        """
        DESCRIPTION: Verify When commentary disappears at bet selection area
        EXPECTED: no additional space should be displayed for the commentary when it disappers
        """
        pass

    def test_005_verify_when_commentary_appears_again_at_bet_selection_area(self):
        """
        DESCRIPTION: Verify When commentary appears again at bet selection area
        EXPECTED: Commentary display area to be &acirc;&euro;&tilde;permanent&acirc;&euro;&trade;and commentary doesn&acirc;&euro;&trade;t slide in / out  and also else commentary reappears with out page up/down.
        """
        pass

    def test_006_repeat__step_4_6_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat  Step 4-6 in cash out tab
        EXPECTED: Result should be same
        """
        pass
