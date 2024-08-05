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
class Test_C24917869_Verify_odds_button_state_after_selection_is_suspended(Common):
    """
    TR_ID: C24917869
    NAME: Verify odds button state after selection is suspended
    DESCRIPTION: This test case verifies odds button state when selection is suspended
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

    def test_001_emulate_that_selection_is_suspended(self):
        """
        DESCRIPTION: emulate that selection is suspended
        EXPECTED: * selection is suspended
        EXPECTED: * 'SUSP' title within Odds button is displayed as per design:
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/42445)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745384)
        """
        pass
