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
class Test_C66116394_Verify_new_iconography_for_status_icons_for_horse_racing_bets_in_My_BetsOpenCash_outSettled_for_single_and_multiple_bets(Common):
    """
    TR_ID: C66116394
    NAME: Verify new iconography for status icons for horse racing bets in My Bets(Open,Cash out,Settled) for single and multiple bets
    DESCRIPTION: This testcase verifies new iconography for status icons for horse racing bets in My Bets(Open,Cash out,Settled) for single and multiple bets
    PRECONDITIONS: Single and multiple bets on Horse racing  should be available in Open,cash out,Settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_acca_bet_on_horse_racing_selections_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify acca bet on horse racing selections displayed in open tab
        EXPECTED: Bet should be diasplayed with all the bet details in expanded state
        """
        pass

    def test_004_verify_once_any_of_the_selection_gets_resulted(self):
        """
        DESCRIPTION: Verify once any of the selection gets resulted
        EXPECTED: tick/cross mark should be displayed beside the selection name which is resulted as per figma
        """
        pass

    def test_005_repeat_step_4_and_step_5_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 4 and step 5 in cash out tab
        EXPECTED: result should be same
        """
        pass

    def test_006_verify_single_and_multiple_bets_on_horse_racing_in_settled_tab(self):
        """
        DESCRIPTION: Verify single and multiple bets on horse racing in settled tab
        EXPECTED: tick/cross mark should be displayed beside the selection name which is resulted as per figma
        """
        pass
