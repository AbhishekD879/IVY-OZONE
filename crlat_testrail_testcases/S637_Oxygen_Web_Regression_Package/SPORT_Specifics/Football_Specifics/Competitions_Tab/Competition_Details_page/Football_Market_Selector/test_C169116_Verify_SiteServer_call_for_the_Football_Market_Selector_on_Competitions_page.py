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
class Test_C169116_Verify_SiteServer_call_for_the_Football_Market_Selector_on_Competitions_page(Common):
    """
    TR_ID: C169116
    NAME: Verify SiteServer call for the Football Market Selector on Competitions page
    DESCRIPTION: This test case verifies SiteServer call for the Football Market Selector on Competitions page
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Go to Football Landing page
    PRECONDITIONS: 3. Click/Tap on Competition Module header
    PRECONDITIONS: 4. Click/Tap on sub-category (Class ID) with Type ID's
    PRECONDITIONS: 5. Choose Competition (Type ID)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |Total Goals Over/Under| (rawHandicapValue="2.5") - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: * |Next Team to Score| - "Next Team to Score"
    PRECONDITIONS: * |Extra-Time Result| - Extra Time Result
    """
    keep_browser_open = True

    def test_001_go_to_network__gt_all__gt_preview_and_find_templatemarketname_attribute_for_different_markets_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -&gt; All -&gt; **Preview** and find 'templateMarketName attribute' for different markets in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * Match Betting
        EXPECTED: * To Qualify
        EXPECTED: * Both Teams to Score
        EXPECTED: * Over/Under Total Goals (rawHandicapValue="2.5")
        EXPECTED: * Draw No Bet
        EXPECTED: * Match Result and Both Teams To Score
        EXPECTED: * First-Half Result
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra-Time Result
        """
        pass

    def test_002_verify_options_available_for_football_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify options available for Football in the 'Market Selector' dropdown list
        EXPECTED: The following options are displayed in the Market selector dropdown list:
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra Time Result
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * Match Result and Both Teams To Score
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        """
        pass
