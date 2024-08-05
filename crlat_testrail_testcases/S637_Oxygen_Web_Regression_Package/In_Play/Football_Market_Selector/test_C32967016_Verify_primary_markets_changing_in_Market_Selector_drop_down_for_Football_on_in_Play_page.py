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
class Test_C32967016_Verify_primary_markets_changing_in_Market_Selector_drop_down_for_Football_on_in_Play_page(Common):
    """
    TR_ID: C32967016
    NAME: Verify primary markets changing in 'Market Selector' drop down for Football on in-Play page
    DESCRIPTION: This test case verifies primary markets changing in 'Market Selector' drop down for Football on in-Play page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of primary markets should be created in OB system using the following marketTemplates:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |Extra-Time Result| - "Extra Time Result"
    PRECONDITIONS: * |Penalty Shoot-Out Winner| - "Penalty Shoot-Out Winner"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |To Qualify| - "To Lift the trophy"
    PRECONDITIONS: * |To Qualify| - "To finish 3rd"
    PRECONDITIONS: * |To Qualify| - "To reach the final"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    PRECONDITIONS: 3) To check what the primary market is available when selecting the 'Main Market 'in 'Market Selector' use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN-PLAY_SPORT_TYPE::XX::LIVE_EVENT::Main Market::XXX"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - category ID
    PRECONDITIONS: XXX - type ID
    PRECONDITIONS: ![](index.php?/attachments/get/10667811)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    PRECONDITIONS: 4. Make sure that 'Market Selector' is displayed below the 'Life Now (n)' header/switcher
    """
    keep_browser_open = True

    def test_001_clicktap_on_the_changechange_marketmarket_button_and_select_main_market_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click/Tap on the 'Change'/'Change Market'/'Market' button and select 'Main Market' in the 'Market Selector' dropdown
        EXPECTED: * The events of the 'Main Markets' are shown:
        EXPECTED: - Match Result
        EXPECTED: - Extra-Time Result
        EXPECTED: - Penalty Shoot-Out Winner
        EXPECTED: - To Qualify
        EXPECTED: - To Lift the trophy
        EXPECTED: - To finish 3rd
        EXPECTED: - To reach the final
        EXPECTED: * Corresponding Odds buttons of the selections are displayed under each market header (home/draw/away); 'draw' column is empty if market consists of 2 selections
        EXPECTED: * Events of not 'Main markets' (like Next Team to Score) are shown as outrights, without odds buttons.
        """
        pass

    def test_002_trigger_undisplaying_of_match_result_market_for_the_event_that_contains_a_set_of_other_primary_markets_from_preconditions(self):
        """
        DESCRIPTION: Trigger undisplaying of 'Match Result' market for the event that contains a set of other Primary markets from Preconditions
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_page_and_select_main_market_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Refresh the page and select 'Main Market' in the 'Market Selector' dropdown
        EXPECTED: * The event with the next available primary market by priority is shown in this case the "Extra Time Result"
        EXPECTED: * Values on Fixture header are changed for the event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: * Check available primary market for a particular event in WS according to Preconditions
        """
        pass

    def test_004_repeat_steps_2_3_for_the_next_items__extra_time_result__penalty_shoot_out_winner__to_qualify__to_lift_the_trophy__to_finish_3rd__to_reach_the_final(self):
        """
        DESCRIPTION: Repeat steps 2-3 for the next items:
        DESCRIPTION: - Extra-Time Result
        DESCRIPTION: - Penalty Shoot-Out Winner
        DESCRIPTION: - To Qualify
        DESCRIPTION: - To Lift the trophy
        DESCRIPTION: - To finish 3rd
        DESCRIPTION: - To reach the final
        EXPECTED: * The events for the available primary market are shown, for a particular case the event with the next available primary market by priority is shown (e.g. "Extra Time Result")
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: * Check available primary market for a particular event in WS according to Preconditions
        """
        pass

    def test_005_repeat_step_1_for_any_of_the_following_items_next_team_to_score_both_teams_to_score_match_result__both_teams_to_score_total_goals_overunder_15_total_goals_overunder_25_total_goals_overunder_35_total_goals_overunder_45_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Repeat step 1 for any of the following items:
        DESCRIPTION: * Next Team to Score
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * Match Result & Both Teams To Score
        DESCRIPTION: * Total Goals Over/Under 1.5
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Total Goals Over/Under 3.5
        DESCRIPTION: * Total Goals Over/Under 4.5
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED: Events of not 'Main markets' (like Next Team to Score) are shown as outrights, without odds buttons
        """
        pass

    def test_006_repeat_steps_1_5_on_football_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-5 on 'Football Landing Page' -> 'In-Play' tab
        EXPECTED: 
        """
        pass
