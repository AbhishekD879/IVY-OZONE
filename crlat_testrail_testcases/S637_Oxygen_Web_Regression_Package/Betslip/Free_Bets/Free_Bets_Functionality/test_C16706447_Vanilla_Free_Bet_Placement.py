import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C16706447_Vanilla_Free_Bet_Placement(Common):
    """
    TR_ID: C16706447
    NAME: [Vanilla] Free Bet Placement
    DESCRIPTION: This test case verifies Free Bet Placement for Single and Multiple Selections
    PRECONDITIONS: User should have multiple Free Bets available on their account
    PRECONDITIONS: NOTE: Contact Coral UAT for assistance with applying free bet tokens to the relevant test accounts
    """
    keep_browser_open = True

    def test_001_log_in_to_applicaiton(self):
        """
        DESCRIPTION: Log in to applicaiton
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: Betslip is open
        """
        pass

    def test_003_for_a_single_selection_press_on_use_free_bet_link_and_select_one_of_available_free_bets(self):
        """
        DESCRIPTION: For a single selection: Press on 'Use Free Bet' link and select one of available Free Bets
        EXPECTED: * Stake field is NOT pre-populated by value of a free bet selected
        EXPECTED: * 'Est. Returns' is calculated
        """
        pass

    def test_004_tap_place_bet(self):
        """
        DESCRIPTION: Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is NOT changed
        """
        pass

    def test_005_1_add_selection_to_the_betslip_and_open_betslip2_enter_value_in_a_stake_field3_add_a_free_bet_for_a_single_selection(self):
        """
        DESCRIPTION: 1. Add selection to the Betslip and open Betslip
        DESCRIPTION: 2. Enter value in a 'Stake' field
        DESCRIPTION: 3. Add a Free Bet for a single selection
        EXPECTED: 1. Selection is visible in Betslip
        EXPECTED: 2. Stake entered is shown is "Stake" field
        EXPECTED: 3. Free Bet is included in bet and 'Est. Returns' is calculated based on stake and free bet
        """
        pass

    def test_006_tap_place_bet(self):
        """
        DESCRIPTION: Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is decreased on a value entered in a 'Stake' field
        """
        pass

    def test_007_for_a_multiple_selection_press_on_use_free_bet_link_and_select_one_of_available_free_bets(self):
        """
        DESCRIPTION: For a Multiple selection: Press on 'Use Free Bet' link and select one of available Free Bets
        EXPECTED: * Free Bet is selected successfully
        EXPECTED: * Stake field is NOT pre-populated by value of a free bet selected
        EXPECTED: * 'Est. Returns' is calculated based on stake and free bet
        """
        pass

    def test_008_tap_place_bet(self):
        """
        DESCRIPTION: Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is NOT changed
        """
        pass

    def test_009_go_back_to_betslipenter_value_in_a_stake_field_and_add_a_free_bet_for_a_multiple_selection(self):
        """
        DESCRIPTION: Go back to Betslip
        DESCRIPTION: Enter value in a 'Stake' field and add a Free Bet for a Multiple selection
        EXPECTED: * Free Bet is selected
        EXPECTED: * Stake entered is shown is "Stake" field
        EXPECTED: * 'Est. Returns' is calculated based on stake and free bet
        """
        pass

    def test_010_tap_place_bet(self):
        """
        DESCRIPTION: Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is decreased on a value entered in a 'Stake' field
        """
        pass
