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
class Test_C59535346_Verify_icon_for_RESULT(Common):
    """
    TR_ID: C59535346
    NAME: Verify icon for "RESULT"
    DESCRIPTION: Verify that icon is displayed before the "RESULT" text
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

    def test_003_click_on_any_result_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any "RESULT" race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        pass

    def test_004_validate_icon_for_result_statusindexphpattachmentsget111160935indexphpattachmentsget111160936(self):
        """
        DESCRIPTION: Validate icon for "RESULT" status
        DESCRIPTION: ![](index.php?/attachments/get/111160935)
        DESCRIPTION: ![](index.php?/attachments/get/111160936)
        EXPECTED: Ladbrokes:
        EXPECTED: 1: User should be displayed icon before the status
        EXPECTED: 2: CSS
        EXPECTED: .Oval-2 {
        EXPECTED: width: 4px;
        EXPECTED: height: 4px;
        EXPECTED: border: solid 1px #000000;
        EXPECTED: }
        EXPECTED: Coral:
        EXPECTED: 1: User should be displayed icon before the status
        EXPECTED: 2: CSS
        EXPECTED: .Mask {
        EXPECTED: width: 375px;
        EXPECTED: height: 70px;
        EXPECTED: background-color: #f9fafe;
        EXPECTED: }
        """
        pass
