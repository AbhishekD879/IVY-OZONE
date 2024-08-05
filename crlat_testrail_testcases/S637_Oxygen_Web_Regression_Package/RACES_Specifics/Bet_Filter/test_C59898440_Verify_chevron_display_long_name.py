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
class Test_C59898440_Verify_chevron_display_long_name(Common):
    """
    TR_ID: C59898440
    NAME: Verify chevron display-long name
    DESCRIPTION: Verify that chevron is not hidden if there is a long name and is displayed as ellipses "..." before the chevron and also there is always minimum of 12px between bet filter and the chevron.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bet Filter should be enabled in CMS
    PRECONDITIONS: 3: Long Course name
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

    def test_003_click_on_race_which_has_a_long_course_name(self):
        """
        DESCRIPTION: Click on race which has a long course name
        EXPECTED: User should be navigated to the Event details page
        """
        pass

    def test_004_validate_breadcrumbs_contentindexphpattachmentsget118934682indexphpattachmentsget118934683(self):
        """
        DESCRIPTION: Validate breadcrumbs content
        DESCRIPTION: ![](index.php?/attachments/get/118934682)
        DESCRIPTION: ![](index.php?/attachments/get/118934683)
        EXPECTED: 1: User should be displayed "Bet Filter" to the right corner
        EXPECTED: 2: Chevron should not be hidden
        EXPECTED: 3: Ellipses "...." should be displayed before the Chevron when there is a long name
        EXPECTED: 4: 12 px should be there between the Chevron and betfilter
        """
        pass
