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
class Test_C31379485_Verify_Hidden_Balance_UI(Common):
    """
    TR_ID: C31379485
    NAME: Verify Hidden Balance UI
    DESCRIPTION: This test case verifies hidden balance feature UI
    PRECONDITIONS: 1. app is installed and launched
    PRECONDITIONS: 2. user is in logged in state
    PRECONDITIONS: 3. user has available amount of account balance/free bet
    """
    keep_browser_open = True

    def test_001_emulate_hidden_balance(self):
        """
        DESCRIPTION: emulate hidden balance
        EXPECTED: Amount of account/free bet balance is hidden/removed with 'Balance' state
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/6348785)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/6348786)
        """
        pass

    def test_002_emulate_available_balance(self):
        """
        DESCRIPTION: emulate available balance
        EXPECTED: Account/free bet Balance is displayed (based on currency of user account)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/6348787)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/6348788)
        """
        pass
