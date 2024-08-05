import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C146507_Cash_Out_tab_when_there_are_no_bets_available_for_cash_out(Common):
    """
    TR_ID: C146507
    NAME: 'Cash Out' tab when there are no bets available for cash out
    DESCRIPTION: This test case verifies 'Cash Out' tab when the customer has no bets available for cash out.
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has no bets available for cash out.
    PRECONDITIONS: Design:
    PRECONDITIONS: Coral:
    PRECONDITIONS: ![](index.php?/attachments/get/2880615)
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: ![](index.php?/attachments/get/2880616)
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Cash out' tab has opened
        """
        pass

    def test_002_verify_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'Cash Out' tab
        EXPECTED: * Text 'You currently have no cash out bets '(Coral)/ You currently have no bets available for cash out(Ladbrokes) is present
        EXPECTED: * Button 'Start betting'(Coral)/'Go betting'(Ladbrokes) is displayed according to design
        """
        pass

    def test_003_tap_start_bettinggo_betting_button(self):
        """
        DESCRIPTION: Tap 'Start betting'/'Go betting' button
        EXPECTED: User is redirected to the Homepage
        """
        pass
