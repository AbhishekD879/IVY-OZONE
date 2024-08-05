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
class Test_C64663347_Verify_the_display_of_Market_Header(Common):
    """
    TR_ID: C64663347
    NAME: Verify the display of Market Header
    DESCRIPTION: This test case verifies the display of market header for list templet
    PRECONDITIONS: 1.Market with List templet should be available ex:Outright,GetAPrice etc..
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

    def test_003_expand_any_market_which_has_list_templet_and_check_market_headerexoutrightgetaprice(self):
        """
        DESCRIPTION: Expand any market which has list templet and check market header
        DESCRIPTION: Ex:Outright,GetAPrice
        EXPECTED: * Market Header should be displayed along with signposting if available
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/b913b04e-a8d0-47f3-ae3d-6508f9a7a2d0)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/e348d741-25b9-4c47-9d2f-e8679e1677d8)
        """
        pass
