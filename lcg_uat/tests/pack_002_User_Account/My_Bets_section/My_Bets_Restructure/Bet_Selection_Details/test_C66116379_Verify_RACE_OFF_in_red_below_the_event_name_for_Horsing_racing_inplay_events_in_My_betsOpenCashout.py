import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66116379_Verify_RACE_OFF_in_red_below_the_event_name_for_Horsing_racing_inplay_events_in_My_betsOpenCashout(Common):
    """
    TR_ID: C66116379
    NAME: Verify  RACE OFF in red below the event name for Horsing racing inplay events in My bets(Open,Cashout)
    DESCRIPTION: This testcase verifies  RACE OFF in red below the event name for Horsing racing inplay events in My bets(Open,Cashout)
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

    def test_002_add_horse_racing_selections_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add horse racing selections to betslip and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_the_bet_palced_in_step_3_in_open_tab(self):
        """
        DESCRIPTION: Verify the bet palced in step 3 in open tab
        EXPECTED: Bet should be dispayed in open tab
        """
        pass

    def test_005_verify_the_bet_selection_area_once_the_race_starts(self):
        """
        DESCRIPTION: Verify the bet selection area once the race starts
        EXPECTED: RACE OFF in red below the event name for Horsing racing inplay events in Open tab
        """
        pass

    def test_006_repeat_5_and_6_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat 5 and 6 in cash out tab
        EXPECTED: Result should be same
        """
        pass
