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
class Test_C9608213_Verify_that_CASH_OUT_button_is_NOT_shown_when_cash_out_is_unavailable_for_the_bet(Common):
    """
    TR_ID: C9608213
    NAME: Verify that 'CASH OUT'  button is NOT shown when cash out is unavailable for the bet
    DESCRIPTION: This test case verifies that 'CASH OUT' button is NOT shown when cash out is unavailable for the bet
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a SINGLE and MULTIPLE bets where one of the events in the bet with CASH OUT unavailable (In AccountHistory?DetailLevel... response: cashoutValue: "CASHOUT_SELN_NO_CASHOUT")
    """
    keep_browser_open = True

    def test_001_navigate_to_my_betsopen_betsverify_that_cash_out_button_is_not_shown_for_the_bets_from_preconditions(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets
        DESCRIPTION: Verify that 'CASH OUT' button is NOT shown for the bets from preconditions
        EXPECTED: 'CASH OUT' button is NOT shown
        """
        pass

    def test_002_coral_onlynavigate_to_my_betscash_outverify_that_cash_out_button_is_not_shown_for_the_bets_from_preconditions(self):
        """
        DESCRIPTION: (Coral only)
        DESCRIPTION: Navigate to My Bets>Cash Out
        DESCRIPTION: Verify that 'CASH OUT' button is NOT shown for the bets from preconditions
        EXPECTED: 'CASH OUT' button is NOT shown
        """
        pass
