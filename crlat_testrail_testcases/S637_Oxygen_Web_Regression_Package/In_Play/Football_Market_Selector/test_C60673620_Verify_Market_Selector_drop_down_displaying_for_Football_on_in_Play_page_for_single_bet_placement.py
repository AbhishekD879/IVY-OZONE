import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C60673620_Verify_Market_Selector_drop_down_displaying_for_Football_on_in_Play_page_for_single_bet_placement(Common):
    """
    TR_ID: C60673620
    NAME: Verify 'Market Selector' drop down displaying for Football on in-Play page for single bet placement
    DESCRIPTION: This test case verifies 'Market Selector' drop down displaying for Football on in-Play page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following marketTemplates:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |Next Team to Score| - "Next Team to Score"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 1.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 3.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 4.5"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Penalty Shoot-Out Winner| - "Penalty Shoot-Out Winner"
    PRECONDITIONS: * |Extra-Time Result| - "Extra Time Result"
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    PRECONDITIONS: 3) To check the available options in 'Market Selector' use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::XX::LIVE_EVENT"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Category ID
    PRECONDITIONS: ![](index.php?/attachments/get/10272745)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **Mobile:**
        EXPECTED: * The 'Market Selector' is displayed below the 'Life Now (n)' header
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: **Desktop:**
        EXPECTED: * The 'Market Selector' is displayed below the 'Life Now' (n) switcher
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change Market' button is placed next to  'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: * 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        pass

    def test_002_click_on_the_changechange_marketmarket_button_to_verify_options_available_for_football_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on the 'Change'/'Change Market'/'Market' button to verify options available for Football in the Market selector dropdown
        EXPECTED: Market selector drop down becomes expanded (with chevron/arrow pointing upwards) with the options in the order listed below:
        EXPECTED: * Main Markets
        EXPECTED: * Match Result
        EXPECTED: * Next Team to Score
        EXPECTED: * Both Teams to Score
        EXPECTED: * Match Result & Both Teams To Score
        EXPECTED: * Total Goals Over/Under 1.5
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Total Goals Over/Under 3.5
        EXPECTED: * Total Goals Over/Under 4.5
        EXPECTED: * To Qualify
        EXPECTED: * Penalty Shoot-Out Winner
        EXPECTED: * Extra Time Result
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        EXPECTED: *If any Market is not available it is not displayed in the Market selector drop-down list*
        """
        pass

    def test_003_verify_bet_placement_for_single_selections_for_the_below_markets_match_result_next_team_to_score_both_teams_to_score_match_result__both_teams_to_score_total_goals_overunder_15_total_goals_overunder_25_total_goals_overunder_35_total_goals_overunder_45_to_qualify_penalty_shoot_out_winner_extra_time_result_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Verify Bet Placement for single selections for the below markets
        DESCRIPTION: * Match Result
        DESCRIPTION: * Next Team to Score
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * Match Result & Both Teams To Score
        DESCRIPTION: * Total Goals Over/Under 1.5
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Total Goals Over/Under 3.5
        DESCRIPTION: * Total Goals Over/Under 4.5
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Penalty Shoot-Out Winner
        DESCRIPTION: * Extra Time Result
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED: Bet should be placed successfully
        """
        pass
