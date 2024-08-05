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
class Test_C64256390_Verify_betslip_if_we_add_more_than_4_selections_from_same_event_different_events(Common):
    """
    TR_ID: C64256390
    NAME: Verify betslip if we add more than 4 selections from same event & different events.
    DESCRIPTION: Verify betslip if we add more than 4 selections from same event & different events.
    PRECONDITIONS: At least 5 preplay events should be available in Front End.
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

    def test_003_add_four_selections_one_on_one_from_same_market_eg_price_boost(self):
        """
        DESCRIPTION: Add four selections one on one from same market e.g., Price Boost
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_004_now_add_fifth_selection_from_same_market_eg_price_boost(self):
        """
        DESCRIPTION: Now add fifth selection from same market e.g., Price Boost
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar becomes available in the FE with the previous selections betslip size.
        """
        pass

    def test_005_add_four_selections_one_on_one_from_different_markets_eg_price_boost_getaprice_outright(self):
        """
        DESCRIPTION: Add four selections one on one from different markets e.g., Price Boost, GetAPrice, Outright
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_006_now_add_fifth_selection_from_different_market_eg_price_boost_getaprice_outright(self):
        """
        DESCRIPTION: Now add fifth selection from different market e.g., Price Boost, GetAPrice, Outright
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar shows up in the FE with the previous selections betslip size.
        """
        pass

    def test_007_add_four_selections_one_on_one_from_different_events__gt_same_market_eg_match_result(self):
        """
        DESCRIPTION: Add four selections one on one from different events -&gt; same market e.g., Match Result
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically along with 'multiples' without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_008_add_fifth_selection_from_different_event__gt_same_market_eg_match_result(self):
        """
        DESCRIPTION: Add fifth selection from different event -&gt; same market e.g., Match Result
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar shows up in the FE with the previous selections betslip size.
        """
        pass

    def test_009_add_four_selections_one_on_one_from_different_events__gt_different_markets_eg_match_result_both_teams_to_score_draw_no_bet(self):
        """
        DESCRIPTION: Add four selections one on one from different events -&gt; different markets e.g., Match Result, Both Teams to Score, Draw No Bet
        EXPECTED: * Four selections are added to betslip & betslip size is going to increase dynamically along with 'multiples' without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_010_add_fifth_selection_from_different_event__gt_different_markets_eg_match_result_both_teams_to_score_draw_no_bet(self):
        """
        DESCRIPTION: Add fifth selection from different event -&gt; different markets e.g., Match Result, Both Teams to Score, Draw No Bet
        EXPECTED: * Fifth selection is added to betslip.
        EXPECTED: * Scroll bar shows up in the FE with the previous selections betslip size.
        """
        pass
