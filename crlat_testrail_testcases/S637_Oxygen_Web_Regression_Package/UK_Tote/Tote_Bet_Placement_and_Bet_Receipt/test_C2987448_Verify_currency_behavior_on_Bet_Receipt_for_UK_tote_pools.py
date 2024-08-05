import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2987448_Verify_currency_behavior_on_Bet_Receipt_for_UK_tote_pools(Common):
    """
    TR_ID: C2987448
    NAME: Verify currency behavior on Bet Receipt for UK tote pools
    DESCRIPTION: This test case verifies the user currency and pool currency on Bet receipt for UK tote pools for users with different currency than pool currency.
    PRECONDITIONS: 1. User is logged in with different currency than pool one
    PRECONDITIONS: 2. User balance is enough to place a bet
    PRECONDITIONS: 3. User has added one or few UK totes selections to betslip from any pool type available (Win/Place/Execta/Trifecta...)
    PRECONDITIONS: 4. User has placed bet and is on Bet receipt
    """
    keep_browser_open = True

    def test_001_on_bet_receipt_verify_the_unit_a_stake_currency_and_currency_sign_under_the_bet(self):
        """
        DESCRIPTION: On bet receipt verify the Unit a Stake currency and currency sign under the bet
        EXPECTED: * Unit Stake currency is displayed in pool currency and pool Currency Sign:
        EXPECTED: 1 Line at £2.00 per line
        EXPECTED: * Total stake currency is displayed in user currency and user Currency Sign:
        EXPECTED: Stake:€2.94
        """
        pass

    def test_002_verify_total_stake_currency_and_sign_at_the_bottom_of_the_bet_receipt(self):
        """
        DESCRIPTION: Verify Total stake currency and sign at the bottom of the bet receipt
        EXPECTED: Total stake currency is displayed in user currency and user Currency Sign
        EXPECTED: Eg: Total Stake: £ 1.40
        """
        pass
