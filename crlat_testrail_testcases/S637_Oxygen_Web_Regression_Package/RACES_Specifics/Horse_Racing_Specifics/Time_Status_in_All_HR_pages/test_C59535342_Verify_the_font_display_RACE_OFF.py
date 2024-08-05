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
class Test_C59535342_Verify_the_font_display_RACE_OFF(Common):
    """
    TR_ID: C59535342
    NAME: Verify the font display "RACE OFF"
    DESCRIPTION: Ladbrokes: Verify that "RACE OFF" is displayed in red color font with color code : #ff0000.
    DESCRIPTION: Coral: Verify that "RACE OFF" is displayed in Orange color font with color code : #f56b23.
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

    def test_004_validate_race_off_status_fontindexphpattachmentsget111160928indexphpattachmentsget111160929(self):
        """
        DESCRIPTION: Validate "RACE OFF" status font
        DESCRIPTION: ![](index.php?/attachments/get/111160928)
        DESCRIPTION: ![](index.php?/attachments/get/111160929)
        EXPECTED: Ladbrokes:
        EXPECTED: 1: User should be displayed with "RACE OFF" status.
        EXPECTED: 2: "RACE OFF" status should be displayed in red color font with color code : #ff0000.
        EXPECTED: Coral:
        EXPECTED: 1: User should be displayed with "RACE OFF" status.
        EXPECTED: 2: "RACE OFF" status should be displayed in orange color font with color code : #f56b23.
        """
        pass
