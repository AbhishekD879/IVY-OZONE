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
class Test_C494703_Verify_SiteServer_call_for_the_Market_Selector_on_the_Football_Coupon_Details_page(Common):
    """
    TR_ID: C494703
    NAME: Verify SiteServer call for the  'Market Selector' on the Football Coupon Details page
    DESCRIPTION: This test case verifies SiteServer call for the  'Market Selector' on the Football Coupon Details page
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Coupons' tab
    PRECONDITIONS: 3. Choose some Football Coupon and navigates to 'Coupons' details page
    PRECONDITIONS: Make sure that this configuration is set up correctly: System Configuration > Config/Structure > FeatureToggle > FootballCoupons must be false for Coral
    PRECONDITIONS: https://jira.egalacoral.com/browse/BMA-37848
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

    def test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_different_markets_in_ss_response_by_coupon_id_from_precobditions(self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName' attribute for different markets in SS response by Coupon ID from Precobditions
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * Match Betting
        EXPECTED: * Both Teams to Score
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * Over/Under Total Goals 1.5
        EXPECTED: * Over/Under Total Goals 2.5
        EXPECTED: * Over/Under Total Goals 3.5
        EXPECTED: * To Win Not to Nil **Ladbrokes removed from OX 100.3**
        EXPECTED: * Draw No Bet
        EXPECTED: * First-Half Result
        EXPECTED: * To Win to Nil
        EXPECTED: * Score Goal in Both Halves
        """
        pass

    def test_002_verify_options_presence_in_the_market_selector_dropdown_list_on_football_coupon_details_page(self):
        """
        DESCRIPTION: Verify options presence in the 'Market selector' dropdown list on Football Coupon Details page
        EXPECTED: The following values are displayed in the 'Market Selector' dropdown list:
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
        """
        pass
