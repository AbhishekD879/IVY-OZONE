import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60079218_Verify_event_displaying_when_market_name_differs_from_the_template_market_name_on_Football_Landing_Page(Common):
    """
    TR_ID: C60079218
    NAME: Verify event displaying when market name differs from the template market name on  Football Landing Page
    DESCRIPTION: This test case verifies event displaying when the market name differs from the template market name on  Football Landing Page
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

    def test_001_in_the_ob_system_add_market_for_the_event_where_the_market_name_differs_from_templatemarketnamestart_for_example_from_templatemarketname__both_teams_to_score_and_name__name_is_not_both_teams_to_score(self):
        """
        DESCRIPTION: In the OB system add market for the event where the market name differs from 'templateMarketName'
        DESCRIPTION: (start, for example, from 'templateMarketName' = 'Both Teams to Score' and name = 'name is NOT Both Teams to Score')
        EXPECTED: Market is added successfully
        """
        pass

    def test_002_back_to_the_app_refresh_the_page_and_check_if_both_teams_to_score_option_is_available_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Back to the app, refresh the page and check if 'Both Teams to Score' option is available in the 'Market Selector' dropdown list
        EXPECTED: 'Both Teams to Score' option is present in the 'Market Selector' dropdown list
        """
        pass

    def test_003_go_to_network___all___preview_and_compare_name_and_templatemarketname_attribute_in_ss_response_for_particular_market(self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and compare 'name' and 'templateMarketName' attribute in SS response for particular market
        EXPECTED: 'name' value differs from 'templateMarketName' = Both Teams to Score
        """
        pass

    def test_004_verify_if_both_teams_to_score_option_presents_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify if 'Both Teams to Score' option presents in the 'Market Selector' dropdown list
        EXPECTED: 'Both Teams to Score' option is displayed in the 'Market Selector' dropdown list
        """
        pass

    def test_005_select_both_teams_to_score_option_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Both Teams to Score' option in the 'Market Selector' dropdown list
        EXPECTED: * Event for the selected market is shown
        EXPECTED: * Values on Odds Card Header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_006_repeat_steps_1_5_for_the_following_markets_match_betting_to_qualify_total_goals_overunder_match_result_and_both_teams_to_score_draw_no_bet_first_half_result(self):
        """
        DESCRIPTION: Repeat steps 1-5 for the following markets:
        DESCRIPTION: * Match Betting
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Total Goals Over/Under
        DESCRIPTION: * Match Result and Both Teams To Score
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * First-Half Result
        EXPECTED: 
        """
        pass
