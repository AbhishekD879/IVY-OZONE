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
class Test_C37568641_Verify_Info_displayed_on_Greyhound_Card(Common):
    """
    TR_ID: C37568641
    NAME: Verify Info displayed on Greyhound Card
    DESCRIPTION: This test case verifies Greyhound Card Information/Data
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://zpl.io/agBGM6Z
    DESCRIPTION: Coral:
    DESCRIPTION: https://zpl.io/aR0YNZ0
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default on the Home page
    PRECONDITIONS: - A Greyhounds module is present on Featured Tab
    PRECONDITIONS: - The Greyhound module includes one or more Greyhound Events
    """
    keep_browser_open = True

    def test_001_verify_info_described_on_greyhound_event_card(self):
        """
        DESCRIPTION: Verify info described on Greyhound Event Card
        EXPECTED: - Event Name (E.G 11.09 Romford)
        EXPECTED: - Countdown Timer (E.G Starts in 15:00)
        EXPECTED: - Each Way Terms (E.G E/W 1/4 Places 1-2-3)
        EXPECTED: - Trap Number
        EXPECTED: - Greyhound Name
        EXPECTED: - Trainer Name
        EXPECTED: - Form
        EXPECTED: - Odds Button
        EXPECTED: - Previous Price (maximum of two previous prices)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/46350900)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/46350901)
        """
        pass
