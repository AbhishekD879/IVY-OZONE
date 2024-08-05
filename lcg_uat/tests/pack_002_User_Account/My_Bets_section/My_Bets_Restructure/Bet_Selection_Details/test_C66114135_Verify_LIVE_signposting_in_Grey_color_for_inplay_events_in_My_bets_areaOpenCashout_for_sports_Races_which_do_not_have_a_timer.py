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
class Test_C66114135_Verify_LIVE_signposting_in_Grey_color_for_inplay_events_in_My_bets_areaOpenCashout_for_sports_Races_which_do_not_have_a_timer(Common):
    """
    TR_ID: C66114135
    NAME: Verify LIVE signposting in Grey color for inplay events in My bets area(Open,Cashout) for sports /Races which do not have a timer.
    DESCRIPTION: This testcase verifies LIVE signposting in Grey color for inplay events in My bets area(Open,Cashout) for sports /Races which do not have a timer.
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

    def test_002_place_bet_by_adding_selections_of_inplay_events_which_do_not_have_timer(self):
        """
        DESCRIPTION: Place bet by adding selections of inplay events which do not have timer
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_live_signposting_at_selection_level_for_the_events_which_do_not_have_timer(self):
        """
        DESCRIPTION: Verify Live signposting at selection level for the events which do not have timer
        EXPECTED: LIVE signposting should be displayed in Grey color  for the events which do not have timer
        """
        pass

    def test_005_click_on_cash_out(self):
        """
        DESCRIPTION: Click on cash out
        EXPECTED: Cash out tab is opened
        """
        pass

    def test_006_verify_live_signposting_at_selection_level_for_the_events_which_do_not_have_timer(self):
        """
        DESCRIPTION: Verify Live signposting at selection level for the events which do not have timer
        EXPECTED: LIVE signposting should be displayed in Grey color for the events which do not have timer
        """
        pass
