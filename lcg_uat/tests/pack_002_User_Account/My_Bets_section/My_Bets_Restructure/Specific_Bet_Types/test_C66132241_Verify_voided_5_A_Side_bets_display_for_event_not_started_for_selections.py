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
class Test_C66132241_Verify_voided_5_A_Side_bets_display_for_event_not_started_for_selections(Common):
    """
    TR_ID: C66132241
    NAME: Verify voided 5-A-Side bets display for event not started for selections
    DESCRIPTION: This test case verify voided 5-A-Side bets display for event not started for selections
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

    def test_000_check_the_selection_got_void_from_5_a_side_bet(self):
        """
        DESCRIPTION: Check the selection got void from 5-A-Side bet
        EXPECTED: Display  'grey dot' for pre match for void bets
        """
        pass

    def test_000_go_to_settle_tab_and_check_the_void_bets(self):
        """
        DESCRIPTION: Go to settle tab and check the void bets
        EXPECTED: 5-A-Side void bets should be available
        """
        pass

    def test_000_check_the_void_bets_in_settle_tab(self):
        """
        DESCRIPTION: Check the void bets in settle tab
        EXPECTED: Void status should display on header
        """
        pass
