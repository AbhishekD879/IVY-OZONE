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
class Test_C59927335_User_removes_Odds_Boost(Common):
    """
    TR_ID: C59927335
    NAME: User removes Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: Odds boost is activated (tapped before)
    PRECONDITIONS: Betslip is collapsed
    PRECONDITIONS: Design
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97cf00f9de0240979268d
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa8af9e4cb5b24eb3e9260
    """
    keep_browser_open = True

    def test_001_observe_betslip(self):
        """
        DESCRIPTION: Observe Betslip
        EXPECTED: Odds Boost icon is displayed on Bet Slip
        """
        pass

    def test_002_tap_on_odds_boost_button_again(self):
        """
        DESCRIPTION: Tap on Odds boost button again
        EXPECTED: Bold colour odd is removed with previous price displayed as original including Animation from precondition
        EXPECTED: ![](index.php?/attachments/get/119602018)
        EXPECTED: ![](index.php?/attachments/get/119602017)
        EXPECTED: Transition guidelines:
        EXPECTED: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eac379287700c18d8439662
        EXPECTED: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5f1844b25f917a6b1f2da9fd
        """
        pass

    def test_003_repeat_steps_1_2_with_expanded_bet_slip(self):
        """
        DESCRIPTION: Repeat steps 1-2 with expanded bet slip
        EXPECTED: 
        """
        pass
