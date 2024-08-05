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
class Test_C1391532_Tracking_of_adding_a_selection_Bet_from_any_Build_Your_Bet_Market(Common):
    """
    TR_ID: C1391532
    NAME: Tracking of adding a selection/Bet from any Build Your Bet Market
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Adding a selection/Bet from any Build Your Bet Market on EDP
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Navigate to Football Landing page
    PRECONDITIONS: 4. Go to the Event details page with the BYB (Leagues with available BYB are marked with BYB icon on accordion) > 'Build Your Bet' tab
    """
    keep_browser_open = True

    def test_001_add_a_selections_bet_from_any_player_markets_accordion_to_the_byb_dashboard(self):
        """
        DESCRIPTION: Add a selection(s) (bet) from any Player Markets accordion to the BYB Dashboard
        EXPECTED: The selection(s) (bet) is added to BYB Dashboard
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'select player bet',
        EXPECTED: 'playerName' : '<< PLAYER NAME >>'
        EXPECTED: 'playerStat' : '<< STATISTIC NAME >>',
        EXPECTED: 'playerStatNum' : '<< STATISTIC NUMBER >>'
        EXPECTED: })
        """
        pass

    def test_003_add_a_selections_bet_from_any__match_markets__accordion_to_the_byb_dashboard(self):
        """
        DESCRIPTION: Add a selection(s) (bet) from any  Match Markets  accordion to the BYB Dashboard
        EXPECTED: The selection(s) (bet) is added to BYB Dashboard
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'match bet',
        EXPECTED: 'sportName' : '<< SPORT NAME >>',
        EXPECTED: 'eventName' : '<< EVENT NAME >>',
        EXPECTED: 'eventID' : '<< EVENT ID >>'
        EXPECTED: })
        """
        pass
