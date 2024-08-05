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
class Test_C59535339_Verify_Race_Start_Time(Common):
    """
    TR_ID: C59535339
    NAME: Verify Race Start Time
    DESCRIPTION: Verify that User is able to view Race start time for all the races at that meeting point.
    PRECONDITIONS: Horse racing event should be available
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

    def test_004_validate_race_time_of_start(self):
        """
        DESCRIPTION: Validate race time of start
        EXPECTED: User should be able view the race times displayed for all the meeting places
        EXPECTED: Example:
        EXPECTED: New Castle
        EXPECTED: 19:40 19:50
        """
        pass
