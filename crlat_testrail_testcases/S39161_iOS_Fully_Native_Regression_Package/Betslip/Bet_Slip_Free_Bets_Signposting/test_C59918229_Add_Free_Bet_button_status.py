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
class Test_C59918229_Add_Free_Bet_button_status(Common):
    """
    TR_ID: C59918229
    NAME: Add Free Bet button status
    DESCRIPTION: This test case describes Add Free Bet button status
    DESCRIPTION: Designs:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard?q=free&sid=5eada1f2d9cc2c193e409814
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard?sid=5ea99a214c42b7267ad5f237
    PRECONDITIONS: - user has a free bet available
    PRECONDITIONS: - qualifying selection is added to bet slip
    PRECONDITIONS: - betslip is expanded
    PRECONDITIONS: - free bet is not selected
    """
    keep_browser_open = True

    def test_001_verify_add_free_bet_button_status(self):
        """
        DESCRIPTION: Verify Add Free Bet button status
        EXPECTED: Free Bet Button is Inactive
        EXPECTED: Ladbrokes:
        EXPECTED: Light mode:
        EXPECTED: ![](index.php?/attachments/get/119425539)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/119778910)
        EXPECTED: Coral:
        EXPECTED: Light mode:
        EXPECTED: ![](index.php?/attachments/get/119778911)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/119778912)
        """
        pass

    def test_002_select_any_free_bet(self):
        """
        DESCRIPTION: Select any free bet
        EXPECTED: free bet is being selected
        EXPECTED: Bet Button should be active
        EXPECTED: Ladbrokes
        EXPECTED: Light mode:
        EXPECTED: ![](index.php?/attachments/get/119425540)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/119778913)
        EXPECTED: Coral
        EXPECTED: Light mode:
        EXPECTED: ![](index.php?/attachments/get/119778914)
        EXPECTED: Dark mode:
        EXPECTED: ![](index.php?/attachments/get/119778916)
        """
        pass
