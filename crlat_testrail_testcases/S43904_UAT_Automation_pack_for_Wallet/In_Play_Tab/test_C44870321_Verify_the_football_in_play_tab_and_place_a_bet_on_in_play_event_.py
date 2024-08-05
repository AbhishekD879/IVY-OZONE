import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870321_Verify_the_football_in_play_tab_and_place_a_bet_on_in_play_event_(Common):
    """
    TR_ID: C44870321
    NAME: "Verify the football in-play tab and place a bet on in-play event "
    DESCRIPTION: this test case verify football inplay tab and bet placement
    PRECONDITIONS: Sport should be available in inplay
    PRECONDITIONS: UserName : goldebuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: In-Play tab opened with all inplay sports
        """
        pass

    def test_003_go_to_football_and_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go to Football and Add selections to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_004_go_to_the_betslip_singles_section(self):
        """
        DESCRIPTION: Go to the Betslip->'Singles' section
        EXPECTED: Betslip is opened
        EXPECTED: Added single selections are present
        """
        pass

    def test_005_enter__stake_for_selection(self):
        """
        DESCRIPTION: Enter  stake for selection
        EXPECTED: Stake is entered and displayed correctly
        EXPECTED: 'Place Bet' button becomes enabled
        """
        pass

    def test_006_tap_on_place_bet_button_and_trigger_error_occurrence_eg_suspension_price_change(self):
        """
        DESCRIPTION: Tap on place bet button and trigger error occurrence (e.g. suspension, price change)
        EXPECTED: After user will deal with error then** 'Place Bet' button** will be enabled within Betslip
        """
        pass

    def test_007_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_008_repeat_steps_3_to_7_for_multiple_bets(self):
        """
        DESCRIPTION: repeat steps #3 to #7 for multiple bets
        EXPECTED: 
        """
        pass
