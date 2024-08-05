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
class Test_C59535340_Verify_the_display_of_RACE_OFF(Common):
    """
    TR_ID: C59535340
    NAME: Verify the display of "RACE OFF"
    DESCRIPTION: Verify that when the Race kick starts "RACE OFF" status of the race is displayed just below the Time of start
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

    def test_003_click_on_any_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        pass

    def test_004_validate_race_off_status(self):
        """
        DESCRIPTION: Validate "RACE OFF" status
        EXPECTED: 1: User should be displayed with "RACE OFF" status
        EXPECTED: 2: "RACE OFF" status should be displayed just below the Race Start Time
        """
        pass
