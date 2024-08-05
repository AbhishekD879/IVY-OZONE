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
class Test_C2746307_Football_Coupons_landing_page_displaying_with_segments_configured_by_Display_Weekly_and_Date_Period(Common):
    """
    TR_ID: C2746307
    NAME: Football Coupons landing page displaying with segments configured by "Display Weekly" and "Date Period"
    DESCRIPTION: This test case verifies displaying of segments configured by "Display Weekly" and "Date Period"
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have segments created (In CMS > Football Coupon > Coupon Segments) with coupons assigned and segments should be configured by "Display Weekly" option
    PRECONDITIONS: - Some segments should be configured to be shown today (e.g. set "MON" if today is Monday) and some segments to be shown on other days (e.g. set "TUE", "WED" etc. if today is Monday)
    PRECONDITIONS: - You should have segments created (In CMS > Football Coupon > Coupon Segments) with coupons assigned and segments should be configured by "Time Period"
    PRECONDITIONS: - Some segments should be configured to be active today (e.g. their date range includes today's day) and some segments to be shown on other days (e.g. they are expired or setup in the future)
    PRECONDITIONS: - Put the segments configured by "Display Weekly" at the top (In CMS > Football Coupon > Coupon Segments)
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_football_coupons_landing_page_content_displaying(self):
        """
        DESCRIPTION: Verify Football Coupons landing page content displaying
        EXPECTED: - Segment configured by "Date Period" have bigger priority and segment with the highest order in CMS and its date range includes today's day is displayed
        EXPECTED: - Segment with higher order in CMS and configured to be shown today, but configured by "Display weekly is ignored in this case
        """
        pass

    def test_002___in_cms__football_coupon__coupon_segments_edit_segments_configured_by_display_range_to_be_inactive_in_current_time__refresh_the_page_in_application_and_verify_football_coupons_landing_page_content_displaying(self):
        """
        DESCRIPTION: - In CMS > Football Coupon > Coupon Segments edit segments configured by "Display Range" to be inactive in current time
        DESCRIPTION: - Refresh the page in application and verify Football Coupons landing page content displaying
        EXPECTED: Segment with the highest order in CMS and is configured to be shown today is displayed
        """
        pass
