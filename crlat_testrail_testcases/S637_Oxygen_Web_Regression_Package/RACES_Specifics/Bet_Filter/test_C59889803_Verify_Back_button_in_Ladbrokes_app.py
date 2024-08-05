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
class Test_C59889803_Verify_Back_button_in_Ladbrokes_app(Common):
    """
    TR_ID: C59889803
    NAME: Verify Back button in Ladbrokes app
    DESCRIPTION: Ladbrokes: Verify that Back button is displayed in the navigation bar
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_app(self):
        """
        DESCRIPTION: Launch Ladbrokes App
        EXPECTED: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_click_on_any_race(self):
        """
        DESCRIPTION: Click on any race
        EXPECTED: User should be navigated to the Event details page
        """
        pass

    def test_004_validate_back_buttonindexphpattachmentsget118703010(self):
        """
        DESCRIPTION: Validate Back button
        DESCRIPTION: ![](index.php?/attachments/get/118703010)
        EXPECTED: 1: User should be able to view the Back button in the navigation bar
        EXPECTED: 2: User should be able to navigate to previous page on clicking back button
        """
        pass
