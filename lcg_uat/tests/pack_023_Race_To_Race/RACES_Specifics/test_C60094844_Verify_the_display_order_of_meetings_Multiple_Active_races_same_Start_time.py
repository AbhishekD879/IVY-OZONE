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
class Test_C60094844_Verify_the_display_order_of_meetings_Multiple_Active_races_same_Start_time(Common):
    """
    TR_ID: C60094844
    NAME: Verify the display order of meetings- Multiple Active races-same Start time
    DESCRIPTION: Verify the display order of meetings within a country panel when there are Multiple Active races which start at same time
    PRECONDITIONS: 1: Multiple meetings should have ACTIVE races which start at same time
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

    def test_003_verify_the_meetings_displayed_in_the_country_panel_with_multiple_active_races_with_same_start_timebefore_page_refresh(self):
        """
        DESCRIPTION: Verify the meetings displayed in the Country panel with multiple ACTIVE races with same start time
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

    def test_005_verify_the_meetings_with_active_races_starting_at_same_time_are_arranged_as_per_open_bet_ranking(self):
        """
        DESCRIPTION: Verify the meetings with ACTIVE Races starting at same time are arranged as per Open Bet ranking
        EXPECTED: Meeting with ACTIVE races starting at same time should be pushed to Top and repositioned among ACTIVE races as per Open Bet ranking
        """
        pass
