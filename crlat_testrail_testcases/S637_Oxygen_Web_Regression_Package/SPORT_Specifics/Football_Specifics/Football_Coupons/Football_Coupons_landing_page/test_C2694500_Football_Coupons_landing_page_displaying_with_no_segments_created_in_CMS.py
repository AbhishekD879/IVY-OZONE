import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C2694500_Football_Coupons_landing_page_displaying_with_no_segments_created_in_CMS(Common):
    """
    TR_ID: C2694500
    NAME: Football Coupons landing page displaying with no segments created in CMS
    DESCRIPTION: This test case verifies Football Coupons landing page displaying without created segments with coupons available
    DESCRIPTION: Note: can't be automated as there always will be Segments configured in CMS
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have no segment created in CMS > Football Coupon > Coupon Segments
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_segments_and_coupons_displaying(self):
        """
        DESCRIPTION: Verify segments and coupons displaying
        EXPECTED: - Only "Popular" segment is displayed with all coupons with available events
        """
        pass
