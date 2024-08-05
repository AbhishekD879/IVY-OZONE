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
class Test_C28790686_Verify_odds_button_state_after_tapping_on_Odds_1_odd_template(Common):
    """
    TR_ID: C28790686
    NAME: Verify odds button state after tapping on Odds (1 odd template)
    DESCRIPTION: This test case verifies odds button state after tapping on Odds
    PRECONDITIONS: Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Featured Tab is displayed by default
    PRECONDITIONS: Pre-Match event card with 1 odds Template is available
    PRECONDITIONS: Design
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_navigate_to_the_event_card_that_contains_1_odd_templatetap_on_an_odds_button(self):
        """
        DESCRIPTION: Navigate to the Event Card that contains 1 Odd Template
        DESCRIPTION: Tap on an 'Odds' Button
        EXPECTED: Odds button must be highlighted in Colour
        EXPECTED: Ladbrokes:
        EXPECTED: https://zpl.io/bL16pJd
        EXPECTED: ![](index.php?/attachments/get/2908874)
        EXPECTED: Coral:
        EXPECTED: https://zpl.io/VOpKOyj
        EXPECTED: ![](index.php?/attachments/get/2937070)
        """
        pass

    def test_002_tap_the_selected_odds_again(self):
        """
        DESCRIPTION: Tap the selected Odds again
        EXPECTED: Odds button returns to the original color
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/2937074)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/2937075)
        """
        pass
