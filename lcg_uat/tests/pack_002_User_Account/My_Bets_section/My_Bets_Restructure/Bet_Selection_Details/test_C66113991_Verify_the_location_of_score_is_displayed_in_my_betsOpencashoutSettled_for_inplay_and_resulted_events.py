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
class Test_C66113991_Verify_the_location_of_score_is_displayed_in_my_betsOpencashoutSettled_for_inplay_and_resulted_events(Common):
    """
    TR_ID: C66113991
    NAME: Verify the location of score is displayed in my bets(Open,cashout,Settled) for inplay and resulted events
    DESCRIPTION: This testcase the location of score is displayed in my bets for inplay and resulted events
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

    def test_004_verify_the_display_of_score_for_inplay_event_in_open_tab_when_the_match_is_in_live(self):
        """
        DESCRIPTION: Verify the display of score for inplay event in Open tab when the match is in live
        EXPECTED: The score should be displayed with a grey background
        """
        pass

    def test_005_verify_the_location_of_score_is_displayed_at_selection_level(self):
        """
        DESCRIPTION: Verify the location of score is displayed at selection level
        EXPECTED: Score should be displayed in between team names and it should be as per figma
        """
        pass

    def test_006_verify_the_location_of_score_is_displayed_at_selection_level_for_resulted_events(self):
        """
        DESCRIPTION: Verify the location of score is displayed at selection level for resulted events
        EXPECTED: Score should be displayed in between team names and it should be as per figma
        """
        pass
