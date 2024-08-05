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
class Test_C59535348_Verify_race_status_in_all_tabs(Common):
    """
    TR_ID: C59535348
    NAME: Verify race status in all tabs
    DESCRIPTION: Verify race status is displayed in the below tabs,
    DESCRIPTION: 1: Horse Racing Homepage (Featured Tab)
    DESCRIPTION: 2: Horse Racing EDP
    PRECONDITIONS: Multiple Horse racing events should be available with different race status as below
    PRECONDITIONS: 1: One race should Kick start
    PRECONDITIONS: 2: One race should be completed
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

    def test_003_validate_status(self):
        """
        DESCRIPTION: Validate Status
        EXPECTED: 1: User should be displayed "RACE OFF" status - when race kick started
        EXPECTED: 2: User should be displayed "RESULT" status - When race has been completed.
        """
        pass

    def test_004_click_on_the_race_and_navigate_to_the_races_for_that_meeting_point(self):
        """
        DESCRIPTION: Click on the race and navigate to the races for that meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        EXPECTED: 3: User should be displayed "RACE OFF" status - when race kick started
        EXPECTED: 4: User should be displayed "RESULT" status - When race has been completed.
        """
        pass
