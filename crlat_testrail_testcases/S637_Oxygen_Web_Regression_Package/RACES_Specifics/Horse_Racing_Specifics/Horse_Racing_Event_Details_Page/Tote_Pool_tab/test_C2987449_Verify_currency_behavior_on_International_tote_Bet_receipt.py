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
class Test_C2987449_Verify_currency_behavior_on_International_tote_Bet_receipt(Common):
    """
    TR_ID: C2987449
    NAME: Verify currency behavior on International tote Bet receipt
    DESCRIPTION: This test case verifies user and pool currency display on International totes Bet Receipt
    PRECONDITIONS: 1. User is logged in with different currency than pool one
    PRECONDITIONS: 2. User balance is enough to place a bet
    PRECONDITIONS: 3. User has added one or few Int totes selections to betslip from any pool type available (Win/Place/Execta/Trifecta...)
    PRECONDITIONS: 4. User has placed bet and is on Bet receipt
    """
    keep_browser_open = True

    def test_001_on_bet_receipt_verify_the_unit_an_total_stake_currency_and_currency_sign_under_the_bet(self):
        """
        DESCRIPTION: On bet receipt verify the Unit an Total stake currency and currency sign under the bet
        EXPECTED: * Unit Stake currency is displayed in pool currency and pool Currency Sign
        EXPECTED: * Total stake currency is displayed in user currency and user Currency Sign
        """
        pass

    def test_002_verify_total_stake_currency_and_sign_at_the_bottom_of_the_bet_receipt(self):
        """
        DESCRIPTION: Verify Total stake currency and sign at the bottom of the bet receipt
        EXPECTED: Total stake currency is displayed in user currency and user Currency Sign
        """
        pass
