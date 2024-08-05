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
class Test_C2507465_To_edit_Full_cash_out_of_Banach_bet(Common):
    """
    TR_ID: C2507465
    NAME: [To edit] Full cash out of Banach bet
    DESCRIPTION: Test case needs to be edited according to new Cash out functionality
    DESCRIPTION: Test case verifies full Cash out of Banach bet
    DESCRIPTION: AUTOTEST: [C2605323]
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Cash-out tab
    PRECONDITIONS: in Dev tools > Network find **getBetDetails** request > identify bet by betID
    PRECONDITIONS: **User has placed Banach bet(s)**
    PRECONDITIONS: **Banach bet is displayed on Cash out tab**
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cash_out_and_verify_cash_out_button_value(self):
        """
        DESCRIPTION: Navigate to My Bets > Cash-out and verify Cash out button value
        EXPECTED: The amount eligible for cash out displayed on the button is taken from cashoutValue parameter of getBetDetails request
        """
        pass

    def test_002_tap_on_cash_out_button(self):
        """
        DESCRIPTION: Tap on CASH OUT button
        EXPECTED: **Confirm cash out %** button is shown,
        EXPECTED: where % is cashoutValue parameter of getBetDetails request
        """
        pass

    def test_003_confirm_cash_out(self):
        """
        DESCRIPTION: Confirm cash out
        EXPECTED: - 'Cashed out' label is displayed in the header on the right
        EXPECTED: - 'You cashed out <currency> <value>' notification is shown below the header
        EXPECTED: - Successful cash out notification is displayed instead of the cashout button
        EXPECTED: - User balance is updated
        EXPECTED: - Bet disappears from Cash Out page after page reload
        """
        pass
