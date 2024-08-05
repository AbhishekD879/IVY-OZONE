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
class Test_C2694503_Football_Coupons_landing_page_displaying_with_segments_configured_by_Date_Period(Common):
    """
    TR_ID: C2694503
    NAME: Football Coupons landing page displaying with segments configured by "Date Period"
    DESCRIPTION: This test case verifies displaying of segment configured by time period.
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: - You should have coupons created with available events
    PRECONDITIONS: - You should have segments created (In CMS >Football Coupon > Coupon Segments) with coupons assigned and segments should be configured by "Time Period"
    PRECONDITIONS: - Some segments should be configured to be active today (e.g. their date range includes today's day) and some segments to be shown on other days (e.g. they are expired or setup in the future)
    PRECONDITIONS: - You should be on a Football Coupons landing page
    """
    keep_browser_open = True

    def test_001_verify_football_coupons_landing_page_content_displaying(self):
        """
        DESCRIPTION: Verify Football Coupons landing page content displaying
        EXPECTED: - Segment with the highest order in CMS and its date range includes current time is displayed only
        EXPECTED: - Coupons which are assigned to the segment are shown within it
        EXPECTED: - All other coupons are shown within 'Popular' segment
        EXPECTED: - Segments configured to be shown on other days are not displayed despite their order in CMS
        """
        pass

    def test_002___in_cms__football_coupon__coupon_segments_edit_currently_displayed_segment_change_its_date_range_to_be_expired_in_a_few_minutes__wait_for_the_segment_expire_time_and_refresh_the_page_in_application__verify_displaying_of_segments(self):
        """
        DESCRIPTION: - In CMS > Football Coupon > Coupon Segments edit currently displayed segment: change its date range to be expired in a few minutes
        DESCRIPTION: - Wait for the segment expire time and refresh the page in application
        DESCRIPTION: - Verify displaying of segments
        EXPECTED: - Edited segment from step 2 is not shown anymore
        EXPECTED: - Coupons which were assigned to undisplayed segment are now shown within "Popular" segment
        EXPECTED: - Segment with the highest order in CMS and its date range includes current time is displayed only
        EXPECTED: - Coupons which are assigned to the currently displayed segment are shown only within it and not shown within 'Popular' segment
        """
        pass

    def test_003___in_cms__football_coupon__coupon_segments_edit_currently_displayed_segment_change_its_date_range_to_be_shown_in_a_few_minutes_and_make_sure_it_will_have_the_highest_priority_when_it_will_be_active__wait_for_the_segment_display_time_and_refresh_the_page_in_application__verify_displaying_of_segments(self):
        """
        DESCRIPTION: - In CMS > Football Coupon > Coupon Segments edit currently displayed segment: change its date range to be shown in a few minutes and make sure it will have the highest priority when it will be active
        DESCRIPTION: - Wait for the segment display time and refresh the page in application
        DESCRIPTION: - Verify displaying of segments
        EXPECTED: - Segment from step 2 is not shown anymore
        EXPECTED: - Coupons which were assigned to undisplayed segment are now shown within "Popular" segment
        EXPECTED: - Segment with the highest order in CMS and its date range includes current time is displayed only
        EXPECTED: - Coupons which are assigned to the currently displayed segment are shown only within it and not shown within 'Popular' segment
        """
        pass

    def test_004_verify_that_just_one_football_segment_is_displayed_at_a_time_on_coupons_page_above_popular_coupons_section_even_if_there_are_several_of_them_configured_in_cms(self):
        """
        DESCRIPTION: Verify that just one football segment is displayed at a time on Coupons page above 'Popular Coupons' section (even if there are several of them configured in CMS).
        EXPECTED: 
        """
        pass
