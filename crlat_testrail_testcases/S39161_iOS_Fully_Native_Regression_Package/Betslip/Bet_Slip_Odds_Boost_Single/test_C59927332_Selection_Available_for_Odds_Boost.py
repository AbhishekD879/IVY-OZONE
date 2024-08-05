import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.native
@vtest
class Test_C59927332_Selection_Available_for_Odds_Boost(Common):
    """
    TR_ID: C59927332
    NAME: Selection Available for Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: User adds a selection to bet slip
    PRECONDITIONS: The selection qualifies as an Odds Boost available selection
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97cea805fe12506e38c97
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa8af7e4cb5b24eb3e9218
    PRECONDITIONS: Betslip is collapse
    """
    keep_browser_open = True

    def test_001_observe_betslip(self):
        """
        DESCRIPTION: Observe Betslip
        EXPECTED: Odds Boost icon is displayed on Bet Slip
        EXPECTED: Light theme
        EXPECTED: ![](index.php?/attachments/get/119601991)
        EXPECTED: ![](index.php?/attachments/get/119601990)
        EXPECTED: Dark theme
        EXPECTED: ![](index.php?/attachments/get/119601993)
        EXPECTED: ![](index.php?/attachments/get/119601995)
        """
        pass

    def test_002_repeat_step_1_with_expanded_bet_slip(self):
        """
        DESCRIPTION: Repeat step 1 with expanded bet slip
        EXPECTED: Light theme
        EXPECTED: ![](index.php?/attachments/get/119601998)
        EXPECTED: ![](index.php?/attachments/get/119602001)
        EXPECTED: Dark theme
        EXPECTED: ![](index.php?/attachments/get/119601996)
        EXPECTED: ![](index.php?/attachments/get/119601997)
        """
        pass
