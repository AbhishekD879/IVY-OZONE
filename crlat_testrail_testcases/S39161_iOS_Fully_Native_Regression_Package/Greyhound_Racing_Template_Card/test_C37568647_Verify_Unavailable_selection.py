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
class Test_C37568647_Verify_Unavailable_selection(Common):
    """
    TR_ID: C37568647
    NAME: Verify Unavailable selection
    DESCRIPTION: This test case verifies the behavior Odds button on the Greyhound Racing Card event when selection is suspended.
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://zpl.io/bL16pJd
    DESCRIPTION: Coral:
    DESCRIPTION: https://zpl.io/VOpKOyj
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - The Greyhound Racing module is present on Featured Tab
    PRECONDITIONS: - The Greyhound Racing module includes one or more Greyhound Racing Events
    """
    keep_browser_open = True

    def test_001_emulate_the_unavailable_of_selection_for_the_greyhound_event(self):
        """
        DESCRIPTION: Emulate the unavailable of selection for the Greyhound Event
        EXPECTED: - The selection on the Greyhound Racing Event card is unavailable
        EXPECTED: - 'N/A' title within the Odds button is displayed as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/46085385)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/46085386)
        """
        pass
