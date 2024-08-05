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
class Test_C2694505_Football_Coupons_landing_page_segments_ordering(Common):
    """
    TR_ID: C2694505
    NAME: Football Coupons landing page segments ordering
    DESCRIPTION: This test case verifies segments ordering on a Football Coupons landing page
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have a segment created (In CMS >Football Coupon > Coupon Segments) with coupons assigned with available events
    PRECONDITIONS: - Segments should be active by time period
    PRECONDITIONS: - Some coupons with available events should be not assigned to any segment
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_ordering_of_segments(self):
        """
        DESCRIPTION: Verify ordering of segments
        EXPECTED: - Custom segment is always shown the first
        EXPECTED: - "Popular" segment is always shown the last
        """
        pass
