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
class Test_C59889804_Verify_Back_button_in_Coral_app(Common):
    """
    TR_ID: C59889804
    NAME: Verify Back button in Coral app
    DESCRIPTION: Coral: Verify that back button is displayed inside the breadcrumbs area.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_coral_app(self):
        """
        DESCRIPTION: Launch Coral App
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

    def test_004_validate_back_buttonindexphpattachmentsget118703011(self):
        """
        DESCRIPTION: Validate Back button
        DESCRIPTION: ![](index.php?/attachments/get/118703011)
        EXPECTED: 1: User should be able to view the Back button in the breadcrumbs area
        EXPECTED: 2: User should be able to navigate to previous page on clicking back button
        """
        pass
