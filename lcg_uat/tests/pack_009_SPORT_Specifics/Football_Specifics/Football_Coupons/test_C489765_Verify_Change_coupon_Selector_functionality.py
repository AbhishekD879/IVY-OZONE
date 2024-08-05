import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.desktop
# we can not run such test simultaneously with other coupons
@pytest.mark.consequent
@pytest.mark.skipif(tests.settings.brand != 'bma' and 'desktop' not in tests.device_name.lower(),
                    reason='SKIPIF: Test case "C489765: Verify "Change coupon" Selector functionality" should be '
                           'executed for Ladbrokes on Desktop only')
@vtest
class Test_C489765_Verify_Change_coupon_Selector_functionality(BaseCouponsTest):
    """
    TR_ID: C489765
    NAME: Verify 'Change coupon' Selector functionality
    DESCRIPTION: This test case verifies  'Change coupon' Selector functionality
    """
    keep_browser_open = True

    auto_hiding_test_coupon = 'Auto Hiding Test Coupon'
    euro_elite_coupon = 'Euro Elite Coupon'

    def verify_correct_events_displayed_for_coupon(self, coupon_name):
        """
        :param coupon_name: name of coupon to verify
        """
        active_events_query = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                      self.ob_config.backend.ti.football.category_id))
        resp = self.ss_req_football.ss_coupon_to_outcome_for_coupon(
            coupon_id=self.ob_config.backend.ti.football.coupons[coupon_name], query_builder=active_events_query)
        self.__class__.coupon_events = [x for x in resp[0]['coupon']['children']]
        events_names_from_ss_resp = [x['event']['name'] for x in self.coupon_events]
        events_names_on_page = []
        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Can not find any section')
        for section_name, section in self.sections.items():
            date_groups = section.items_as_ordered_dict
            self.assertTrue(date_groups, msg=f'No date groups found on Coupon section {section_name}')
            for name, date_group in date_groups.items():
                events = date_group.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events found on Coupon details page in date group "{name}"')
                for event_name, events in events.items():
                    events_names_on_page.append(event_name)

        self.softAssert(self.assertListEqual, sorted(events_names_on_page), sorted(events_names_from_ss_resp))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add events for few coupons
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        autotest_event_id = self.ob_config.add_autotest_premier_league_football_event().event_id
        autotest_match_result_market_id = self.ob_config.market_ids[autotest_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id,
                                           coupon_name=self.auto_hiding_test_coupon)

        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        epl_event_id = self.ob_config.add_football_event_to_england_premier_league().event_id
        epl_match_result_market_id = self.ob_config.market_ids[epl_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=epl_match_result_market_id,
                                           coupon_name=self.euro_elite_coupon)

        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.ob_config.backend.ti.football.category_id)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page on coupons tab is opened
        EXPECTED: Football Landing page is opened with opened coupons tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        result = self.site.football.tabs_menu.current
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.matches}" tab was not opened')
        coupons = self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.assertTrue(coupons, msg='Coupons page was not opened')
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but Coupons is expected to be active')

    def test_002_select_coupon_from_the_list_and_tap_its_name(self, expected_coupon_name=auto_hiding_test_coupon):
        """
        DESCRIPTION: Select coupon from the list and tap its name
        EXPECTED: Selected Coupon details page is opened
        """
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=expected_coupon_name)

    def test_003_selector_displaying_in_the_coupons_details_page(self, expected_coupon_name=auto_hiding_test_coupon):
        """
        DESCRIPTION: Verify 'Change coupon' Selector displaying in the Coupon's Details page
        EXPECTED: 'Change coupon' Selector is displayed at the right side of Coupons sub-header
        """
        self.site.wait_content_state('CouponPage')
        result = wait_for_result(lambda: self.site.coupon.name == expected_coupon_name,
                                 timeout=5,
                                 name='Coupon name to be displayed')
        self.assertTrue(result, msg=f'Coupon name in subheader "{self.site.coupon.name}" is not the '
                                    f'same as expected "{expected_coupon_name}"')
        self.assertTrue(self.site.coupon.has_coupon_selector, msg='Coupon subheader doesn\'t have coupon selector')

    def test_004_tap_change_coupon_selector_link_and_verify_selector_content_and_animation(self):
        """
        DESCRIPTION: Tap 'Change coupon' Selector link and verify selector content and animation
        EXPECTED: - List of all available coupons received in response from OB is displayed
        EXPECTED: - the coupon list drop overlay cascades down the page
        EXPECTED: - white background must be visible hiding the content of the background page
        """
        # List of coupons verified in step 5
        pass

    def test_005_select_coupon_from_the_coupon_selector_and_tap_it(self, coupon_from_dropdown=auto_hiding_test_coupon):
        """
        DESCRIPTION: Select Coupon from the Coupon Selector and tap it
        EXPECTED: - Coupon Selector is automatically closed
        EXPECTED: - List of events for selected coupon is displayed for the chosen Coupon
        EXPECTED: - Selected coupon name is displayed in the sub header
        """
        self.site.coupon.coupon_selector_link.click()
        result = wait_for_result(lambda: coupon_from_dropdown in self.site.coupon.coupons_list.items_as_ordered_dict,
                                 timeout=1,
                                 name='Coupon name to be displayed in the list of coupons')
        self.assertTrue(result, msg=f'{coupon_from_dropdown} is not found in list of coupons')

        coupons_list = self.site.coupon.coupons_list.items_as_ordered_dict
        coupon = coupons_list.get(coupon_from_dropdown)
        coupon.click()
        self.site.wait_content_state('CouponPage')
        result = wait_for_result(lambda: self.site.coupon.name == coupon_from_dropdown,
                                 timeout=2,
                                 name='Coupon name to be changed')
        self.assertTrue(result, msg=f'Coupon name in subheader is not the '
                                    f'same as expected {coupon_from_dropdown}')

        self.verify_correct_events_displayed_for_coupon(coupon_name=coupon_from_dropdown)
        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on Coupon page')

    def test_006_repeat_step_5_for_all_available_in_the_selector_coupons(self, coupon_from_dropdown=euro_elite_coupon):
        """
        DESCRIPTION: Repeat step 5 for all available in the Selector Coupons
        """
        self.test_005_select_coupon_from_the_coupon_selector_and_tap_it(coupon_from_dropdown=coupon_from_dropdown)
