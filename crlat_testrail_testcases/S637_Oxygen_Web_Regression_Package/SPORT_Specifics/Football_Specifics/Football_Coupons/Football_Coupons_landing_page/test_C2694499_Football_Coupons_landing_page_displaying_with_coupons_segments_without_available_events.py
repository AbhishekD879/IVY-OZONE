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
class Test_C2694499_Football_Coupons_landing_page_displaying_with_coupons_segments_without_available_events(Common):
    """
    TR_ID: C2694499
    NAME: Football Coupons landing page displaying with coupons segments without available events
    DESCRIPTION: This test case verifies Football Coupons landing page displaying when there are active segments available and there are coupons without available events
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have NO coupons with available events
    PRECONDITIONS: - You should have a segment created (In CMS >Football Coupon > Coupon Segments) with coupons assigned and some coupons should stay not assigned to any segment
    PRECONDITIONS: - Segment should be active by time period
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_segments_and_coupons_displaying(self):
        """
        DESCRIPTION: Verify segments and coupons displaying
        EXPECTED: - There are no custom segments displayed
        EXPECTED: - "Popular" segment is not displayed
        EXPECTED: - "No coupons found" message is displayed
        """
        pass
