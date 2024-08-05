import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1901955_Tracking_of_clicks_on_Home_Away_Team_Switcher(Common):
    """
    TR_ID: C1901955
    NAME: Tracking of clicks on Home/Away Team Switcher
    DESCRIPTION: This Test Case verifies tracking of clicks on Home/Away Team Switcher in the Google Analytics data Layer.
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_inplay_and_select_event_with_configured_player_markets(self):
        """
        DESCRIPTION: Navigate to InPlay and select Event with configured Player Markets
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_select_all_markets_tab(self):
        """
        DESCRIPTION: Select All Markets tab
        EXPECTED: - All Markets tab is opened
        EXPECTED: - '#YourCall Player Markets' section is displayed
        EXPECTED: - Home/Away Team switcher is displayed beneath  '#YourCall Player Markets' accordion
        """
        pass

    def test_004_click_on_homeaway_team_switcher(self):
        """
        DESCRIPTION: Click on Home/Away Team Switcher
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'ds in play player stat',
        EXPECTED: 'eventLabel' : 'switch team - << TEAM NAME >>' //e.g. switch team - Germany
        EXPECTED: })
        """
        pass
