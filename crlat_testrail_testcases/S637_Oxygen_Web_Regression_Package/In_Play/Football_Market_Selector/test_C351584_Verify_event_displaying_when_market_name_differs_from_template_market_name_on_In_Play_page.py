import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C351584_Verify_event_displaying_when_market_name_differs_from_template_market_name_on_In_Play_page(Common):
    """
    TR_ID: C351584
    NAME: Verify event displaying when market name differs from template market name on 'In-Play' page
    DESCRIPTION: This test case verifies event displaying when the market name differs from the template market name on 'In-Play' page
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
    PRECONDITIONS: 4) To check the availability of selected market in 'Market Selector' from dropdown list use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::{templateMarketName}::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Category ID
    PRECONDITIONS: XXX - Type ID
    PRECONDITIONS: ![](index.php?/attachments/get/18576729)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    """
    keep_browser_open = True

    def test_001_in_the_ob_system_add_market_for_the_event_where_market_name_is_different_than_templatemarketnamestart_for_example_from_templatemarketname__both_teams_to_score_and_name__name_is_not_both_teams_to_score(self):
        """
        DESCRIPTION: In the OB system add market for the event where market name is different than templateMarketName
        DESCRIPTION: (start, for example, from templateMarketName = 'Both Teams to Score' and name = 'name is NOT Both Teams to Score')
        EXPECTED: Market is added successfully
        """
        pass

    def test_002_back_to_the_app_refresh_the_page_and_check_if_both_teams_to_score_option_is_available_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Back to the app, refresh the page and check if 'Both Teams to Score' option is available in the 'Market Selector' dropdown list
        EXPECTED: 'Both Teams to Score' option is present in the 'Market Selector' dropdown list
        """
        pass

    def test_003_select_the_both_teams_to_score_option_from_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select the 'Both Teams to Score' option from the 'Market Selector' dropdown list
        EXPECTED: * Event for the selected market is shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: * 'name' value is different from 'templateMarketName' = 'Both Teams to Score' in the response
        EXPECTED: ![](index.php?/attachments/get/18576736)
        """
        pass

    def test_004_repeat_steps_1_3_for_the_following_markets_match_result_next_team_to_score_both_teams_to_score_match_result__both_teams_to_score_total_goals_overunder_15_total_goals_overunder_25_total_goals_overunder_35_total_goals_overunder_45_to_qualify_penalty_shoot_out_winner_extra_time_result_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Repeat steps 1-3 for the following markets:
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
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_1_4_on_football_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 on 'Football Landing Page' -> 'In-Play' tab
        EXPECTED: 
        """
        pass
