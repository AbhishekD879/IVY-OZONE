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
class Test_C62764549_Verify_whether_user_is_able_to_see_information_messagerelated_to_Antepost_Bets_under_the_Cashout_tab(Common):
    """
    TR_ID: C62764549
    NAME: Verify whether user is able to see information message(related to Antepost Bets) under the Cashout tab
    DESCRIPTION: This testcase verifies whether user is able to see an information message under cashout tab
    PRECONDITIONS: 1. Login to the application
    """
    keep_browser_open = True

    def test_001_go_to_my_bets__cashout_tab_and_check_for_the_information_message(self):
        """
        DESCRIPTION: Go to My Bets- Cashout tab and check for the information message
        EXPECTED: The Information message "If you require account or gambling history over longer periods, or details of unsettled bets placed over 1 year ago, please contact us." should be displayed under the Cashout tab.
        EXPECTED: Note: When user clicks on the Contact Us link- it should redirect to the appropriate help center page.
        """
        pass
