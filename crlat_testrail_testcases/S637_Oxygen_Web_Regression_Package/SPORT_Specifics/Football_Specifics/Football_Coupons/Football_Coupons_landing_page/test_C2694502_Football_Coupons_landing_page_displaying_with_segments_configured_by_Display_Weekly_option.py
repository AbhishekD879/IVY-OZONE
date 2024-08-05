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
class Test_C2694502_Football_Coupons_landing_page_displaying_with_segments_configured_by_Display_Weekly_option(Common):
    """
    TR_ID: C2694502
    NAME: Football Coupons landing page displaying with segments configured by "Display Weekly" option
    DESCRIPTION: This test case verifies displaying of segment configured by "Display Weekly" option.
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have segments created (In CMS >Football Coupon > Coupon Segments) with coupons assigned and segments should be configured by "Display Weekly" option
    PRECONDITIONS: - Some segments should be configured to be shown today (e.g. set "MON" if today is Monday) and some segments to be shown on other days (e.g. set "TUE", "WED" etc. if today is Monday)
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_football_coupons_landing_page_content_displaying(self):
        """
        DESCRIPTION: Verify Football Coupons landing page content displaying
        EXPECTED: - Segment with the highest order in CMS and is configured to be shown today is displayed only
        EXPECTED: - Coupons which are assigned to the segment are shown within it
        EXPECTED: - All other coupons are shown within 'Popular' segment
        EXPECTED: - Segments configured to be shown on other days are not displayed despite their order in CMS
        """
        pass

    def test_002___in_cms__football_coupon__coupon_segments_edit_segment_configured_to_be_shown_today_uncheck_check_box_for_todays_day_and_check_check_box_for_any_other_day__refresh_the_page_in_application__verify_displaying_of_a_football_coupons_segment_which_was_unchecked_to_be_shown_today(self):
        """
        DESCRIPTION: - In CMS > Football Coupon > Coupon Segments edit segment configured to be shown today: uncheck check box for today's day and check check box for any other day
        DESCRIPTION: - Refresh the page in application
        DESCRIPTION: - Verify displaying of a Football Coupons segment which was unchecked to be shown today
        EXPECTED: - Edited segment from step 2 is not shown any more
        EXPECTED: - Segment with the highest order in CMS and is configured to be shown today is displayed only
        EXPECTED: - Coupons which were assigned to undisplayed segment are now shown within "Popular" segment
        EXPECTED: - Coupons which are assigned to the currently displayed segment are shown only within it and not shown within 'Popular' segment
        """
        pass

    def test_003_verify_that_just_one_football_segment_is_displayed_at_a_time_on_coupons_page_above_popular_coupons_section_even_if_there_are_several_of_them_configured_in_cms(self):
        """
        DESCRIPTION: Verify that just one football segment is displayed at a time on Coupons page above 'Popular Coupons' section (even if there are several of them configured in CMS).
        EXPECTED: 
        """
        pass
