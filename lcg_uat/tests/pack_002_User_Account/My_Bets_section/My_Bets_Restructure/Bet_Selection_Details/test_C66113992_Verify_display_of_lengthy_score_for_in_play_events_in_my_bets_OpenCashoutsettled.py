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
class Test_C66113992_Verify_display_of_lengthy_score_for_in_play_events_in_my_bets_OpenCashoutsettled(Common):
    """
    TR_ID: C66113992
    NAME: Verify display of  lengthy score for in play events in my bets (Open,Cashout,settled)
    DESCRIPTION: This testcase verifies display of  lengthy score for in play events in my bets (Open,Cashout,settled)
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

    def test_002_place_bet_by_adding_selections_of_inplay_events_which_shows_lengthy_score_updates_in_my_bets_areaex_tennis(self):
        """
        DESCRIPTION: Place bet by adding selections of inplay events which shows lengthy score updates in my bets area(Ex: Tennis)
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_the_display_of__lengthy_score_for_inplay_event_in_open_tab_when_the_match_is_in_live(self):
        """
        DESCRIPTION: Verify the display of  lengthy score for inplay event in Open tab when the match is in live
        EXPECTED: The score should display in second line for consistency
        """
        pass

    def test_005_repeat_step_5_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 5 in Cash out tab
        EXPECTED: Result should be same
        """
        pass

    def test_006_verify_the_display_of__lengthy_score_in_settled_tab(self):
        """
        DESCRIPTION: Verify the display of  lengthy score in settled tab
        EXPECTED: The score should display in second line for consistency
        """
        pass
