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
class Test_C2694504_Football_Coupons_landing_page_coupons_ordering_within_the_segments(Common):
    """
    TR_ID: C2694504
    NAME: Football Coupons landing page coupons ordering within the segments
    DESCRIPTION: This test case verifies coupons ordering on a Football Coupons landing page
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

    def test_001_verify_coupons_ordering(self):
        """
        DESCRIPTION: Verify coupons ordering
        EXPECTED: - Coupons within custom segments are ordered according to the coupons IDs order in CMS
        EXPECTED: - Coupons in a "Popular" segment are ordered by OB display order
        """
        pass
