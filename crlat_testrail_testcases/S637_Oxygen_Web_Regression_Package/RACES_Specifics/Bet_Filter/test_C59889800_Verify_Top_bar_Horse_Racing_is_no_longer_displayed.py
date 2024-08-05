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
class Test_C59889800_Verify_Top_bar_Horse_Racing_is_no_longer_displayed(Common):
    """
    TR_ID: C59889800
    NAME: Verify Top bar "Horse Racing" is no longer displayed
    DESCRIPTION: Verify that Top bar "Horse Racing" is no longer displayed.
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

    def test_004_validate_top_barindexphpattachmentsget118703003indexphpattachmentsget118703004(self):
        """
        DESCRIPTION: Validate Top bar
        DESCRIPTION: ![](index.php?/attachments/get/118703003)
        DESCRIPTION: ![](index.php?/attachments/get/118703004)
        EXPECTED: User should not be displayed "Horse racing" top bar
        """
        pass
