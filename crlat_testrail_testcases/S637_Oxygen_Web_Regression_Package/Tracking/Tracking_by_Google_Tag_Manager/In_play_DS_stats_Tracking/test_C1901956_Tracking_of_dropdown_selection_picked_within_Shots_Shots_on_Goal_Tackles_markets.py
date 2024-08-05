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
class Test_C1901956_Tracking_of_dropdown_selection_picked_within_Shots_Shots_on_Goal_Tackles_markets(Common):
    """
    TR_ID: C1901956
    NAME: Tracking of dropdown selection picked within Shots, Shots on Goal & Tackles markets
    DESCRIPTION: This Test Case verifies tracking in the Google Analytics data Layer of dropdown selection picked within Shots, Shots on Goal & Tackles markets.
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_inplay_and_select_event_with_available_player_markets(self):
        """
        DESCRIPTION: Navigate to InPlay and select Event with available Player Markets
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_select_all_markets_tab(self):
        """
        DESCRIPTION: Select All Markets tab
        EXPECTED: '#YourCall Player Markets' section is displayed
        """
        pass

    def test_004_select_player_market_with_numbers_dropdown_available_shots_shots_on_goal__tackles_markets(self):
        """
        DESCRIPTION: Select Player Market with 'Numbers' dropdown available (Shots, Shots on Goal & Tackles markets)
        EXPECTED: 
        """
        pass

    def test_005_select_dropdown_values_within_shots_shots_on_goal__tackles_markets(self):
        """
        DESCRIPTION: Select dropdown values within Shots, Shots on Goal & Tackles markets
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'ds in play player stat',
        EXPECTED: 'eventLabel' : 'update statistic',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>'
        EXPECTED: })
        """
        pass
