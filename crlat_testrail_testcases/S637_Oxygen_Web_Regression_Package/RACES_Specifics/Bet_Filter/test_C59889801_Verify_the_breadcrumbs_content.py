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
class Test_C59889801_Verify_the_breadcrumbs_content(Common):
    """
    TR_ID: C59889801
    NAME: Verify the breadcrumbs content
    DESCRIPTION: Verify that Bet Filter is displayed to the right corner inside the breadcrumbs content.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral App
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

    def test_004_validate_breadcrumbs_contentindexphpattachmentsget118703005indexphpattachmentsget118703006(self):
        """
        DESCRIPTION: Validate breadcrumbs content
        DESCRIPTION: ![](index.php?/attachments/get/118703005)
        DESCRIPTION: ![](index.php?/attachments/get/118703006)
        EXPECTED: User should be displayed "Bet Filter" to the right corner
        """
        pass
