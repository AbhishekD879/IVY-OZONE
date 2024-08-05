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
class Test_C508513_Verify_event_displaying_when_market_name_differs_from_the_template_market_name_on_Football_Coupon_Details_Page(Common):
    """
    TR_ID: C508513
    NAME: Verify event displaying when market name differs from the template market name on Football Coupon Details Page
    DESCRIPTION: This test case verifies event displaying when market name differs from market template name on Football Coupon Details Page
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

    def test_006_repeat_steps_1_5_for_the_following_markets_match_result_match_result__both_teams_to_score_ladbrokes_added_from_ox_1003_total_goals_over_under_15_total_goals_over_under_25_total_goals_over_under_35_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_draw_no_bet_1st_half_result_to_win_to_nil_goal_in_both_halves(self):
        """
        DESCRIPTION: Repeat steps 1-5 for the following markets:
        DESCRIPTION: * Match Result
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
