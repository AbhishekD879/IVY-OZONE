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
class Test_C24917868_Verify_odds_button_state_after_selection_has_a_price_change(Common):
    """
    TR_ID: C24917868
    NAME: Verify odds button state after selection has a price change
    DESCRIPTION: This test case verifies odds button state after selection has a price change
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default
    PRECONDITIONS: * Pre-Match event card with 2 odds Template is available
    PRECONDITIONS: * User is navigated to the Event that contains 2 Odds Template
    """
    keep_browser_open = True

    def test_001_emulate_the_selection_price_change_price_up(self):
        """
        DESCRIPTION: Emulate the selection price change (Price up)
        EXPECTED: the Odds Price within Odds Button changes colour as per design
        EXPECTED: * animation duration is 2000ms
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/42443)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745382)
        """
        pass

    def test_002_emulate_the_selection_price_change_down(self):
        """
        DESCRIPTION: Emulate the selection price change (Down)
        EXPECTED: the Odds Price within Odds Button changes colour as per design
        EXPECTED: * animation duration is 2000ms
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/42443)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745383)
        """
        pass
