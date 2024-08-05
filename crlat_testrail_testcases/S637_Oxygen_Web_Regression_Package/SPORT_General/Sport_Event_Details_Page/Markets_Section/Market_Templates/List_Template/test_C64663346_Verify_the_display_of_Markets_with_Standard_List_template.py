import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64663346_Verify_the_display_of_Markets_with_Standard_List_template(Common):
    """
    TR_ID: C64663346
    NAME: Verify the display of Markets with Standard List template
    DESCRIPTION: This test case verifies display of market with Standard list templet
    PRECONDITIONS: 1.Market with List templet should be available ex:Outright,GetAPrice etc..
    PRECONDITIONS: ![](index.php?/attachments/get/d6eae6da-13ca-4fdb-847d-457e6be39d0c)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page(self):
        """
        DESCRIPTION: Navigate to EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_any_market_which_has_list_templetexoutrightgetaprice(self):
        """
        DESCRIPTION: Expand any market which has list templet
        DESCRIPTION: Ex:Outright,GetAPrice
        EXPECTED: * Market Header should be displayed with standerd list templet available
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/15c3b55d-6105-4410-9120-7857fafe251a)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/db3beb71-7610-4f02-8f11-2382ee10ad18)
        """
        pass
