import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870215_Customer_Bet_placements_fails_on_an_in_play_event_where_betting_is_not_allowed_once_event_starts_and_event_suspended_error_message_displays(Common):
    """
    TR_ID: C44870215
    NAME: Customer Bet placements fails on an in play event where betting is not allowed once event starts and event suspended error message displays
    DESCRIPTION: This test case verify suspended error message on Quick bet / Betslip
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_go_to_in_play_on_sport_ribbon(self):
        """
        DESCRIPTION: Go to In-Play on sport ribbon
        EXPECTED: In-Play landing page opened
        """
        pass

    def test_003_make_a_selection_from_any_inplay_sport_and_add_to_betslip(self):
        """
        DESCRIPTION: Make a selection from any inplay sport and add to betslip
        EXPECTED: Selection added to betslip
        """
        pass

    def test_004_enter_the_stake_to_place_a_bet(self):
        """
        DESCRIPTION: Enter the stake to place a bet
        EXPECTED: Stake entered
        """
        pass

    def test_005_verify_that_selection_suspended_in_betslip(self):
        """
        DESCRIPTION: Verify that selection suspended in betslip
        EXPECTED: Some of the selections are suspended message display on top of betslip
        EXPECTED: Selections are greyed out
        EXPECTED: Place bet button is grey out
        """
        pass
