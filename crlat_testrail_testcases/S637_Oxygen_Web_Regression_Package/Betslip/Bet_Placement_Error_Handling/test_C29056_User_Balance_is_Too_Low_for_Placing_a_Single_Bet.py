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
class Test_C29056_User_Balance_is_Too_Low_for_Placing_a_Single_Bet(Common):
    """
    TR_ID: C29056
    NAME: User Balance is Too Low for Placing a Single Bet
    DESCRIPTION: This test case verifies bet slip error handling in case when user balance is too low.
    DESCRIPTION: Autotest Mobile: [C16074331]
    DESCRIPTION: Autotest Desktop: [C16268913]
    PRECONDITIONS: 1.  Application is loaded
    PRECONDITIONS: 2.  User is logged in
    PRECONDITIONS: 3.  The user account is NOT sufficient to cover any stake
    PRECONDITIONS: 4.  User doesn't have added debit/credit cards
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> sport it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event landing page
    PRECONDITIONS: NOTE: in order to check Max Allowed Bet enter extremely large stake value in 'Stake' field and tap 'Bet Now' button to see what is Max allowed bet for selection.
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_002_enter_a_stake_which_will_exceed_users_balance_but_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Enter a stake which will exceed user's balance but won't exceed a max bet allowed
        EXPECTED: 'Bet Now' (from OX 99 'Place Bet') button is enabled
        """
        pass

    def test_003_tap_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: User is navigated to 'Deposit' page
        EXPECTED: * User is navigated to 'Add Credit Card' tab for **Coral** brand
        EXPECTED: * User is navigated to 'Account One' system for **Ladbrokes** brand
        EXPECTED: * Betslip is closed
        """
        pass
