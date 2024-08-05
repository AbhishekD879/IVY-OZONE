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
class Test_C60086586_User_add_remove_Odds_Boost(Common):
    """
    TR_ID: C60086586
    NAME: User add/remove Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: Odds boost is available
    PRECONDITIONS: Betslip with 2 selections
    PRECONDITIONS: Betslip is expanded.
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98e668618bbbae028a133 - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa98a1775d4a236be20213 - Coral
    """
    keep_browser_open = True

    def test_001_observe_betslip(self):
        """
        DESCRIPTION: Observe Betslip
        EXPECTED: Odds Boost icon is displayed on Bet Slip
        """
        pass

    def test_002_tap_on_odds_boost_button(self):
        """
        DESCRIPTION: Tap on Odds boost button
        EXPECTED: Animation is displayed, prices are boosted, old prices are crossed out
        EXPECTED: FROM -> TO
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/122183751) ![](index.php?/attachments/get/122183750)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/122183752) ![](index.php?/attachments/get/122183753)
        EXPECTED: Transition guidelines:
        EXPECTED: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eac379287700c18d8439662
        EXPECTED: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5f1844b25f917a6b1f2da9fd
        """
        pass

    def test_003_tap_on_odds_boost_button_aggain(self):
        """
        DESCRIPTION: Tap on Odds boost button aggain
        EXPECTED: Animation is displayed, prices are UNboosted, old prices are displayed
        EXPECTED: FROM -> TO
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/122183750) ![](index.php?/attachments/get/122183751)
        EXPECTED: Ladbrokes:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/122183753) ![](index.php?/attachments/get/122183752)
        """
        pass
