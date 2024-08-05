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
class Test_C59535345_Verify_the_CSS_for_RESULT_status(Common):
    """
    TR_ID: C59535345
    NAME: Verify the CSS for "RESULT" status
    DESCRIPTION: Verify the CSS for "RESULT" status as mentioned in the design
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

    def test_004_validate_result_status_cssindexphpattachmentsget111160934indexphpattachmentsget111160933(self):
        """
        DESCRIPTION: Validate "RESULT" status CSS
        DESCRIPTION: ![](index.php?/attachments/get/111160934)
        DESCRIPTION: ![](index.php?/attachments/get/111160933)
        EXPECTED: Ladbrokes:
        EXPECTED: 1: User should be displayed "RESULT" status.
        EXPECTED: 2: CSS for "RESULT" should be as mentioned in the design
        EXPECTED: .RESULT {
        EXPECTED: width: 32px;
        EXPECTED: height: 13px;
        EXPECTED: font-family: Roboto;
        EXPECTED: font-size: 10px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: condensed;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: 0.3px;
        EXPECTED: color: #000000;
        EXPECTED: }
        EXPECTED: Coral:
        EXPECTED: CSS
        EXPECTED: .RESULT {
        EXPECTED: width: 33px;
        EXPECTED: height: 11px;
        EXPECTED: font-family: Lato;
        EXPECTED: font-size: 9px;
        EXPECTED: font-weight: normal;
        EXPECTED: font-stretch: normal;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: normal;
        EXPECTED: text-align: center;
        EXPECTED: color: #41494e;
        EXPECTED: }
        """
        pass
