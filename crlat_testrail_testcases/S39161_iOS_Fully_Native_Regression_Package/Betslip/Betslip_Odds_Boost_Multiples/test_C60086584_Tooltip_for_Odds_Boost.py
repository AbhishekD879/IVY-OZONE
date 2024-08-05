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
class Test_C60086584_Tooltip_for_Odds_Boost(Common):
    """
    TR_ID: C60086584
    NAME: Tooltip for Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: User adds  selections to bet slip
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98e63752e63bc004e57ec
    PRECONDITIONS: Betslip is expanded
    """
    keep_browser_open = True

    def test_001_observe_betslip(self):
        """
        DESCRIPTION: Observe Betslip
        EXPECTED: 'I' icon is displayed next to odds boost
        """
        pass

    def test_002_tap_on_i_icon(self):
        """
        DESCRIPTION: Tap on 'I' icon
        EXPECTED: User sees pop-up
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/122150088)  ![](index.php?/attachments/get/122183488)
        EXPECTED: Coral
        EXPECTED: ![](index.php?/attachments/get/122183489) ![](index.php?/attachments/get/122183490)
        """
        pass
