import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.native
@vtest
class Test_C29807823_Verify_UI_after_Tapping_on_Odds_Button(Common):
    """
    TR_ID: C29807823
    NAME: Verify UI after Tapping on 'Odds' Button
    DESCRIPTION: This test case verifies UI after Tapping on 'Odds' Button
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - Pre-Match event card with 3 odds Template is available
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_tap_on_an_odds_button(self):
        """
        DESCRIPTION: Tap on an 'Odds' Button
        EXPECTED: 'Odds' button is highlighted in Colour
        """
        pass

    def test_002_tap_the_selected_odds_again(self):
        """
        DESCRIPTION: Tap the selected 'Odds' again
        EXPECTED: 'Odds' button returns to the original colour
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39898)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704302)
        """
        pass
