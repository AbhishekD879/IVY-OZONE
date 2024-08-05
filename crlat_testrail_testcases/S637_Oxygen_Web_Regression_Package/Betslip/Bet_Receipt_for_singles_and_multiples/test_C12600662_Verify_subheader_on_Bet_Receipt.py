import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C12600662_Verify_subheader_on_Bet_Receipt(Common):
    """
    TR_ID: C12600662
    NAME: Verify subheader on Bet Receipt
    DESCRIPTION: This test case verifies the displaying of subheader on Bet Receipt
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: For <Sport>  it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    """
    keep_browser_open = True

    def test_001_verify_subheader_displaying_on_bet_receipt(self):
        """
        DESCRIPTION: Verify subheader displaying on Bet Receipt
        EXPECTED: * Tick icon and 'Bet Placed Successfully' text is aligned by the left side
        EXPECTED: * Date and time are displayed in the next format: i.e. 19/09/2019, 11:57 and aligned by the right side
        EXPECTED: * Bet count is displayed in the next format: 'Your Bets:(X)'
        EXPECTED: where 'X' is the number of bets placed in for that receipt
        """
        pass
