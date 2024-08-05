import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870255_Validate_Cash_Out_available_on_an_edited_acca(Common):
    """
    TR_ID: C44870255
    NAME: Validate  Cash Out available on an edited acca
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User have accumulator bets on my bets area
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets-open bets tab
        EXPECTED: Cash out option should be available for EMA
        """
        pass

    def test_002_tap_cash_out_buttonverify_that_confirm_cash_out_shown_and_enabledand_edit_my_bet_button_should_be_displayed(self):
        """
        DESCRIPTION: Tap 'Cash Out' button
        DESCRIPTION: Verify that 'Confirm Cash Out' shown and enabled
        DESCRIPTION: and 'EDIT MY BET' button should be displayed
        EXPECTED: 'Confirm Cash Out' button is shown and enabled
        EXPECTED: Confirm Cash Out' button is flashing 3 times
        EXPECTED: 'EDIT MY Bet' button is should display
        """
        pass
