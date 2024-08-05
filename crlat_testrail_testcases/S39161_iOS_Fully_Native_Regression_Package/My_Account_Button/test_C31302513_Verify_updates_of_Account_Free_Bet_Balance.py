import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C31302513_Verify_updates_of_Account_Free_Bet_Balance(Common):
    """
    TR_ID: C31302513
    NAME: Verify updates of Account/Free Bet Balance
    DESCRIPTION: This test case verifies that the Account/free bet balance is automatically updated to reflect the new free bet balance
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. My account button is in Logged In state
    PRECONDITIONS: 3. Amount of Account/free bet balance is available (emulated)
    """
    keep_browser_open = True

    def test_001_emulate_deposit_account_balance_has_been_awarded_to_user(self):
        """
        DESCRIPTION: Emulate deposit (account balance has been awarded to User)
        EXPECTED: Account balance is automatically updated (including the Animation:
        EXPECTED: https://jira.egalacoral.com/secure/attachment/1290957/Native-Lads-Header_v1.mp4)
        """
        pass

    def test_002_emulate_free_bet_has_been_awarded_to_user(self):
        """
        DESCRIPTION: Emulate free bet has been awarded to User
        EXPECTED: Free bet balance is automatically updated (including the Animation
        EXPECTED: https://jira.egalacoral.com/secure/attachment/1290957/Native-Lads-Header_v1.mp4)
        """
        pass
