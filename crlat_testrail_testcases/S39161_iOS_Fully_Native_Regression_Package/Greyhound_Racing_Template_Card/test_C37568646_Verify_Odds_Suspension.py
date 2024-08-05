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
class Test_C37568646_Verify_Odds_Suspension(Common):
    """
    TR_ID: C37568646
    NAME: Verify Odds Suspension
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

    def test_001_emulate_selection_suspension_for_the_greyhound_event(self):
        """
        DESCRIPTION: Emulate selection suspension for the Greyhound event
        EXPECTED: - selection on the Greyhound Event card is suspended
        EXPECTED: - 'SUSP' title within Odds button is displayed as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/45754221)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/45754222)
        """
        pass
