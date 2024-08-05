import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58424356_Verify_expanded_view_of_1_selection_in_the_Betslip(Common):
    """
    TR_ID: C58424356
    NAME: Verify expanded view of 1 selection in the Betslip
    DESCRIPTION: This test case verifies expanded view of 1 selection in the Betslip
    PRECONDITIONS: - Application is installed and launched
    PRECONDITIONS: - One selection is added to the Betslip
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard
    """
    keep_browser_open = True

    def test_001_slide_betslip_upwards(self):
        """
        DESCRIPTION: Slide BetSlip upwards
        EXPECTED: The Betslip in the expanded view is displayed
        """
        pass

    def test_002_verify_expanded_betslip_view_details(self):
        """
        DESCRIPTION: Verify expanded Betslip view details
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/109061174)
        EXPECTED: Ladbrokes Dark Mode
        EXPECTED: ![](index.php?/attachments/get/109061173)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/109061177)
        EXPECTED: Coral Dark Mode
        EXPECTED: ![](index.php?/attachments/get/109061176)
        """
        pass

    def test_003_slide_betslip_down(self):
        """
        DESCRIPTION: Slide Betslip down
        EXPECTED: The collapsed Bet Slip view is displayed
        """
        pass
