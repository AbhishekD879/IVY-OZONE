import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C51315_Bet_Placement_when_Stake_value_is_Lower_than_MinStake(Common):
    """
    TR_ID: C51315
    NAME: Bet Placement when Stake value is Lower than MinStake
    DESCRIPTION: This test case is for checking error message displaying when stake value is lower that minStake value received from server
    DESCRIPTION: AUTOTEST: [C871638]
    PRECONDITIONS: Make sure user has sufficient funds to place a bet
    PRECONDITIONS: In order to modify min stake value use steps:
    PRECONDITIONS: 1. Open OpenBet TI system (use corresponding environment: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems)
    PRECONDITIONS: 2. Go to selection hierarchy level
    PRECONDITIONS: 3. Change the value in the field: 'Min Bet'
    PRECONDITIONS: 4. Check the 'Fixed Stake Limit' checkbox and tap 'Save'
    PRECONDITIONS: Note, now it is unknown how to change min bet for forecast / tricats bets
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: App is loaded
        """
        pass

    def test_002_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_003_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is open
        EXPECTED: Added selection is displayed
        """
        pass

    def test_004_in_a_stake_field_enter_a_stake_value_which_is_lower_than_minstake_allowedtap_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: In a stake field enter a stake value which is lower than minStake allowed
        DESCRIPTION: Tap 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: [Not actual from OX 99]
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Error message 'Sorry, the minimum stake for this bet is <currency symbol><amount>' is shown under this selection
        EXPECTED: [From OX 99]
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Minimum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: * Place Bet button is inactive
        """
        pass

    def test_005_add_few_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add few selections to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_006_enter_valid_stakes_for_several_selectionsin_one_selection_enter_stake_lower_than_min_allowed___tap_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Enter valid stakes for several selections
        DESCRIPTION: In one selection enter stake lower than min allowed -> tap 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: [Not actual from OX 99]
        EXPECTED: * Bets are NOT placed
        EXPECTED: * Error message 'Sorry, the minimum stake for this bet is <currency symbol><amount>' is shown under this selection
        EXPECTED: [From OX 99]
        EXPECTED: * Bets are NOT placed
        EXPECTED: * 'Minimum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: * Place Bet button is inactive
        """
        pass

    def test_007_enter_correct_stakes_which_are_equivalent_to_min_bet_and_tap_on_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Enter correct stakes which are equivalent to min bet and tap on 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: Bet is placed
        EXPECTED: User balance is decreased by value entered in stake field
        """
        pass
