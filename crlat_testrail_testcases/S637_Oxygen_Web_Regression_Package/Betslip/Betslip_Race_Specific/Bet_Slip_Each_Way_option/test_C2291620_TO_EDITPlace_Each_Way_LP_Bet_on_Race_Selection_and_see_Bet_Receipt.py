import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C2291620_TO_EDITPlace_Each_Way_LP_Bet_on_Race_Selection_and_see_Bet_Receipt(Common):
    """
    TR_ID: C2291620
    NAME: [TO-EDIT]Place Each Way LP Bet on Race Selection and see Bet Receipt
    DESCRIPTION: [TO-EDIT]This case should also include the check on QB + after placing the bet the buttons on betslip 'Resuse selections' & 'Go betting' + EW option
    DESCRIPTION: This test case verifies placing Each Way bet on Race Selection and its Bet Receipt for LP priced selection
    DESCRIPTION: AUTOTEST [C2323020]
    PRECONDITIONS: There is event with 'Win Or Each Way market' with LP prices
    PRECONDITIONS: User is logged in and has positive balance to place a bet
    PRECONDITIONS: User is placed single bet with 'LP' selection and with selected 'Each Way' checkbox
    """
    keep_browser_open = True

    def test_001_click_bet_now_button(self):
        """
        DESCRIPTION: Click 'Bet Now' button
        EXPECTED: 1. Bet is placed
        EXPECTED: 2. Balance is decreased by 'Total Stake' value
        EXPECTED: 3. Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_002_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: Bet Receipt header is present
        EXPECTED: Bet Receipt contains the following information:
        EXPECTED: *   header 'Singles(1)'
        EXPECTED: *   selection name
        EXPECTED: *   the market type user has bet on - i.e. Win or Each Way
        EXPECTED: *   the event name to which the outcome belongs to
        EXPECTED: *   the Bet ID. The Bet ID is start with O and contain numeric values - i.e. O/0123828/0000155
        EXPECTED: *   Odds
        EXPECTED: *   Unit Stake and 'E/W' label
        EXPECTED: *   Total Stake
        EXPECTED: *   Est. Returns
        EXPECTED: **All information corresponds to the information about just placed bet**
        EXPECTED: 'Reuse Selection' and 'Done' buttons
        """
        pass
