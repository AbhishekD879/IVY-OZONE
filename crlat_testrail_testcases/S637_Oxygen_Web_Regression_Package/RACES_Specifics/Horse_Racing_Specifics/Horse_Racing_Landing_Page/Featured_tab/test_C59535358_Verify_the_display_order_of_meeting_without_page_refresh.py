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
class Test_C59535358_Verify_the_display_order_of_meeting_without_page_refresh(Common):
    """
    TR_ID: C59535358
    NAME: Verify the display order of meeting without page refresh
    DESCRIPTION: Verify that Meeting does not display at top within the Country panel if the User does not refresh the page
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

    def test_004_do_not_fresh_the_page_in_10_minutes_window(self):
        """
        DESCRIPTION: Do not fresh the page in 10 minutes window
        EXPECTED: 
        """
        pass

    def test_005_verify_the_meeting_within_the_country_panel_does_not_raise_above_when_user_does_not_refresh_pageexamplemeeting_1_1300_1330_1400meeting_2_0800_0830_0900meeting_3_0300_0330_0400meeting_4_1100_1130_1200do_not_refresh_page(self):
        """
        DESCRIPTION: Verify the meeting within the Country panel does not raise above when User does not refresh page
        DESCRIPTION: Example:
        DESCRIPTION: Meeting 1: 13:00, 13:30, 14:00,...
        DESCRIPTION: Meeting 2: 08:00. 08:30, 09:00,...
        DESCRIPTION: Meeting 3: 03:00. 03:30, 04:00,...
        DESCRIPTION: Meeting 4: 11:00, 11:30. 12:00,…
        DESCRIPTION: DO NOT REFRESH PAGE
        EXPECTED: User should be able to see no change in the display order of Meetings within Country panels
        EXPECTED: Example:
        EXPECTED: Meeting 1: 13:00, 13:30, 14:00,...
        EXPECTED: Meeting 2: 08:00. 08:30, 09:00,...
        EXPECTED: Meeting 3: 03:00. 03:30, 04:00,...
        EXPECTED: Meeting 4: 11:00, 11:30. 12:00,…
        """
        pass
