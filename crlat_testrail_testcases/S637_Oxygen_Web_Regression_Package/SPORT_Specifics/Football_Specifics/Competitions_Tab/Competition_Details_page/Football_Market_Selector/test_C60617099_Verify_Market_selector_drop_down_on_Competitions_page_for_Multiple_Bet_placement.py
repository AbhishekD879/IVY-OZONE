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
class Test_C60617099_Verify_Market_selector_drop_down_on_Competitions_page_for_Multiple_Bet_placement(Common):
    """
    TR_ID: C60617099
    NAME: Verify Market selector drop down on Competitions page for Multiple Bet placement
    DESCRIPTION: This test case verifies Market selector drop down on Competitions page for Multiple Bet placement
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Go to Football Landing page
    PRECONDITIONS: 3. Click/Tap on Competition Module header
    PRECONDITIONS: 4. Click/Tap on sub-category (Class ID) with Type ID's
    PRECONDITIONS: 5. Choose Competition (Type ID)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3/Coral from OX 101.1**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3/Coral from OX 101.1**
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

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **For tablet/mobile:**
        EXPECTED: * ‘Market Selector’ is displayed below Competitions sub-tabs (Matches/Outrights/Results)
        EXPECTED: * 'Match Result' is selected by default in 'Market selector' drop down
        EXPECTED: * "Market:" is shown in front of <market name>
        EXPECTED: **For desktop:**
        EXPECTED: * ‘Market Selector’ is displayed next to Matches/Outrights Selector on the right side
        EXPECTED: * 'Match Result' is selected by default in 'Market Selector' drop down
        EXPECTED: * Up and down arrows (chevrons) are shown next to 'Match result' in 'Market Selector'
        """
        pass

    def test_002_verify_options_available_for_football_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify options available for Football in the Market selector drop down:
        EXPECTED: *The following markets are shown in the Market selector drop down in the order listed below:*
        EXPECTED: * Match Result
        EXPECTED: * To Qualify
        EXPECTED: * Next Team to Score
        EXPECTED: * Extra Time Result
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Both Teams to Score
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3/Coral from OX 101.1**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3/Coral from OX 101.1**
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        EXPECTED: *If any Market is not available it is skipped in the Market selector drop down list*
        """
        pass

    def test_003_verify_bet_placement_for_multiple_for_the_below_markets_match_result_to_qualify_next_team_to_score_extra_time_result_total_goals_overunder_25_both_teams_to_score_to_win_not_to_nil_ladbrokes_removed_from_ox_1003coral_from_ox_1011_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003coral_from_ox_1011_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Verify Bet Placement for multiple for the below markets
        DESCRIPTION: * Match Result
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Next Team to Score
        DESCRIPTION: * Extra Time Result
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * To Win Not to Nil **Ladbrokes removed from OX 100.3/Coral from OX 101.1**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3/Coral from OX 101.1**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED: Bet should be placed successfully
        """
        pass
