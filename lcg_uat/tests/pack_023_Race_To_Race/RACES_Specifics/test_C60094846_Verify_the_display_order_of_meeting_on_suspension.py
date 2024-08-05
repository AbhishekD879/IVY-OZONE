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
class Test_C60094846_Verify_the_display_order_of_meeting_on_suspension(Common):
    """
    TR_ID: C60094846
    NAME: Verify the display order of meeting on suspension
    DESCRIPTION: This Test case verifies the first race in a meeting is about to start in next 10 minutes was suspended within the specific Country panel
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

    def test_004_verify_if_the_meeting_is_suspended_which_us_about_to_start_in_10_minutes_or_suspend_the_meeting_from_ob(self):
        """
        DESCRIPTION: verify, if the meeting is suspended (Which us about to start in 10 minutes) or suspend the meeting from ob
        EXPECTED: meeting should be suspended
        """
        pass

    def test_005_refresh_the_page_in_the_active_window_within_10_minutes_of_start_time(self):
        """
        DESCRIPTION: Refresh the page in the ACTIVE window (within 10 minutes of start time)
        EXPECTED: User should be able to refresh the page
        """
        pass

    def test_006_verify_the_meeting_within_the_country_panel_unchangedexamplemeeting_1_1300_1330_1400meeting_2_0800_0830_0900meeting_3_0300_0330_0400meeting_4_1100_1130_1200after_page_refresh_at_250_and_meeting_3__at_0300_is_suspended(self):
        """
        DESCRIPTION: Verify the meeting within the Country panel unchanged
        DESCRIPTION: Example:
        DESCRIPTION: Meeting 1: 13:00, 13:30, 14:00,...
        DESCRIPTION: Meeting 2: 08:00. 08:30, 09:00,...
        DESCRIPTION: Meeting 3: 03:00. 03:30, 04:00,...
        DESCRIPTION: Meeting 4: 11:00, 11:30. 12:00,…
        DESCRIPTION: After page refresh at 2:50 and meeting 3 : at 03:00 is suspended
        EXPECTED: User should be able to see no change in meeting panel order within the Country panel
        EXPECTED: Example:
        EXPECTED: Meeting 1: 13:00, 13:30, 14:00,...
        EXPECTED: Meeting 2: 08:00. 08:30, 09:00,...
        EXPECTED: Meeting 3: 03:00. 03:30, 04:00,...
        EXPECTED: Meeting 4: 11:00, 11:30. 12:00,…
        """
        pass
