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
class Test_C9243966_Verify_adding_new_selection_to_the_BetSlip_which_contains_undisplayed_selection(Common):
    """
    TR_ID: C9243966
    NAME: Verify adding new selection to the BetSlip which contains undisplayed selection
    DESCRIPTION: This test case verifies adding new selection to the BetSlip which contains undisplayed selection.
    DESCRIPTION: AUTOTEST [C9690036]
    PRECONDITIONS: * User is Logged in
    PRECONDITIONS: * User has positive balance to place a bet
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: Selection is added
        """
        pass

    def test_002_undisplay_current_selection_in_ti(self):
        """
        DESCRIPTION: Undisplay current selection in TI
        EXPECTED: Current selection still remains in the BetSlip
        """
        pass

    def test_003_add_new_selection_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add new selection to the BetSlip and open it
        EXPECTED: * New selection is added to the BetSlip
        EXPECTED: * Old (undisplayed) selection remains shown in the BetSlip
        """
        pass

    def test_004_place_a_bet_on_both_selections(self):
        """
        DESCRIPTION: Place a bet on both selections
        EXPECTED: Both bets are placed successfully
        """
        pass
