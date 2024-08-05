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
class Test_C29807825_Verify_UI_of_Suspended_Unavailable_Odds_button(Common):
    """
    TR_ID: C29807825
    NAME: Verify UI of Suspended/Unavailable 'Odds' button
    DESCRIPTION: This test case verifies UI of Suspended/Unavailable 'Odds' button
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - Pre-Match event card with 3 odds Template is available
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_emulate_suspension_of_selection(self):
        """
        DESCRIPTION: Emulate Suspension of selection
        EXPECTED: - Selection is suspended
        EXPECTED: - 'SUSP' text is displayed within the 'Odds' button as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39906)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704329)
        """
        pass

    def test_002_emulate_unavailable_of_selection(self):
        """
        DESCRIPTION: Emulate Unavailable of selection
        EXPECTED: - The selection is unavailable
        EXPECTED: - 'N/A' text is displayed within the Odds button as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39907)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704330)
        """
        pass
