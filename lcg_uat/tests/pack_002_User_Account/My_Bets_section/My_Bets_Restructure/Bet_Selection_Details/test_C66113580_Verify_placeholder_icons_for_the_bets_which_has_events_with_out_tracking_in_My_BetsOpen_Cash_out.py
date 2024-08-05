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
class Test_C66113580_Verify_placeholder_icons_for_the_bets_which_has_events_with_out_tracking_in_My_BetsOpen_Cash_out(Common):
    """
    TR_ID: C66113580
    NAME: Verify placeholder/icons for the bets which has events with out tracking in My Bets(Open, Cash out)
    DESCRIPTION: This testcase verifies placeholder/icons for the bets which has events with out tracking in My Bets(Open, Cash out)
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

    def test_003_place_any_acca_bet_using_multiple_sellections_from_different_preplay_events(self):
        """
        DESCRIPTION: Place any acca bet using multiple sellections from different preplay events
        EXPECTED: Bet placed successfully
        """
        pass

    def test_004_verift_acca_bet_placed_in_step4(self):
        """
        DESCRIPTION: verift acca bet placed in step4
        EXPECTED: No icons should be displayed for the selections of preplay events. No placeholder should be displayed for the selections with out tracking.
        EXPECTED: ![](index.php?/attachments/get/32025b86-a6cc-44c7-91b5-f72157ea7e14)
        """
        pass

    def test_005_repeat_4_and_5_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat 4 and 5 in Cash out tab
        EXPECTED: result should be same
        """
        pass

    def test_006_repeat_step_4_7_for_single_bets(self):
        """
        DESCRIPTION: Repeat step 4-7 for single bets
        EXPECTED: Result should be same
        """
        pass
