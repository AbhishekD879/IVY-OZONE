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
class Test_C60086591_Tooltip_on_selection_for_Odds_Boost(Common):
    """
    TR_ID: C60086591
    NAME: Tooltip on selection for Odds Boost
    DESCRIPTION: Test case verifies odd boosting UI on Betslip
    PRECONDITIONS: User adds two selection to bet slip
    PRECONDITIONS: The selection qualifies as an Odds Boost available selection
    PRECONDITIONS: Design:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98e62752e63bc004e5738
    PRECONDITIONS: Betslip is expanded
    PRECONDITIONS: One selection on the bet slip is not available for odds boost
    """
    keep_browser_open = True

    def test_001_observe_betslip(self):
        """
        DESCRIPTION: Observe Betslip
        EXPECTED: 'I' icon is displayed next to odds boosted (not for unavailable )
        """
        pass

    def test_002_tap_on_unavailable_tooltip_icon(self):
        """
        DESCRIPTION: Tap on unavailable tooltip icon
        EXPECTED: Appropriate tool tip message is displayed
        EXPECTED: ![](index.php?/attachments/get/122150089)
        EXPECTED: ![](index.php?/attachments/get/122187414)
        """
        pass
