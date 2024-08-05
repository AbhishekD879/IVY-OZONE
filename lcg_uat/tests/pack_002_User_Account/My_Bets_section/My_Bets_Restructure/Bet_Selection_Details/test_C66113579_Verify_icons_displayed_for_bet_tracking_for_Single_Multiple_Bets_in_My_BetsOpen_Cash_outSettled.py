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
class Test_C66113579_Verify_icons_displayed_for_bet_tracking_for_Single_Multiple_Bets_in_My_BetsOpen_Cash_outSettled(Common):
    """
    TR_ID: C66113579
    NAME: Verify icons displayed for bet tracking  for Single/Multiple Bets in My Bets(Open, Cash out,Settled)
    DESCRIPTION: Verify icons displayed for bet tracking  for Single/Multiple Bets in My Bets(Open, Cash out)
    PRECONDITIONS: 
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

    def test_003_place_any_acca_bet_using_multiple_sellections_from_different_inplay_events(self):
        """
        DESCRIPTION: Place any acca bet using multiple sellections from different inplay events
        EXPECTED: Bet placed successfully
        """
        pass

    def test_004_verify_acca_bet_placed_in_step4_in_open_tab(self):
        """
        DESCRIPTION: Verify acca bet placed in step4 in Open Tab
        EXPECTED: Status tracking icons should be displayed for every selection as per figma provided
        EXPECTED: ![](index.php?/attachments/get/d34d20dd-643d-48e8-92e7-b74dd49c1f96)
        """
        pass

    def test_005_repeat_step_5_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 5 in Cash out tab
        EXPECTED: Status tracking icons should be displayed for every selection as per figma provided
        """
        pass

    def test_006_repeat_step_4_7_for_single_bets(self):
        """
        DESCRIPTION: Repeat step 4-7 for single bets
        EXPECTED: Result should be same
        """
        pass
