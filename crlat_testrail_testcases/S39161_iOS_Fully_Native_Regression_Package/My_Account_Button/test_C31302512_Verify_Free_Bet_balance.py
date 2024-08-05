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
class Test_C31302512_Verify_Free_Bet_balance(Common):
    """
    TR_ID: C31302512
    NAME: Verify Free Bet balance
    DESCRIPTION: This test case verifies that amount of Free Bets available is displayed below the Account Balance (based on currency of Free Bet awarded) if AND user has Free Bet amount available to spend
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. user is logged in
    PRECONDITIONS: 3. user has not any free bet available
    """
    keep_browser_open = True

    def test_001_emulate_free_bet_has_been_awarded_to_user(self):
        """
        DESCRIPTION: Emulate free bet has been awarded to User
        EXPECTED: Amount of Free Bets is available below the Account Balance (based on currency of Free Bet awarded)
        EXPECTED: AND is presented through Animation as per designs attached:
        EXPECTED: https://jira.egalacoral.com/secure/attachment/1290957/Native-Lads-Header_v1.mp4
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/6348766)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/6348768)
        """
        pass
