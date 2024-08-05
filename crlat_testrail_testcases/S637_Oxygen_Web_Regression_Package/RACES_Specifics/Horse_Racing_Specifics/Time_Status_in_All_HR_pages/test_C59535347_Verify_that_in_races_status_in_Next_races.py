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
class Test_C59535347_Verify_that_in_races_status_in_Next_races(Common):
    """
    TR_ID: C59535347
    NAME: Verify that in races status in Next races
    DESCRIPTION: Verify that in Next races tab no status should display as the tab contains only the future races.
    PRECONDITIONS: 1: Horse racing events should be available in Next races tab
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

    def test_003_click_on_any_race_from_next_races_tab(self):
        """
        DESCRIPTION: Click on any race from Next races tab
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other available races from Next race tab should be displayed
        """
        pass

    def test_004_validate_status(self):
        """
        DESCRIPTION: Validate Status
        EXPECTED: 1: User should not be able to view any status in Next races.
        """
        pass
