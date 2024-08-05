import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094795_Verify_the_time_period_for_display_of_RACE_OFF(Common):
    """
    TR_ID: C60094795
    NAME: Verify the time period for display of "RACE OFF"
    DESCRIPTION: Verify the "RACE OFF" status label is displayed until the result is available for race event.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should kick start
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

    def test_003_click_on_any_race_off_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any "RACE OFF" race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        pass

    def test_004_validate_race_off_time_period(self):
        """
        DESCRIPTION: Validate "RACE OFF" time period
        EXPECTED: 1: User should be displayed with "RACE OFF" status
        EXPECTED: 2: "RACE OFF" status should be displayed until the result is available for race event
        """
        pass
