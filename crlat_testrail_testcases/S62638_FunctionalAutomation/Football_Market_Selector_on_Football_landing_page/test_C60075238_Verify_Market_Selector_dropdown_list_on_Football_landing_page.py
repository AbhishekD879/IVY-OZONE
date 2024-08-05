import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60075238_Verify_Market_Selector_dropdown_list_on_Football_landing_page(Common):
    """
    TR_ID: C60075238
    NAME: Verify 'Market Selector' dropdown list on Football landing page
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on the Football landing page
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

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match result' in 'Market selector' **Coral**
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • To Qualify
        EXPECTED: • Total Goals Over/Under 2.5
        EXPECTED: • Both Teams to Score
        EXPECTED: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: • Draw No Bet
        EXPECTED: • 1st Half Result
        EXPECTED: **Note:**
        EXPECTED: *If any Market is not available it is skipped in the Market selector drop down list*
        """
        pass

    def test_003_select_match_results_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Results' in the 'Market Selector' dropdown list
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_004_repeat_step_3_for_the_following_markets_to_qualify_total_goals_overunder_25_both_teams_to_score_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED: 
        """
        pass

    def test_005_select_any_other_sport_not_football_from_the_sports_menu_and_verify_availability_of_market_selector(self):
        """
        DESCRIPTION: Select any other Sport (not Football) from the Sports menu and verify availability of 'Market Selector'
        EXPECTED: The 'Market Selector' is NOT available
        """
        pass
