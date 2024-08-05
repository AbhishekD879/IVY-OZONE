import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C59486916_Coral_Verify_Horse_panel_in_Next_races_tab(Common):
    """
    TR_ID: C59486916
    NAME: Coral: Verify Horse panel in Next races tab
    DESCRIPTION: Verify that when user clicks on Horse panel ( Not on the Prices), User is navigated to full race card( Event details page)
    PRECONDITIONS: 1: Horse racing event should be available in Next races tab
    PRECONDITIONS: 2: Next races tab should be enabled in CMS
    PRECONDITIONS: CMS Configuration
    PRECONDITIONS: 1: System configuration > Structure > Next races toggle
    PRECONDITIONS: 2: System configuration > Structure > Next races
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

    def test_002_ladbrokesclick_on_horse_racing_from_sports_ribbon_or_from_menucoralnavigate_to_home_page(self):
        """
        DESCRIPTION: Ladbrokes:
        DESCRIPTION: Click on Horse racing from sports ribbon or from Menu
        DESCRIPTION: Coral:
        DESCRIPTION: Navigate to Home page
        EXPECTED: Ladbrokes:
        EXPECTED: User should be navigated to Horse racing Landing page
        EXPECTED: Coral:
        EXPECTED: User should be able to see Next races tab in home page
        """
        pass

    def test_003_click_on_next_races_tab(self):
        """
        DESCRIPTION: Click on 'Next Races' Tab
        EXPECTED: 1: User should be able to to navigate to Next races tab
        EXPECTED: 2: Horse race events which starts in next 45 mins should be displayed
        EXPECTED: 3: The following should displayed
        EXPECTED: 1:Event Time
        EXPECTED: 2:Meeting name
        EXPECTED: 3:countdown timer
        EXPECTED: 4:'SEE ALL' links in event header
        """
        pass

    def test_004_click_on_horse_panel_not_on_prices(self):
        """
        DESCRIPTION: Click on Horse panel (Not on Prices)
        EXPECTED: 1: User should be able to click anywhere on Horse panel
        EXPECTED: 2: User should be navigated to Full race card (Event details page)
        """
        pass
