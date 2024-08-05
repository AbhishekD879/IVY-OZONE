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
class Test_C874312_Place_Tennis_bet_using_Freebet_Token(Common):
    """
    TR_ID: C874312
    NAME: Place Tennis bet using Freebet Token
    DESCRIPTION: Bet Placement - Verify that the customer can place a bet on Tennis using a Freebet Token (with a customer that has 0 funds)
    DESCRIPTION: Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: A customer with zero balance (£ 0) but has freebets  available.
    """
    keep_browser_open = True

    def test_001_login_to_oxygen_app_with_a_customer_with_zero_balance_and_at_least_one_freebet(self):
        """
        DESCRIPTION: Login to Oxygen app with a customer with Zero balance and at least one freebet.
        EXPECTED: The customer is logged in
        """
        pass

    def test_002_add_a_tennis_selectionselections_to_bet_slip(self):
        """
        DESCRIPTION: Add a Tennis selection/selections to bet slip
        EXPECTED: The selection/selections is added to bet slip
        """
        pass

    def test_003_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: The betslip is loaded
        """
        pass

    def test_004_select_a_freebet_from_the_freebets_drop_downcustomer_needs_to_have_a_zero_balance(self):
        """
        DESCRIPTION: Select a freebet from the freebets drop-down
        DESCRIPTION: (Customer needs to have a zero balance)
        EXPECTED: The freebet is selected
        """
        pass

    def test_005_click_on_place_bet_button(self):
        """
        DESCRIPTION: Click on 'Place Bet' button
        EXPECTED: The bet is successfully placed and bet receipt is displayed.
        """
        pass

    def test_006_verify_the_bet_receipt(self):
        """
        DESCRIPTION: Verify the Bet receipt
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Event is displayed;
        EXPECTED: * 'Cashout' label between the bet and Bet ID (if cashout is available for this event)
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        pass

    def test_007_click_on_my_bets(self):
        """
        DESCRIPTION: Click on My Bets
        EXPECTED: My Bets page is opened
        """
        pass

    def test_008_go_to_the_bet_that_was_just_placed_and_verify_bet_details(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify bet details.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: **Correct Stake is correctly displayed;
        """
        pass

    def test_009_click_on_user_menu___logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        pass
