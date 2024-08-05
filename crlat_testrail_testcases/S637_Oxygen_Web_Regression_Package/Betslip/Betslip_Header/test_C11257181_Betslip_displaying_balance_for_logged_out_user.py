import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C11257181_Betslip_displaying_balance_for_logged_out_user(Common):
    """
    TR_ID: C11257181
    NAME: Betslip: displaying balance for logged out user
    DESCRIPTION: This test case verifies that balance is not displayed for logged out user
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have some selections added to betslip and betslip should be opened
    """
    keep_browser_open = True

    def test_001_verify_displaying_account_balance_in_the_betslip_header(self):
        """
        DESCRIPTION: Verify displaying account balance in the betslip header
        EXPECTED: Balance is displayed at the top right corner
        """
        pass

    def test_002___log_out_and_open_betslip__verify_displaying_account_balance_in_the_betslip_header(self):
        """
        DESCRIPTION: - Log out and open betslip
        DESCRIPTION: - Verify displaying account balance in the betslip header
        EXPECTED: Balance is NOT displayed at the top right corner
        """
        pass
