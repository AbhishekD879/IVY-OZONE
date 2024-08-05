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
class Test_C1952655_Verify_Primary_markets_change_for_Hero_Module(Common):
    """
    TR_ID: C1952655
    NAME: Verify Primary markets change for Hero Module
    DESCRIPTION: This test case verifies Primary markets change for Hero Module on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up with Live Events ONLY in CMS
    PRECONDITIONS: * In order to check data open Dev Tools -> Network -> WS -> select request to InPlay MS 'wss://{domain}/websocket/?EIO=3&transport=websocket' -> Frames
    PRECONDITIONS: * Order of markets is the next:
    PRECONDITIONS: - 1 - Match Betting/Match Result (market template: |Match Betting|)
    PRECONDITIONS: - 2 - Extra-Time Result (market template: |Extra-Time Result|)
    PRECONDITIONS: - 3 - Penalty Shoot-Out Winner (market template: |Penalty Shoot-Out Winner|)
    PRECONDITIONS: - 4 - To Qualify (market template: |To Qualify|)
    PRECONDITIONS: - 5 - To Lift the trophy (market template: |To Qualify|)
    PRECONDITIONS: - 6 - To finish 3rd (market template: |To Qualify|)
    PRECONDITIONS: - 7 - To reach the final (market template: |To Qualify|)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_hero_module_next_events_module_for_live_events___event_with_live_score_available(self):
        """
        DESCRIPTION: Go to Hero Module (Next Events Module for Live Events) -> event with Live Score available
        EXPECTED: Event with Live Score is present within Hero Module
        """
        pass

    def test_004_verify_primary_market_for_event_with_live_scores(self):
        """
        DESCRIPTION: Verify primary market for event with Live Scores
        EXPECTED: * 'Match Betting'/'Match Result' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'Match Betting'/'Match Result' market
        EXPECTED: * Primary market with template **'Match Betting'** is received in **markets** array from GET
        EXPECTED: "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_005_go_to_openbet_ti_tool_and_undisplay_match_bettingmatch_result_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'Match Betting'/'Match Result' primary market
        EXPECTED: 
        """
        pass

    def test_006_verify_hero_module(self):
        """
        DESCRIPTION: Verify Hero Module
        EXPECTED: Event with primary market 'Match Betting'/'Match Result' disappears from Hero Module immediately
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Event is displayed on Hero Module
        EXPECTED: * 'Extra-Time Result' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'Extra-Time Result' market
        EXPECTED: * Primary market with template **'Extra-Time Result'** is received in **markets** array from GET "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_008_go_to_openbet_ti_tool_and_undisplay_extra_time_result_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'Extra-Time Result' primary market
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: * Event is displayed on Hero Module
        EXPECTED: * 'Penalty Shoot-Out Winner' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'Penalty Shoot-Out Winner' market
        EXPECTED: * Primary market with template **'Penalty Shoot-Out Winner'** is received in **markets** array from GET "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_010_go_to_openbet_ti_tool_and_undisplay_penalty_shoot_out_winner_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'Penalty Shoot-Out Winner' primary market
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: * Event is displayed on Hero Module
        EXPECTED: * 'To Qualify' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'To Qualify' market
        EXPECTED: * Primary market with template **'To Qualify'** is received in **markets** array from GET "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_012_go_to_openbet_ti_tool_and_undisplay_to_qualify_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'To Qualify' primary market
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: * Event is displayed on Hero Module
        EXPECTED: * 'To Lift the trophy' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'To Lift the trophy' market
        EXPECTED: * Primary market with template **'To Qualify'** is received in **markets** array from GET "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_014_go_to_openbet_ti_tool_and_undisplay_to_lift_the_trophy_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'To Lift the trophy' primary market
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: * Event is displayed on Hero Module
        EXPECTED: * 'To finish 3rd' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'To finish 3rd' primary market market
        EXPECTED: * Primary market with template **'To Qualify'** is received in **markets** array from GET "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_016_go_to_openbet_ti_tool_and_undisplay_to_finish_3rd_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'To finish 3rd' primary market
        EXPECTED: 
        """
        pass

    def test_017_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps #6-7
        EXPECTED: * Event is displayed on Hero Module
        EXPECTED: * 'To reach the final' label is displayed above Price Odds
        EXPECTED: * Price Odds belongs to 'To reach the final' market
        EXPECTED: * Primary market with template **'To Qualify'** is received in **markets** array from GET "IN_PLAY_SPORT_TYPE" response in WS
        """
        pass

    def test_018_go_to_openbet_ti_tool_and_undisplay_to_reach_the_final_primary_market(self):
        """
        DESCRIPTION: Go to Openbet TI tool and undisplay 'To reach the final' primary market
        EXPECTED: 
        """
        pass

    def test_019_repeat_steps_6(self):
        """
        DESCRIPTION: Repeat steps #6
        EXPECTED: 
        """
        pass
