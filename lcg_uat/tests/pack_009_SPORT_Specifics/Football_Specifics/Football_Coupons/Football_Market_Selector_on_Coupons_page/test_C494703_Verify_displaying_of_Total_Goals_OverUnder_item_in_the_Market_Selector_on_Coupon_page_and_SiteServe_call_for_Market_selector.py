import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import simple_filter
import tests
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.market_selector
@pytest.mark.markets
@pytest.mark.ob_smoke
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C494703_Verify_SiteServer_call_for_the_Football_Market_Selector_on_Coupon_Details_page(BaseCouponsTest):
    """
    TR_ID: C494703
    NAME: Verify SiteServer call for the Football Market Selector on Coupon Details page
    DESCRIPTION: This test case verifies SiteServer call for the Football Market Selector on Coupon Details page
    PRECONDITIONS: 1) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: Steps
    PRECONDITIONS: 3) Use ti tool http://backoffice-tst2.coral.co.uk/ti/ for creation the markets with following templateMarketName for a particular event:
    PRECONDITIONS: * Over/Under Total Goals (rawHandicapValue="1.5")
    PRECONDITIONS: * Over/Under Total Goals (rawHandicapValue="2.5")
    PRECONDITIONS: * Over/Under Total Goals (rawHandicapValue="3.5")
    PRECONDITIONS: * Over/Under Total Goals (rawHandicapValue="4.5")
    """
    keep_browser_open = True
    autotest_coupon = 'Football Auto Test Coupon'
    ss_req = None
    over_under_values = [1.5, 2.5, 3.5, 4.5]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event with 'Over/Under Total Goals' market with "rawHandicapValue" = 1.5/2.5/3.5 and 4.5
        """
        for value in self.over_under_values:
            event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[
                ('over_under_total_goals', {'cashout': True, 'over_under': value})])
            self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[
                event_params.event_id]['over_under_total_goals'], coupon_name=self.autotest_coupon)

        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.ob_config.backend.ti.football.category_id)

    def test_001_navigate_to_test_coupon(self):
        """
        DESCRIPTION: Navigate to Football 'Coupons' tab
        EXPECTED: Events for selected coupon are displayed on Coupons Details page
        """
        self.navigate_to_page(name='sport/football/coupons')
        self.site.wait_content_state('Football')

        self.find_coupon_and_open_it(coupon_name=self.autotest_coupon)

    def test_002_go_to_network_all_preview_and_find_template_market_name_attribute_for_total_goals_overunder_market_in_ss_response(self):
        """
        DESCRIPTION: Go to Network -> All -> Preview and find 'templateMarketName' attribute for different markets in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * Over/Under Total Goals (rawHandicapValue="1.5")
        EXPECTED: * Over/Under Total Goals (rawHandicapValue="2.5")
        EXPECTED: * Over/Under Total Goals (rawHandicapValue="3.5")
        EXPECTED: * Over/Under Total Goals (rawHandicapValue="4.5")
        """
        active_events_query = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID,
                                      OPERATORS.INTERSECTS,
                                      self.ob_config.backend.ti.football.category_id))
        resp = self.ss_req_football.ss_coupon_to_outcome_for_coupon(coupon_id=self.ob_config.backend.ti.football.coupons[
            self.autotest_coupon], query_builder=active_events_query)
        events_in_coupon = [x for x in resp[0]['coupon']['children']]
        self._logger.info('*** Found events in coupon "{events_in_coupon}"')
        raw_handicap_values_from_request = [event['event']['children'][0]['market']['rawHandicapValue']
                                            for event in events_in_coupon
                                            if 'rawHandicapValue' in event['event']['children'][0]['market'].keys()]
        over_under_values = [str(x) for x in self.over_under_values]
        handicap_values_from_request_unique = sorted(list(set(raw_handicap_values_from_request)))
        self.assertListEqual(handicap_values_from_request_unique, over_under_values,
                             msg=f'Handicap values from request "{handicap_values_from_request_unique}" '
                                 f'are not the same as on UI "{over_under_values}"')

    def test_003_verify_if_value_is_available_for_coupon_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify values available for Coupon in the Market selector drop down
        EXPECTED: The following values are displayed in the Market selector drop down:
        EXPECTED: * Over/Under Total Goals 1.5
        EXPECTED: * Over/Under Total Goals 2.5
        EXPECTED: * Over/Under Total Goals 3.5
        EXPECTED: * Over/Under Total Goals 4.5
        """
        available_markets = self.site.coupon.tab_content.dropdown_market_selector.available_options
        self.assertTrue(available_markets, msg='Can not find any markets in drop down')
        self.assertIn(vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_1_5, available_markets,
                      msg=f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_1_5}" not found in "{available_markets}"')
        self.assertIn(vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5, available_markets,
                      msg=f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5}" not found in "{available_markets}"')
        self.assertIn(vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_3_5, available_markets,
                      msg=f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_3_5}" not found in "{available_markets}"')
        self.assertNotIn(vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_4_5, available_markets,
                         msg=f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_4_5}" found in "{available_markets}"')
