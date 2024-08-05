import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C9608212_Verify_that_EDIT_MY_ACCA_button_is_not_shown_when_cash_out_is_unavailable_for_the_bet(Common):
    """
    TR_ID: C9608212
    NAME: Verify that 'EDIT MY ACCA' button is not shown when cash out is unavailable for the bet
    DESCRIPTION: This test case verifies that 'EDIT MY ACCA' button is not shown when cash out is unavailable for the bet
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a MULTIPLE bet where one of the events in the bet with CASH OUT unavailable (- In AccountHistory?DetailLevel... response: cashoutValue: "CASHOUT_SELN_NO_CASH)
    PRECONDITIONS: **Coral** has 'EDIT MY BET' button
    PRECONDITIONS: **Ladbrokes** has 'EDIT MY ACCA' button
    """
    keep_browser_open = True

    def test_001_navigate_to_my_betsopen_betsverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_bet(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is not shown for the bet
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is not shown
        """
        pass

    def test_002_navigate_to_my_betssettled_betsverify_that_edit_my_betedit_my_acca_button_is_not_shown_for_the_bet(self):
        """
        DESCRIPTION: Navigate to My Bets>Settled Bets
        DESCRIPTION: Verify that 'EDIT MY BET/EDIT MY ACCA' button is not shown for the bet
        EXPECTED: - 'EDIT MY BET/EDIT MY ACCA' button is not shown
        """
        pass
