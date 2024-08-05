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
class Test_C28908467_Verify_odds_button_state_after_selection_has_a_price_change_1_Odds_Template(Common):
    """
    TR_ID: C28908467
    NAME: Verify odds button state after selection has a price change (1 Odds Template)
    DESCRIPTION: This test case verifies odds button state after the selection has a price change
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

    def test_001_emulate_the_selection_price_change_price_up(self):
        """
        DESCRIPTION: Emulate the selection price change (Price up)
        EXPECTED: The Odds Price within Odds Button changes color as per design
        EXPECTED: - animation-duration is 2000ms
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/3004745)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3004746)
        """
        pass

    def test_002_emulate_the_selection_price_change_down(self):
        """
        DESCRIPTION: Emulate the selection price change (Down)
        EXPECTED: The Odds Price within Odds Button changes color as per design
        EXPECTED: - animation duration is 2000ms
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/3004747)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3004748)
        """
        pass
