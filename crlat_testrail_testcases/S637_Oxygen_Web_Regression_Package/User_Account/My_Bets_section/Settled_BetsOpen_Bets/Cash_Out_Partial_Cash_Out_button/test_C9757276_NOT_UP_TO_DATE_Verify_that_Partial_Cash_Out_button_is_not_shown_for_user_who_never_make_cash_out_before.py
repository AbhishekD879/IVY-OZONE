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
class Test_C9757276_NOT_UP_TO_DATE_Verify_that_Partial_Cash_Out_button_is_not_shown_for_user_who_never_make_cash_out_before(Common):
    """
    TR_ID: C9757276
    NAME: [NOT UP TO DATE] Verify that 'Partial Cash Out' button is not shown for user who never make cash out before
    DESCRIPTION: Test Case is not valid, please see comments to https://jira.egalacoral.com/browse/BMA-49009
    DESCRIPTION: This test case verifies that partial cash out is not available for user who never makes Cash Out
    PRECONDITIONS: 1. Login with user who never makes Cash Out (it can be a new User)
    PRECONDITIONS: 2. Place a SINGLE and MULTIPLE bets with cash out available
    PRECONDITIONS: 3. Navigate to By Bets Page
    """
    keep_browser_open = True

    def test_001_open_cash_out_tabverify_that_partial_cash_out_button_is_not_shown_for_placed_bets(self):
        """
        DESCRIPTION: Open Cash Out tab
        DESCRIPTION: Verify that 'Partial Cash Out' button is not shown for placed bets
        EXPECTED: 'Partial Cash Out' button is not shown
        """
        pass

    def test_002_make_s_full_cash_out_for_single_bet_from_preconditionsverify_that_partial_cash_out_button_is_not_shown_for_multiple_bet_from_precondition(self):
        """
        DESCRIPTION: Make s full cash out for SINGLE bet from preconditions
        DESCRIPTION: Verify that 'Partial Cash Out' button is not shown for MULTIPLE bet from precondition
        EXPECTED: 'Partial Cash Out' button is not shown for MULTIPLE bet
        """
        pass
