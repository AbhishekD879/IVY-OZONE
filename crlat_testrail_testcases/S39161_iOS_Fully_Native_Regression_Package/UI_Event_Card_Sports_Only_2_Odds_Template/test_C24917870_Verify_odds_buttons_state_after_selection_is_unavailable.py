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
class Test_C24917870_Verify_odds_buttons_state_after_selection_is_unavailable(Common):
    """
    TR_ID: C24917870
    NAME: Verify odds buttons state after selection is unavailable
    DESCRIPTION: This test case verifies odds button state in case selection is unavailable
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

    def test_001_emulate_unavailable_selection(self):
        """
        DESCRIPTION: emulate unavailable selection
        EXPECTED: * selection is unavailable
        EXPECTED: * 'N/A' title within Odds button is displayed as per design:
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/42446)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745385)
        """
        pass
