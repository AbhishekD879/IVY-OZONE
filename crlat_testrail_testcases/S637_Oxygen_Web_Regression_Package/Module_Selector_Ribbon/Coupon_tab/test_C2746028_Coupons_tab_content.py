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
class Test_C2746028_Coupons_tab_content(Common):
    """
    TR_ID: C2746028
    NAME: Coupons tab content
    DESCRIPTION: This test case verifies content displaying of a "Coupons" tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have a module "Coupons" created and enabled in CMS > Module Ribbon Tabs
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have segments created in CMS > Football Coupon > Coupon Segments
    PRECONDITIONS: - Segments should be active by time period
    PRECONDITIONS: - Some coupons should be assigned to segments and some shouldn't
    PRECONDITIONS: - You should be on a Home page > Coupons tab
    PRECONDITIONS: NOTE: Coral brand uses "Coupons" name for coupons tab and "Ladbrokes" brand uses "Accas" name for coupons tab
    """
    keep_browser_open = True

    def test_001_verify_coupons_tab_content(self):
        """
        DESCRIPTION: Verify "Coupons" tab content
        EXPECTED: - All active segments with coupons are displayed
        EXPECTED: - Coupons assigned to segments are displayed under respective segments
        EXPECTED: - Coupons not assigned to any segment are displayed within the "Popular" segment
        """
        pass
