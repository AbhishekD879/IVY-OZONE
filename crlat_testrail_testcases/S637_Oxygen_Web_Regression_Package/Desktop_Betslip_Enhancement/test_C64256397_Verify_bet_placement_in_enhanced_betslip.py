import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C64256397_Verify_bet_placement_in_enhanced_betslip(Common):
    """
    TR_ID: C64256397
    NAME: Verify bet placement in enhanced betslip
    DESCRIPTION: Verify bet placement in enhanced betslip
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_the_application__navigate_to_any_sport_eg_football_hr(self):
        """
        DESCRIPTION: Load the application & navigate to any sport e.g., Football, HR
        EXPECTED: * Front End application is loaded.
        EXPECTED: * SLP is displayed.
        """
        pass

    def test_002_click_on_any_event_in_slp(self):
        """
        DESCRIPTION: Click on any event in SLP
        EXPECTED: * Navigated to EDP page & able to see multiple markets
        """
        pass

    def test_003_place_bet_by_adding_four_selections_from_same_market_eg_price_boost(self):
        """
        DESCRIPTION: Place bet by adding four selections from same market e.g., Price Boost
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_004_reuse_step_3_selections_add_fifth_selection_from_same_market_eg_price_boost_then_place_bet(self):
        """
        DESCRIPTION: Reuse step-3 selections add fifth selection from same market e.g., Price Boost then place bet.
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar is displayed in the FE with the previous selections betslip size.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_005_place_bet_by_adding_four_selections_one_on_one_from_different_markets_eg_price_boost_getaprice_outright(self):
        """
        DESCRIPTION: Place bet by adding four selections one on one from different markets e.g., Price Boost, GetAPrice, Outright
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_006_reuse_step_5_selections__add_fifth_selection_from_different_market_eg_price_boost_getaprice_outright(self):
        """
        DESCRIPTION: Reuse step-5 selections & add fifth selection from different market e.g., Price Boost, GetAPrice, Outright
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar shows up in FE with the previous selections betslip size.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_007_place_bet_by_adding_four_selections_one_on_one_from_different_events__gt_same_market_eg_match_result(self):
        """
        DESCRIPTION: Place bet by adding four selections one on one from different events -&gt; same market e.g., Match Result
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_008_reuse_step_7_selections__add_fifth_selection_from_different_events__gt_same_market_eg_match_result(self):
        """
        DESCRIPTION: Reuse step-7 selections & add fifth selection from different events -&gt; same market e.g., Match Result
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar is displayed with the previous selections betslip size.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_009_place_bet_by_adding_four_selections_one_on_one_from_different_events__gt_different_markets_eg_match_result_both_teams_to_score_draw_no_bet(self):
        """
        DESCRIPTION: Place bet by adding four selections one on one from different events -&gt; different markets e.g., Match Result, Both Teams to Score, Draw No Bet
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass

    def test_010_reuse_step_9_selections__add_fifth_selection_from_different_events__gt_different_markets_eg_match_result_both_teams_to_score_draw_no_bet(self):
        """
        DESCRIPTION: Reuse step-9 selections & add fifth selection from different events -&gt; different markets e.g., Match Result, Both Teams to Score, Draw No Bet
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar is displayed with the previous selections betslip size.
        EXPECTED: * Bet is placed successfully & betslip is expanded without scroll bar.
        """
        pass
