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
class Test_C60094841_Verify_the_display_order_of_meeting_first_race_in_next_10_min(Common):
    """
    TR_ID: C60094841
    NAME: Verify the display order of meeting- first race in next 10 min
    DESCRIPTION: Verify that first race in a meeting is about to start in next 10 minutes then that Meeting should raise above within the specific Country panel
    PRECONDITIONS: 1: First race in a meeting should start in Next 10 minutes
    PRECONDITIONS: 2: No other meeting within that Country panel should be Active
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

    def test_003_verify_any_country_panel_meeting_which_has_race_in_next_10_minutesany_meeting_first_race_did_not_start(self):
        """
        DESCRIPTION: Verify any Country Panel meeting which has race in Next 10 minutes
        DESCRIPTION: (Any meeting first race did not start)
        EXPECTED: The meetings in Country panel should be displayed as per OB ranking
        """
        pass

    def test_004_refresh_the_page_in_the_active_window_within_10_minutes_of_start_time(self):
        """
        DESCRIPTION: Refresh the page in the ACTIVE window (within 10 minutes of start time)
        EXPECTED: User should be able to refresh the page
        """
        pass

    def test_005_verify_the_meeting_within_the_country_panel_raises_above_and_displays_at_the_topexamplemeeting_1_1300_1330_1400meeting_2_0800_0830_0900meeting_3_0300_0330_0400meeting_4_1100_1130_1200after_page_refresh_at_250(self):
        """
        DESCRIPTION: Verify the meeting within the Country panel raises above and displays at the top
        DESCRIPTION: Example:
        DESCRIPTION: Meeting 1: 13:00, 13:30, 14:00,...
        DESCRIPTION: Meeting 2: 08:00. 08:30, 09:00,...
        DESCRIPTION: Meeting 3: 03:00. 03:30, 04:00,...
        DESCRIPTION: Meeting 4: 11:00, 11:30. 12:00,…
        DESCRIPTION: After page refresh at 2:50
        EXPECTED: User should be able to see that meeting panel at top within the Country panel
        EXPECTED: Example:page refresh at 2:50 . (following order should display in panel)
        EXPECTED: Meeting 3: 03:00. 03:30, 04:00,…
        EXPECTED: Meeting 1: 13:00, 13:30, 14:00,...
        EXPECTED: Meeting 2: 08:00. 08:30, 09:00,…
        EXPECTED: Meeting 4: 11:00, 11:30. 12:00,…
        """
        pass
