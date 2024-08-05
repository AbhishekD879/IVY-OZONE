import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C2507463_Partial_cash_out_of_Banach_bet(Common):
    """
    TR_ID: C2507463
    NAME: Partial cash out of Banach bet
    DESCRIPTION: Test case verifies Partial cash out of Banach bet
    DESCRIPTION: AUTOTEST Mobile: [C2605354] (adapted for hl and prod)
    DESCRIPTION: AUTOTEST Desktop: [C2605355]
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Cash-out tab
    PRECONDITIONS: in Dev tools > Network find **getBetDetails** request > identify bet by betID
    PRECONDITIONS: **User has placed Banach bet(s)**
    PRECONDITIONS: **Banach bet is displayed on Cash out tab**
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets___cash_out_page(self):
        """
        DESCRIPTION: Navigate to My Bets -> Cash out page
        EXPECTED: - Cash Out Button contains Partial cash-out option if getBetDetails has parameter partialCashoutAvailable: "Y"
        EXPECTED: - The amount eligible for cash out displayed on the button is taken from cashoutValue parameter of getBetDetails request
        EXPECTED: **From release XXX.XX:**
        EXPECTED: - Cash Out Button contains Partial cash-out option if in WebSocket connection to Cashout MS initial bets data has parameter partialCashoutAvailable: "Y"
        """
        pass

    def test_002_tap_partial_cash_out(self):
        """
        DESCRIPTION: Tap partial cash out
        EXPECTED: The slider is opened with default value in the middle
        """
        pass

    def test_003_tap_on_cash_out(self):
        """
        DESCRIPTION: Tap on Cash out
        EXPECTED: Confirm Cash out button is shown with correct value
        EXPECTED: (cashoutValue parameter of getBetDetails request divided by 2)
        EXPECTED: **From release XXX.XX:**
        EXPECTED: Confirm Cash out button is shown with correct value
        EXPECTED: (cashoutValue parameter of initial bets response in WS connection is divided by 2)
        """
        pass

    def test_004_approve_cashout(self):
        """
        DESCRIPTION: Approve cashout
        EXPECTED: - Successful cash out notification 'Partial cashout Successful' is displayed below the cashout button
        EXPECTED: - User balance is increased accordingly by cashed out amount
        EXPECTED: -  Bet still displayed on Cash Out page
        EXPECTED: -  The amount of cash out displayed on the button decreased accordingly by cashed out amount
        """
        pass
