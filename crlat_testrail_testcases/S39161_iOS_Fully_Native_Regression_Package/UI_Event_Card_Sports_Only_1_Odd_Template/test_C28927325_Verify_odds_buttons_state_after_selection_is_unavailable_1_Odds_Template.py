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
class Test_C28927325_Verify_odds_buttons_state_after_selection_is_unavailable_1_Odds_Template(Common):
    """
    TR_ID: C28927325
    NAME: Verify odds buttons state after selection is unavailable (1 Odds Template)
    DESCRIPTION: This test case verifies odds button state in case selection is unavailable
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - Pre-Match event card with 1 odds Template is available
    PRECONDITIONS: - User is navigated to the Event that contains 1 Odds Template
    PRECONDITIONS: Design
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_emulate_unavailable_selection(self):
        """
        DESCRIPTION: Emulate unavailable selection
        EXPECTED: - selection is unavailable
        EXPECTED: - 'N/A' title within the Odds button is displayed as per design:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/3027307)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3027308)
        """
        pass
