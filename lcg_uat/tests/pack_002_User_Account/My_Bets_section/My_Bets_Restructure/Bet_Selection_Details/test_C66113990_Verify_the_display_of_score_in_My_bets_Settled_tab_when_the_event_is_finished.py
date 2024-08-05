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
class Test_C66113990_Verify_the_display_of_score_in_My_bets_Settled_tab_when_the_event_is_finished(Common):
    """
    TR_ID: C66113990
    NAME: Verify the display of score in My bets Settled tab when the event is finished
    DESCRIPTION: This testcase verifies the display of score in My bets Settled tab when the event is finished
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

    def test_002_place_bet_by_adding_selections_of_inplay_events_which_shows_dcore_updates_in_my_bets_area(self):
        """
        DESCRIPTION: Place bet by adding selections of inplay events which shows dcore updates in my bets area
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_the_display_of_score_for_inplay_event_in_open_tab_when_one_of_the_events_resulted(self):
        """
        DESCRIPTION: Verify the display of score for inplay event in Open tab when one of the events resulted
        EXPECTED: score should be displayed with a white background and a box around the score
        """
        pass

    def test_005_verify_the_display_of_score_for_inplay_event_in_cashout_tab_when_one_of_the_events_resulted(self):
        """
        DESCRIPTION: Verify the display of score for inplay event in Cashout tab when one of the events resulted
        EXPECTED: score should be displayed with a white background and a box around the score
        """
        pass

    def test_006_repeat_3_6_with_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat 3-6 with Tier1 and Tier2 sports
        EXPECTED: Result should be same
        """
        pass
