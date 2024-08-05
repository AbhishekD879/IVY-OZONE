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
class Test_C66113993_Verify_micro_animation_and_color_change_when_there_is_a_score_change_for_inplay_events_in_My_BetsOpenCash_outSettled(Common):
    """
    TR_ID: C66113993
    NAME: Verify micro animation and color change when there is a score change for inplay events in My Bets(Open,Cash out,Settled)
    DESCRIPTION: This testcase verifies micro animation and color change when there is a score change for inplay events in My Bets(Open,Cash out,Settled)
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

    def test_002_place_bet_by_adding_selections_of_inplay_events_which_shows_score_updates_in_my_bets_areaex_tennis(self):
        """
        DESCRIPTION: Place bet by adding selections of inplay events which shows score updates in my bets area(Ex: Tennis)
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_the_score_updates_in_open_tab(self):
        """
        DESCRIPTION: Verify the score updates in Open tab
        EXPECTED: When score updates the change whould highlighted in yellow color and micro animation should be as per figma provided
        """
        pass

    def test_005_repeat_step_5_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 5 in Cash out tab
        EXPECTED: Result should be same
        """
        pass

    def test_006_repeat_step_5_in_settled_tab(self):
        """
        DESCRIPTION: Repeat step 5 in Settled tab
        EXPECTED: result should be same
        """
        pass
