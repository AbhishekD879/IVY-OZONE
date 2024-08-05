import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C59486917_Verify_adding_selection_to_Bet_slip_from_Next_races_tab(Common):
    """
    TR_ID: C59486917
    NAME: Verify adding selection to Bet slip from Next races tab
    DESCRIPTION: Verify that User is able to add selections to Bet slip from races displayed in the Next races tab
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
        EXPECTED: Click on Horse racing from sports ribbon or from Menu
        EXPECTED: Coral:
        EXPECTED: Navigate to Home page
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

    def test_004_click_on_any_selection_odd_price(self):
        """
        DESCRIPTION: Click on any Selection Odd (Price)
        EXPECTED: 1: User should be able to add the selection to Bet slip
        EXPECTED: 2: If it is the first selection user made, Quick Bet should be displayed else the counter displayed at the Bet slip should be increased by one
        """
        pass
