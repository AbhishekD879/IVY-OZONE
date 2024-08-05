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
class Test_C1901953_Tracking_of_Main_Player_Bets_InPlay_Market_Accordion_Names(Common):
    """
    TR_ID: C1901953
    NAME: Tracking of Main Player Bets InPlay Market Accordion (Names)
    DESCRIPTION: This Test Case verifies tracking in the Google Analytics data Layer of Main Player Bets InPlay Market Accordion.
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Featured tab is opened
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
        EXPECTED: -  - '#YourCall Player Markets' section is displayed
        """
        pass

    def test_004_expandcollapse_main_player_bets_inplay_market_accordion__yourcall_player_markets(self):
        """
        DESCRIPTION: Expand/Collapse Main Player Bets InPlay Market Accordion ( '#YourCall Player Markets')
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'ds in play player stat',
        EXPECTED: 'eventLabel' : '<< ACTION >>' //e.g. expand accordion - shots, collapse accordion - shots, expand accordion - shots on goal, etc.
        EXPECTED: })
        """
        pass
