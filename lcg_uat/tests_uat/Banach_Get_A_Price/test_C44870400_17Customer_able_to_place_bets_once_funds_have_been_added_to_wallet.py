import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870400_17Customer_able_to_place_bets_once_funds_have_been_added_to_wallet(Common):
    """
    TR_ID: C44870400
    NAME: 17.Customer able to place bets once funds have been added to wallet
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_a_new_user_add_a_card_but_dont_add_money(self):
        """
        DESCRIPTION: Make a new user, add a card, but don't add money
        EXPECTED: You should have made a new user, but not made a deposit
        """
        pass

    def test_002_add_a_selection_from_a_banache_market_and_add_a_stake(self):
        """
        DESCRIPTION: Add a selection from a Banache market and add a stake.
        EXPECTED: You should have made a selection from a Banache market and added a stake
        """
        pass

    def test_003_verify_that_the_make_a_quick_deposit_button_appears_on_the_bet_slip_and_you_see_the_funds_needed_for_bet_x_message(self):
        """
        DESCRIPTION: Verify that the Make a Quick Deposit button appears on the bet slip and you see the 'Funds needed for bet: X' message
        EXPECTED: The Make a Quick Deposit button and an error message should have appeared on the bet slip
        """
        pass

    def test_004_in_quick_deposit_add_your_cvv_number_and_click_deposit_and_place_bet(self):
        """
        DESCRIPTION: In Quick Deposit add your CVV number and click Deposit and place bet
        EXPECTED: Your bet should have been placed
        """
        pass
