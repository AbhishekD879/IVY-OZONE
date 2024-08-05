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
class Test_C2694501_Football_Coupons_landing_page_displaying_with_segment_with_available_events(Common):
    """
    TR_ID: C2694501
    NAME: Football Coupons landing page displaying with segment with available events
    DESCRIPTION: This test case verifies Football Coupons landing page displaying with segment with coupons
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have a segment created (In CMS >Football Coupon > Coupon Segments) with coupons assigned with available events
    PRECONDITIONS: - Segment should be active by time period
    PRECONDITIONS: - Some coupons with available events should be not assigned to any segment
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_segments_and_coupons_displaying(self):
        """
        DESCRIPTION: Verify segments and coupons displaying
        EXPECTED: - Custom segment is displayed with coupons assigned to it
        EXPECTED: - All not assigned coupons are displayed within "Popular" segment
        """
        pass
