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
class Test_C59923220_Verify_behaviour_of_Price_Boost_signposting_in_betslip(Common):
    """
    TR_ID: C59923220
    NAME: Verify  behaviour of  Price Boost signposting in betslip.
    DESCRIPTION: This test case verifies the behaviour of "Price Boost" signposting in collapsed/expanded betslips.
    PRECONDITIONS: App is installed and launched:
    PRECONDITIONS: Designs:
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5eaaf04734c349b6cdef883e - Ladbrokes
    PRECONDITIONS: https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eb2c2bf7fce624e1be930c5 - Coral
    """
    keep_browser_open = True

    def test_001_add_selection_with_price_boost_to_the_betslip(self):
        """
        DESCRIPTION: Add selection with "Price Boost" to the Betslip.
        EXPECTED: * Selection is added to the Betslip
        EXPECTED: * Collapsed Betslip view with Bottom Bar displayed
        EXPECTED: * "Price Boost" signposting below the selection name is not shown.
        """
        pass

    def test_002_expand_the_betslip(self):
        """
        DESCRIPTION: Expand the Betslip.
        EXPECTED: * Betslip is expanded.
        EXPECTED: * "Price Boost" signposting is shown below the selection name (Ladbrokes).
        EXPECTED: Ladbrokes: ![](index.php?/attachments/get/119657449)
        EXPECTED: * "Price Boost" signposting is shown below the event name (Coral).
        EXPECTED: Coral: ![](index.php?/attachments/get/119657450)
        """
        pass

    def test_003_collapse_the_betslip(self):
        """
        DESCRIPTION: Collapse the Betslip.
        EXPECTED: * Betslip is collapsed.
        EXPECTED: * "Price Boost" signposting below the selection name is not shown.
        """
        pass
