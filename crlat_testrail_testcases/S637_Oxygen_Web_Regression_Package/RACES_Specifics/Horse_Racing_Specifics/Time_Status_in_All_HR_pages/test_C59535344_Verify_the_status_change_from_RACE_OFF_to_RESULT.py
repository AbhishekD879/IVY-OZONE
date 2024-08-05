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
class Test_C59535344_Verify_the_status_change_from_RACE_OFF_to_RESULT(Common):
    """
    TR_ID: C59535344
    NAME: Verify the status change from "RACE OFF" to "RESULT"
    DESCRIPTION: Verify that when race is completed the "RACE OFF" status changes to "RESULT"
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should be completed
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

    def test_003_click_on_any_race_from_the_meeting_pointpick_a_race_off_race_event_and_wait_for_the_status_change(self):
        """
        DESCRIPTION: Click on any race from the meeting point
        DESCRIPTION: (Pick a RACE OFF race event and wait for the status change)
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        pass

    def test_004_validate_result_status(self):
        """
        DESCRIPTION: Validate "RESULT" status
        EXPECTED: 1: User should be displayed "RESULT" status.
        EXPECTED: 2: "RACE OFF" status should be Changed to "RESULT" status once the race has been completed
        """
        pass
