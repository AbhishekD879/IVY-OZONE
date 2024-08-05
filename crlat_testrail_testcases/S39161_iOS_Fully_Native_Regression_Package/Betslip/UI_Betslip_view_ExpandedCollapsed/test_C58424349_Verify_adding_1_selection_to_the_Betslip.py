import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C58424349_Verify_adding_1_selection_to_the_Betslip(Common):
    """
    TR_ID: C58424349
    NAME: Verify adding 1 selection to the Betslip
    DESCRIPTION: This test case verifies adding 1 selection to the Betslip
    PRECONDITIONS: - Application is installed and launched
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/dashboard
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/dashboard
    """
    keep_browser_open = True

    def test_001_add_1_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add 1 selection to the Betslip
        EXPECTED: - Selection is added to the Betslip
        EXPECTED: - Collapsed BetSlip view is displayed
        """
        pass

    def test_002_verify_betslip_view_details(self):
        """
        DESCRIPTION: Verify Betslip view details
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/109061172)
        EXPECTED: Ladbrokes Dark mode:
        EXPECTED: ![](index.php?/attachments/get/109061171)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/109061169)
        EXPECTED: CORAL Dark mode:
        EXPECTED: ![](index.php?/attachments/get/109061170)
        """
        pass
