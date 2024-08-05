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
class Test_C492715_Verify_Market_Selector_dropdown_list_on_Football_Coupon_Details_page(Common):
    """
    TR_ID: C492715
    NAME: Verify 'Market Selector' dropdown list on Football Coupon Details page
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Football Coupon Details page
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Coupons' tab
    PRECONDITIONS: 3. Choose some Football Coupon and navigates to 'Coupons' details page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3**
    PRECONDITIONS: * |Over/Under Total Goals| - "Total Goals Over/Under 1.5"
    PRECONDITIONS: * |Over/Under Total Goals| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Over/Under Total Goals| - "Total Goals Over/Under 3.5"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: * |To Win to Nil| - "To Win To Nil"
    PRECONDITIONS: * |Score Goal in Both Halves| - "Goal in Both Halves"
    PRECONDITIONS: 2) In order to get information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: * The 'Market Selector' is displayed below the Coupon sub-header and above the First accordion on the page
        EXPECTED: * 'Match Result' is selected by default in 'Market Selector' dropdown list
        """
        pass

    def test_002_verify_options_presence_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify options presence in the 'Market Selector' dropdown list
        EXPECTED: The following markets are shown in the Market selector dropdown in the order listed below:
        EXPECTED: * Match Result
        EXPECTED: * Both Teams to Score
        EXPECTED: * Match Result & Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Total Goals Over/ Under 1.5
        EXPECTED: * Total Goals Over/ Under 2.5
        EXPECTED: * Total Goals Over/ Under 3.5
        EXPECTED: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        EXPECTED: * To Win To Nil
        EXPECTED: * Goal in Both Halves
        EXPECTED: **Note:** If any Market is not available it is skipped in the Market selector dropdown list. Also, the order can be configured in CMS
        """
        pass

    def test_003_select_match_results_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Select 'Match Results' in the Market selector drop down
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_004_repeat_the_previous_step_for_the_next_markets_both_teams_to_score_match_result__both_teams_to_score_ladbrokes_added_from_ox_1003_total_goals_over_under_15_total_goals_over_under_25_total_goals_over_under_35_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_draw_no_bet_1st_half_result_to_win_to_nil_goal_in_both_halves(self):
        """
        DESCRIPTION: Repeat the previous step for the next markets:
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * Match Result & Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: * Total Goals Over/ Under 1.5
        DESCRIPTION: * Total Goals Over/ Under 2.5
        DESCRIPTION: * Total Goals Over/ Under 3.5
        DESCRIPTION: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        DESCRIPTION: * To Win To Nil
        DESCRIPTION: * Goal in Both Halves
        EXPECTED: 
        """
        pass

    def test_005_verify_bet_placement_for_single_and_multiple_bets_for_the_below_markets_match_result_both_teams_to_score_match_result__both_teams_to_score_ladbrokes_added_from_ox_1003_total_goals_over_under_15_total_goals_over_under_25_total_goals_over_under_35_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_draw_no_bet_1st_half_result_to_win_to_nil_goal_in_both_halves(self):
        """
        DESCRIPTION: Verify Bet Placement for Single and multiple Bets for the below markets
        DESCRIPTION: * Match Result
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * Match Result & Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: * Total Goals Over/ Under 1.5
        DESCRIPTION: * Total Goals Over/ Under 2.5
        DESCRIPTION: * Total Goals Over/ Under 3.5
        DESCRIPTION: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        DESCRIPTION: * To Win To Nil
        DESCRIPTION: * Goal in Both Halves
        EXPECTED: Bet should be placed successfully
        """
        pass
