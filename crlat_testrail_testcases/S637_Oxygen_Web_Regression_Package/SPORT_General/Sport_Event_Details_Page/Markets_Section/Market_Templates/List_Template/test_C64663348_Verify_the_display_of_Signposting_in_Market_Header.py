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
class Test_C64663348_Verify_the_display_of_Signposting_in_Market_Header(Common):
    """
    TR_ID: C64663348
    NAME: Verify the display of Signposting in Market Header
    DESCRIPTION: This test case verifies signposting for market templet
    PRECONDITIONS: 1.Market with List templet should be available ex:Outright,GetAPrice etc..
    PRECONDITIONS: ![](index.php?/attachments/get/614afc21-740c-4dd2-9bda-b4e6817fe9a5)
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

    def test_003_expand_any_market_which_has_list_templet_and_check_the_signpostingexoutrightgetaprice(self):
        """
        DESCRIPTION: Expand any market which has list templet and check the signposting
        DESCRIPTION: Ex:Outright,GetAPrice
        EXPECTED: * Market Header should be displayed along with signposting if available
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/1fbf465c-3ac5-4674-95e4-dd8544d759ba)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/26410426-06ef-4740-9efa-09e96ed7d057)
        """
        pass
