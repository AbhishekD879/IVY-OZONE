import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C60094843_Verify_the_display_order_of_meetings_Multiple_Active_races_different_Start_time(Common):
    """
    TR_ID: C60094843
    NAME: Verify the display order of meetings- Multiple Active races-different Start time
    DESCRIPTION: Verify the display order of meetings within a country panel when there are Multiple Active races which start at different time
    PRECONDITIONS: 1: Multiple meetings should have ACTIVE races which start at different time
    PRECONDITIONS: ACTIVE: If the first race within a meeting starts in Next 10 minutes
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_verify_the_meetings_displayed_in_the_country_panel_with_multiple_active_races_with_different_start_timebefore_page_refresh(self):
        """
        DESCRIPTION: Verify the meetings displayed in the Country panel with multiple ACTIVE races with different start time
        DESCRIPTION: (Before Page refresh)
        EXPECTED: The meetings in Country panel should be displayed as per OB ranking
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 
        """
        pass

    def test_005_verify_the_meetings_are_arranged_as_per_their_ob_rankings_as_their_first_priority_when_they_are_multiple_active_racesexamplekempton_starts_in_5_minutes_southwell_starts_in_7_minutes_and_ascot_starts_in_3_minutesand_let_say_ob_rankings_is_southwell_as_rank_1__kempton_r2__ascot_as_r3_the_order_will_be1southwell2kempton3ascot(self):
        """
        DESCRIPTION: Verify the meetings are arranged as per their OB rankings as their first priority, When they are multiple ACTIVE races.
        DESCRIPTION: Example:
        DESCRIPTION: Kempton starts in 5 minutes, Southwell starts in 7 minutes, and Ascot starts in 3 minutes.
        DESCRIPTION: and Let say OB rankings is Southwell as Rank-1 , Kempton R2 & Ascot as R3 the order will be:
        DESCRIPTION: 1.Southwell
        DESCRIPTION: 2.Kempton
        DESCRIPTION: 3.Ascot
        EXPECTED: meetings are arranged as per their OB rankings as their first priority, When they are multiple ACTIVE races.
        EXPECTED: Example:
        EXPECTED: Kempton starts in 5 minutes, Southwell starts in 7 minutes, and Ascot starts in 3 minutes.
        EXPECTED: and Let say OB rankings is Southwell as Rank-1 , Kempton R2 & Ascot as R3 the order will be:
        EXPECTED: 1.Southwell
        EXPECTED: 2.Kempton
        EXPECTED: 3.Ascot
        """
        pass
