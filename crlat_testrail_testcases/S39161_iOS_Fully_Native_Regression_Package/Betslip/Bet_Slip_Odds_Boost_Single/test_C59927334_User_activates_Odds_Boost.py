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
class Test_C59927334_User_activates_Odds_Boost(Common):
    """
    TR_ID: C59927334
    NAME: User activates Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: Odds boost is available but not activated
    PRECONDITIONS: Betslip is collapsed
    PRECONDITIONS: Design
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea97cf00f9de0240979268d
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa8af9e4cb5b24eb3e9260
    """
    keep_browser_open = True

    def test_001_click_on_odds_boost_icon(self):
        """
        DESCRIPTION: Click on Odds Boost Icon
        EXPECTED: Odds are crossed out.
        EXPECTED: New odds presented in bold colour as per design attached including Animation
        EXPECTED: https://jira.egalacoral.com/secure/attachment/1427141/betslip-oddsboost.mp4
        EXPECTED: https://coralracing.sharepoint.com/sites/NATIVEPROJECTDELIVERY/Shared%20Documents/General/03-Betslip%20Optimisation/Coral/03-Prototypes/coral-oddsboostbutton.mp4
        EXPECTED: ![](index.php?/attachments/get/119602014)
        EXPECTED: ![](index.php?/attachments/get/119602015)
        EXPECTED: Transition guidelines:
        EXPECTED: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eac379287700c18d8439662
        EXPECTED: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5f1844b25f917a6b1f2da9fd
        """
        pass

    def test_002_repeat_step_1_with_expanded_bet_slip(self):
        """
        DESCRIPTION: Repeat step 1 with expanded bet slip
        EXPECTED: 
        """
        pass
