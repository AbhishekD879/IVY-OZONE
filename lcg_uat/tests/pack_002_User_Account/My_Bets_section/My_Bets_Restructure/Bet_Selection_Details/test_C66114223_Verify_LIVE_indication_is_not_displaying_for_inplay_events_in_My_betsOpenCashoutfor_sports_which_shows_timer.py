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
class Test_C66114223_Verify_LIVE_indication_is_not_displaying_for_inplay_events_in_My_betsOpenCashoutfor_sports_which_shows_timer(Common):
    """
    TR_ID: C66114223
    NAME: Verify  LIVE indication is not displaying  for inplay events in My bets(Open,Cashout)for sports which shows timer
    DESCRIPTION: This testcase verifies LIVE indication is not displaying  for inplay events in My bets(Open,Cashout)for sports which shows timer
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

    def test_002_place_bet_by_adding_selections_of_inplay_events_which_shows_timer(self):
        """
        DESCRIPTION: Place bet by adding selections of inplay events which shows timer
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_live_signposting_at_selection_level_for_the_events_which_have_timer(self):
        """
        DESCRIPTION: Verify Live signposting at selection level for the events which have timer
        EXPECTED: LIVE signposting should not be displayed at selection level for the events which have timer
        """
        pass

    def test_005_click_on_cash_out_tab(self):
        """
        DESCRIPTION: Click on cash out tab
        EXPECTED: Cash out tab is opened
        """
        pass

    def test_006_verify_live_signposting_at_selection_level_for_the_events_which_have_timer(self):
        """
        DESCRIPTION: Verify Live signposting at selection level for the events which have timer
        EXPECTED: LIVE signposting should not be displayed at selection level for the events which have timer
        """
        pass
