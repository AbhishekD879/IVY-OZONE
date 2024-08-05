import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C145822_Verify_SiteServer_call_for_the_Football_Market_Selector_on_Landing_page(Common):
    """
    TR_ID: C145822
    NAME: Verify SiteServer call for the Football Market Selector on Landing page
    DESCRIPTION: This test case verifies that SiteServer call "simpleFilter=market.templateMarketName" is using instead of the "simpleFilter=market.name".
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_network___all___headers_and_find_simplefiltermarkettemplatemarketname_in_ss_request(self):
        """
        DESCRIPTION: Go to Network -> All -> **Headers** and find 'simpleFilter=market.templateMarketName' in SS request
        EXPECTED: The following values are displayed in the SS request to get the list of particular markets:
        EXPECTED: * Match Betting
        EXPECTED: * To Qualify
        EXPECTED: * Over/Under Total Goals
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * First-Half Result
        """
        pass

    def test_002_go_to_network___all___preview_and_find_templatemarketname_attribute_for_different_markets_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName attribute' for different markets in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * Match Betting
        EXPECTED: * To Qualify
        EXPECTED: * Over/Under Total Goals
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * First-Half Result
        """
        pass

    def test_003_verify_options_available_for_football_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify options available for Football in the 'Market selector' dropdown list
        EXPECTED: The following options are displayed in the Market selector dropdown list:
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        """
        pass
