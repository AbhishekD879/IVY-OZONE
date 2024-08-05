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
class Test_C28908468_Verify_odds_button_state_after_selection_is_suspended_1_Odds_Template(Common):
    """
    TR_ID: C28908468
    NAME: Verify odds button state after selection is suspended (1 Odds Template)
    DESCRIPTION: This test case verifies odds button state when selection is suspended
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - Pre-Match event card with 1 Odds Template is available
    PRECONDITIONS: - User is navigated to the Event that contains 1 Odds Template
    PRECONDITIONS: Design
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_emulate_that_selection_is_suspended(self):
        """
        DESCRIPTION: Emulate that selection is suspended
        EXPECTED: - Selection is suspended
        EXPECTED: - 'SUSP' title within Odds button is displayed as per design:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/3016027)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3021667)
        """
        pass
