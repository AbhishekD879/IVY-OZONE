import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.google_analytics
@pytest.mark.market_selector
@pytest.mark.goalscorer
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.markets
@pytest.mark.other
@pytest.mark.low
@vtest
class Test_C490346_Football_Coupons_Market_Selector_Tracking(BaseDataLayerTest, BaseCouponsTest):
    """
    TR_ID: C490346
    VOL_ID: C9698698
    NAME: Football Coupons Market Selector Tracking
    DESCRIPTION: This Test Case verifies tracking of Coupons Market Selector usage by users
    PRECONDITIONS: 1. Console is opened
    PRECONDITIONS: 2. To verify tracking on real devices please use following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: 3. MARKET NAME - This is what market the customer sees and selects on site
    PRECONDITIONS: 4. OPENBET CATEGORY ID - This is the Sport on which the market selector was used.
    PRECONDITIONS: For Football Coupons always will be a football category ID
    """
    keep_browser_open = True
    euro_elite_coupon = 'Euro Elite Coupon'
    autotest_event_markets = ['both_teams_to_score', 'match_result']
    euro_elite_event_markets = ['match_result', 'draw_no_bet']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events were created
        """
        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('both_teams_to_score',
                                                                                    {'cashout': True})])
        for market, market_id in self.ob_config.market_ids[event.event_id].items():
            self.ob_config.add_event_to_coupon(market_id=market_id, coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

        event = self.ob_config.add_football_event_to_spanish_la_liga(markets=[('draw_no_bet', {'cashout': True})])
        for market, market_id in self.ob_config.market_ids[event.event_id].items():
            self.ob_config.add_event_to_coupon(market_id=market_id, coupon_name=self.euro_elite_coupon)

    def test_001_load_oxygen_application_and_go_to_football_coupons_landing_page(self):
        """
        DESCRIPTION: Load Oxygen application and go to Football -> Coupons landing page
        EXPECTED: Coupons landing page is opened
        """
        sport_name = vec.sb.FOOTBALL if self.brand == 'ladbrokes' else vec.sb.FOOTBALL.upper()

        self.site.home.menu_carousel.click_item(item_name=sport_name)
        self.site.wait_content_state(state_name='Football')
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)

        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but "{self.coupon_tab_name}" is expected to be active')

    def test_002_select_coupon_from_coupons_list_and_tap_it(self, coupon=vec.siteserve.EXPECTED_COUPON_NAME):
        """
        DESCRIPTION: Select Coupon from Coupons list and tap it
        EXPECTED: Coupon Details page is opened
        EXPECTED: Coupon Market Selector is displayed on the page
        """
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=coupon)

    def test_003_select_market_from_the_list_and_verify_tracking_data_for_the_selector(self, markets=autotest_event_markets):
        """
        DESCRIPTION: Tap Coupons Market selector and select Market from the list.
        DESCRIPTION: Go to Console -> DataLayer and verify tracking data for the Selector
        EXPECTED: Following data are displayed in DataLater:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'market selector',
        EXPECTED: 'eventAction' : 'change market',
        EXPECTED: 'eventLabel' : '<< MARKET NAME >>',
        EXPECTED: 'categoryID' : '<< OPENBET CATEGORY ID >>'
        EXPECTED: });
        """
        markets_in_dropdown = self.site.coupon.tab_content.dropdown_market_selector.available_options

        expected_markets_name = []
        for market in markets:
            market_template = getattr(vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES, market)
            expected_markets_name.append(self.cms_config.get_coupon_market_name_and_headers(market_template).market_name)

        for market in expected_markets_name:
            self.assertIn(market, markets_in_dropdown,
                          msg=f'"{market}" market cannot be found in {markets_in_dropdown} markets list')
            self.site.coupon.tab_content.dropdown_market_selector.value = market

            result = wait_for_result(lambda: market == self.site.coupon.tab_content.dropdown_market_selector.selected_market_selector_item,
                                     name=f'"{market}" market to be selected', timeout=3)
            selected_market = self.site.coupon.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertTrue(result, msg=f'Wrong market is selected. Expected: "{market}". Actual: "{selected_market}"')

            self.verify_coupon_market_selector_tracking(market_name=market)

    def test_004_repeat_step_3_for_different_markets_and_for_different_coupons(self):
        """
        DESCRIPTION: Repeat step 3 for different markets and for different Coupons
        """
        self.site.back_button_click()
        self.test_002_select_coupon_from_coupons_list_and_tap_it(coupon=self.euro_elite_coupon)
        self.test_003_select_market_from_the_list_and_verify_tracking_data_for_the_selector(markets=self.euro_elite_event_markets)
