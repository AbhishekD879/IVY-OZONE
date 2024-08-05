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
class Test_C2323004_TO_EDITPlace_Each_Way_SP_Bet_on_Race_Selection_and_see_Bet_Receipt(Common):
    """
    TR_ID: C2323004
    NAME: [TO-EDIT]Place Each Way SP Bet on Race Selection and see Bet Receipt
    DESCRIPTION: [TO-EDIT]This case should also include the check on QB + after placing the bet the buttons on betslip 'Resuse selections' & 'Go betting' + EW option
    DESCRIPTION: This test case verifies placing Each Way bet on Race Selection and its Bet Receipt for SP priced selection
    DESCRIPTION: AUTOTEST [C2351909]
    PRECONDITIONS: There is event with 'Win Or Each Way market' with SP prices
    PRECONDITIONS: User is logged in and has positive balance to place a bet,
    PRECONDITIONS: User is placed single bet with 'SP' selection and with selected 'Each Way' checkbox
    PRECONDITIONS: 'Est. Returns' displays "N/A"
    PRECONDITIONS: 'Total Est. Returns' displays "N/A"
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
        EXPECTED: *   Odds displays "SP"
        EXPECTED: *   Unit Stake and 'E/W' label
        EXPECTED: *   Total Stake
        EXPECTED: *   Est. Returns displays "N/A"
        EXPECTED: **All information corresponds to the information about just placed bet**
        EXPECTED: From OX99
        EXPECTED: * Header: "Bet placed successfully" with date and time "05/11/2019, 13:03"
        EXPECTED: * Single @ SP
        EXPECTED: * Bet ID ie i.e. O/0123828/0000155
        EXPECTED: * Selection name
        EXPECTED: * Market name / Event name
        EXPECTED: * Each way terms (eg. "Each Way Odds 1/5 Places 1-2-3")
        EXPECTED: * "2 Lines at STAKE per line
        EXPECTED: Bottom part:
        EXPECTED: * Stake: total stake
        EXPECTED: * Est. returns: N/A
        EXPECTED: 'Reuse Selection' and 'Done' buttons (Only in Betslip)
        """
        pass
