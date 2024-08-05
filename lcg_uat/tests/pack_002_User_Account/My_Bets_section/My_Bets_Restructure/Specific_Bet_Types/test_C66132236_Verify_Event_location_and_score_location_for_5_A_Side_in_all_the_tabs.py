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
class Test_C66132236_Verify_Event_location_and_score_location_for_5_A_Side_in_all_the_tabs(Common):
    """
    TR_ID: C66132236
    NAME: Verify Event location and score location for 5-A-Side in  all the tabs
    DESCRIPTION: This test case verify Event location and score location for 5-A-Side in  all the tabs
    PRECONDITIONS: 5-A-Side event should be available
    PRECONDITIONS: Bets should be available in  open/cashout(if available),settle  tabs for 5-A-Side bets
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokes(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_000_navigate_to_football_page_and_check_for_5_a_side_event(self):
        """
        DESCRIPTION: Navigate to football page and check for 5-A-Side event
        EXPECTED: 5-A-Side event should be available
        """
        pass

    def test_000_check__the_event_which_has_5_a_side_available_and_click_on_the_tab(self):
        """
        DESCRIPTION: Check  the event which has 5-A-Side available and click on the tab
        EXPECTED: 5-A-Side tab should be opened in EDP page
        """
        pass

    def test_000_select_at_least_2_valid_players_on_pitch_view(self):
        """
        DESCRIPTION: Select at least 2 valid players on Pitch view
        EXPECTED: Players are selected on Pitch view
        """
        pass

    def test_000_note_place_multiple_5__a_side_bets(self):
        """
        DESCRIPTION: Note: Place multiple 5 -A-Side bets
        EXPECTED: 'Place Bet' button becomes active
        """
        pass

    def test_000_clicktap_place_bet_button(self):
        """
        DESCRIPTION: Click/Tap 'Place Bet' button
        EXPECTED: Bet should be place on 5-A-Side
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Bet receipt will be displayed
        """
        pass

    def test_000_navigate_to_my_bets_gtopen(self):
        """
        DESCRIPTION: Navigate to My Bets-&gt;Open
        EXPECTED: 5-A-Side event should be available
        """
        pass

    def test_000_check_5_a_side_bet_available_in_open_tab(self):
        """
        DESCRIPTION: Check 5-A-Side bet available in open tab
        EXPECTED: 5-A-Side bet available in open tab
        """
        pass

    def test_000_check_the_event_location_for_5_a_side_bet(self):
        """
        DESCRIPTION: Check the event location for 5-A-Side bet
        EXPECTED: Event name should be  show above the  legs  below the header
        """
        pass

    def test_000_check_the_score__location_for_5_a_side_bet__after_the_event_goes_live(self):
        """
        DESCRIPTION: Check the score  location for 5-A-Side bet  after the event goes live
        EXPECTED: Scores should be  show between the selection  for the event name
        """
        pass

    def test_000_check_the_5_a_side_bets_after_its_got_settle_in_settle_tab(self):
        """
        DESCRIPTION: Check the 5-A-Side bets after its got settle in settle tab
        EXPECTED: 5-A-Side settle bets should be displayed
        """
        pass

    def test_000_check_the_event_name_and_scores_position__for_5_a_side_bet__in_settle_bets(self):
        """
        DESCRIPTION: Check the event name and scores position  for 5-A-Side bet  in settle bets
        EXPECTED: Event name should be  show above the  legs  below the header
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Scores should be shown between the selections in settle bets
        """
        pass

    def test_000_repeat_above_steps_in_settle_tab(self):
        """
        DESCRIPTION: Repeat above steps in settle tab
        EXPECTED: 
        """
        pass
