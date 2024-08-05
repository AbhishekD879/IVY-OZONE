import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.google_analytics
@pytest.mark.goalscorer
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.other
@pytest.mark.low
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-48836')  # Coral only
@vtest
class Test_C474792_Verify_Football_Coupons_Tracking(BaseCouponsTest, BaseDataLayerTest):
    """
    TR_ID: C474792
    VOL_ID: C9698456
    NAME: Verify Football Coupons Tracking
    DESCRIPTION: This test case verifies Football Coupons Tracking
    PRECONDITIONS: Dev Tools -> Console should be opened
    PRECONDITIONS: COUPON NAME - This is what coupon the user sees and selects on site
    """
    keep_browser_open = True
    coupons = None
    markets = [
        ('anytime_goalscorer', {'cashout': False}),
        ('first_goalscorer', {'cashout': False}),
        ('last_goalscorer', {'cashout': False})
    ]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add events to the following coupons: Football Autotest Coupon
        """
        self.__class__.expected_page_header = self.expected_sport_tabs.coupons

        event_id = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets).event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        match_result_market_id = self.ob_config.market_ids[event_id][market_short_name]

        self.__class__.coupons = list(self.ob_config.football_config.coupons.keys())
        self.__class__.coupons.remove('Auto Hiding Test Coupon')
        self.__class__.coupons.remove(vec.coupons.GOALSCORER_COUPON)

        for coupon_name in self.coupons:
            self.ob_config.add_event_to_coupon(market_id=match_result_market_id, coupon_name=coupon_name)

        for goalscorer_market, market_cashout_status in self.markets:
            goalscorer_market_id = self.ob_config.market_ids[event_id][goalscorer_market]
            self.ob_config.add_event_to_coupon(market_id=goalscorer_market_id, coupon_name=vec.coupons.GOALSCORER_COUPON)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        sport_name = vec.sb.FOOTBALL if self.brand == 'ladbrokes' else vec.sb.FOOTBALL.upper()

        self.site.home.menu_carousel.click_item(item_name=sport_name)
        self.site.wait_content_state(state_name='Football')

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: 'Coupons' tab is selected and highlighted
        EXPECTED: Coupons Landing page is loaded
        EXPECTED: List of coupons is displayed on the Coupons Landing page
        """
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)

        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}", but "{self.coupon_tab_name}" is expected')

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        DESCRIPTION: Choose any coupon from list on Coupons Landing page
        DESCRIPTION: Repeat steps 4-6 for all available coupons
        EXPECTED: Coupon Details page is loaded
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Coupon Selector',
        EXPECTED: 'eventAction' : 'Select Coupon',
        EXPECTED: 'eventLabel' : '<< COUPON NAME >>',
        EXPECTED: });
        """
        for coupon_name in self.coupons:
            self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=coupon_name)

            actual_page_title = self.site.coupon.header_line.page_title.title
            self.__class__.expected_page_header = 'COUPONS' if self.brand != 'ladbrokes' else coupon_name
            self.assertEqual(actual_page_title, self.expected_page_header,
                             msg=f'Page title "{actual_page_title}" '
                                 f'is not the same as expected "{self.expected_page_header}"')

            coupon_name_on_page = self.site.coupon.name
            self.assertEqual(coupon_name_on_page, coupon_name,
                             msg=f'Coupon name in subheader "{coupon_name_on_page}" '
                                 f'is not the same as expected "{coupon_name}"')

            self.verify_coupon_selection_tracking(coupon_name=coupon_name)
            self.site.back_button.click() if self.brand == 'ladbrokes' else self.site.coupon.back_button_click()

    def test_004_navigate_to_any_coupon_details_page(self):
        """
        DESCRIPTION: Navigate to any Coupon Details page
        EXPECTED: Coupon Details page is loaded
        """
        coupon_name = self.coupons[-1]
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=coupon_name)
        self.assertEqual(self.site.coupon.header_line.page_title.title, self.expected_page_header)

    def test_005_tap_change_coupon_selector_link_on_coupons_sub_header(self):
        """
        DESCRIPTION: Tap 'Change coupon' Selector link on Coupons sub-header
        DESCRIPTION: Choose any coupon from list on Coupons Landing page
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: List of all available coupons is displayed
        EXPECTED: Coupon Details page is loaded
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Coupon Selector',
        EXPECTED: 'eventAction' : 'Select Coupon',
        EXPECTED: 'eventLabel' : '<< COUPON NAME >>',
        EXPECTED: });
        """
        # there is no coupon selector on ladbrokes
        if self.brand != 'ladbrokes':
            for coupon_name in self.coupons:
                self.site.coupon.coupon_selector_link.click()

                coupons_list = self.site.coupon.coupons_list.items_as_ordered_dict
                self.assertIn(coupon_name, list(coupons_list.keys()),
                              msg=f'"{coupon_name}" is not found in list of coupons "{list(coupons_list.keys())}"')

                coupons_list[coupon_name].click()
                self.site.wait_content_state(state_name='CouponPage')

                result = wait_for_result(lambda: self.site.coupon.name == coupon_name,
                                         name=f'Coupon name to change',
                                         timeout=3)
                self.assertTrue(result, msg=f'Coupon name in header '
                                            f'is not the same as expected "{coupon_name}"')

                self.verify_coupon_selection_tracking(coupon_name=coupon_name)
