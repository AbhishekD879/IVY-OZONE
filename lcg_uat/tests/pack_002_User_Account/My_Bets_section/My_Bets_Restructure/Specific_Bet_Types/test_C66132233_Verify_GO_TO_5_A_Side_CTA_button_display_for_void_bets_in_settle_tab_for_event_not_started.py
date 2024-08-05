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
class Test_C66132233_Verify_GO_TO_5_A_Side_CTA_button_display_for_void_bets_in_settle_tab_for_event_not_started(Common):
    """
    TR_ID: C66132233
    NAME: Verify  GO TO 5-A-Side CTA  button display for void bets in settle tab for event not started
    DESCRIPTION: This test case verify  GO TO 5-A-Side CTA  button display for void bets in settle tab for event not started
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

    def test_000_(self):
        """
        DESCRIPTION: 
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

    def test_000_check_the_above_bet_in_settle_tab_after_bet_got_void(self):
        """
        DESCRIPTION: Check the above bet in settle tab after bet got void
        EXPECTED: 5-A-Side bet available in settle tab with status as void
        """
        pass

    def test_000_check_go_to_5_a_side_cta__button__for_void_bets_for_event_not_started(self):
        """
        DESCRIPTION: Check GO TO 5-A-Side CTA  button  for void bets for event not started
        EXPECTED: In settle tab  GO TO 5-A-Side CTA  button  is  displayed for void bets if the event is not started
        """
        pass
