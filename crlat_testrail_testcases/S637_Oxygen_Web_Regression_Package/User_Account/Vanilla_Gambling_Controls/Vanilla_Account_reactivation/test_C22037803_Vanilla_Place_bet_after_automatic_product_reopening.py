import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C22037803_Vanilla_Place_bet_after_automatic_product_reopening(Common):
    """
    TR_ID: C22037803
    NAME: [Vanilla] Place bet after automatic product reopening
    DESCRIPTION: 
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Log in on user account that had Sports product closed, but the closure time ended automatically
    PRECONDITIONS: 3. User has enough balance to place a bet
    """
    keep_browser_open = True

    def test_001_make_a_selection(self):
        """
        DESCRIPTION: Make a selection
        EXPECTED: -
        """
        pass

    def test_002_enter_stake_within_the_available_balance(self):
        """
        DESCRIPTION: Enter stake (within the available balance)
        EXPECTED: -
        """
        pass

    def test_003_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: Bet is successfully placed.
        """
        pass
