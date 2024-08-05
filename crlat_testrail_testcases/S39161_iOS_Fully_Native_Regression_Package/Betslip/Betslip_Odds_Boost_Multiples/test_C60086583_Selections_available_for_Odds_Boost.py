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
class Test_C60086583_Selections_available_for_Odds_Boost(Common):
    """
    TR_ID: C60086583
    NAME: Selections available for Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: User adds two selection to bet slip
    PRECONDITIONS: The selection qualifies as an Odds Boost available selection
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98e668618bbbae028a133 - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa98a1775d4a236be20213 - Coral
    PRECONDITIONS: Betslip is collapsed
    """
    keep_browser_open = True

    def test_001_observe_betslip(self):
        """
        DESCRIPTION: Observe Betslip
        EXPECTED: Odds Boost icon is displayed on Bet Slip area
        """
        pass

    def test_002_repeat_step_1_with_expanded_bet_slip(self):
        """
        DESCRIPTION: Repeat step 1 with expanded bet slip
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/122183493) ![](index.php?/attachments/get/122183494)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/122183496) ![](index.php?/attachments/get/122183495)
        """
        pass
