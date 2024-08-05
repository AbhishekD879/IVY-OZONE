import random
import re
import pytest
from tests.base_test import vtest
from tests.Common import Common
from json import JSONDecodeError
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
import voltron.environments.constants as vec
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.sports_specific
@pytest.mark.football_specific
@pytest.mark.reg171_fix
@pytest.mark.other
@vtest
class Test_C65949644_Verify_coupon_switcher_and_market_switchers_in_coupons_display_page(Common):
    """
    TR_ID: C65949644
    NAME: Verify coupon switcher and market switchers in coupons display page
    DESCRIPTION: This test case verify coupon switcher and market switchers in coupons display page
    PRECONDITIONS: CMS->sport category->football->(enable)accumulators
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        NAME: Verify coupon switcher and market switchers in coupons display page
    DESCRIPTION: This test case verify coupon switcher and market switchers in coupons display page
    PRECONDITIONS: CMS->sport category->football->(enable)accumulators
        """
        # checking whether coupons tab is enable or disable
        sport_id = self.ob_config.football_config.category_id
        response = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name='coupons')
        # making coupons tab is enabled in cms if it is disable in cms
        if not response['enabled']:
            tab_id = self.cms_config.get_sport_tab_id(sport_id=sport_id,
                                                      tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons)
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, enabled="true",
                                                     sport_id=sport_id)
        self.__class__.tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                                          self.ob_config.football_config.category_id).upper()

    def test_001_1launch_bmaapplication(self):
        """
        DESCRIPTION: 1.launch BMA
        DESCRIPTION: application
        EXPECTED: Application
        EXPECTED: Launched
        EXPECTED: successfully
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_navigate_to_football_page_and_clickon_coupons_tabnote_for_coral_accumulators(self):
        """
        DESCRIPTION: Navigate to football page and click
        DESCRIPTION: on coupons tab
        DESCRIPTION: Note for coral: Accumulators
        EXPECTED: Navigated to football page and coupons
        EXPECTED: tab opened
        """
        self.site.football.tabs_menu.click_button(self.tab_name)
        self.site.wait_content_state_changed()
        self.assertEqual(self.site.football.tabs_menu.current.upper(), self.tab_name,
                         msg=f'"{self.tab_name}" tab was not opened, active is "{self.site.football.tabs_menu.current}"')

    def test_003_find_the_popular_coupons_displayedbelow_the_featured_coupons_incoupons_tab(self):
        """
        DESCRIPTION: Find the popular coupons displayed
        DESCRIPTION: below the featured coupons in
        DESCRIPTION: coupons tab
        EXPECTED: Popular coupons displayed below the
        EXPECTED: featured coupons
        """
        # ********************** Getting expected coupons ****************************************************
        filters = [
            simple_filter(LEVELS.COUPON, attribute=ATTRIBUTES.CATEGORY_ID, operator=OPERATORS.EQUALS, value=16),
            simple_filter(LEVELS.COUPON, attribute=ATTRIBUTES.SITE_CHANNELS, operator=OPERATORS.CONTAINS, value='M'),
            exists_filter(LEVELS.COUPON,
                          simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, operator=OPERATORS.IS_FALSE))
        ]
        ss_bulider = self.ss_query_builder
        for fil in filters:
            ss_bulider.add_filter(fil)
        res = self.ss_req.ss_coupon(query_builder=ss_bulider)
        expected_coupons_list = [coupon['coupon']['name'].upper() for coupon in res]
        expected_coupons_list.sort()
        # ********************** Getting actual coupons ****************************************************
        wait_for_haul(2)
        all_coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.all_coupons = {coupon_name.upper(): coupon.items_as_ordered_dict for coupon_name, coupon in
                                      all_coupons.items()}
        actual_coupons_list = [coupon_name.upper() for coupons in self.all_coupons.values() for coupon_name in coupons]
        actual_coupons_list.sort()
        # ********************** Comparing expected and  actual coupons lists ****************************************************
        self.assertListEqual(expected_coupons_list, actual_coupons_list,
                             msg=f'expected coupons list is {expected_coupons_list} but actual coupons list {actual_coupons_list}')

    def test_004_click_on_any_of_the_popular_couponand_navigate_to_coupons_page(self):
        """
        DESCRIPTION: Click on any of the popular coupon
        DESCRIPTION: and navigate to coupons page
        EXPECTED: Coupons page is open and found
        """
        popular_coupons = self.all_coupons.get(vec.coupons.POPULAR_COUPONS.upper())
        self.assertTrue(popular_coupons, msg=f'No popular_coupons leagues are found in FE')
        random_pc_league_name, random_pc_league = next(iter(popular_coupons.items()))
        random_pc_league.click()

    def test_005_verify_edp_displayed_with_respectivecoupon_leagues_events_in_expanded_mode(self):
        """
        DESCRIPTION: Verify EDP displayed with respective
        DESCRIPTION: coupon leagues events in expanded mode
        EXPECTED: EDP displayed with respective leagues
        EXPECTED: and events in expanded mode
        """
        wait_for_haul(5)
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sections found in leagues')
        for section_name, section in list(sections.items())[0:5] if len(sections) > 2 else sections.items():
            if not section.is_expanded():
                section.expand()
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found in section')

    def test_006_verify_coupon_switcher_and_marketswitcher_displayed_in_edp(self):
        """
        DESCRIPTION: verify coupon switcher and market
        DESCRIPTION: switcher displayed in EDP
        EXPECTED: Coupon switcher and market
        EXPECTED: switcher displayed in EDP
        """
        self.site.header.scroll_to_top()
        self.assertTrue(self.site.coupon.has_coupon_selector, msg='Coupon subheader doesn\'t have coupon selector')
        self.site.coupon.coupon_selector_link.click()
        coupons_dropdown = self.site.coupon.coupons_list.items_as_ordered_dict
        self.assertTrue(coupons_dropdown, msg=f'No popular_coupons leagues are found in FE')
        random_dropdown_league_name, random_dropdown_league = next(iter(coupons_dropdown.items()))
        random_dropdown_league.click()
        self.site.wait_content_state('CouponPage')
        result = wait_for_result(lambda: self.site.coupon.name == random_dropdown_league_name,
                                 timeout=5,
                                 name='Coupon name to be changed')
        self.assertTrue(result, msg=f'Coupon name in subheader is not the '
                                    f'same as expected {random_dropdown_league_name}')

        # getting markets names from coupon's network call
        expected_markets = []
        response_url = self.get_response_url('EventToOutcomeForEvent')
        response = do_request(method='GET', url=response_url)
        events = response['SSResponse']['children']

        for event in events:
            if event.get('childCount'):
                break
            markets = event['event']['children']
            for market in markets:
                expected_markets.append(market['market']['name'])

        # Update the expected_markets acording to below markets
        for i, expected_market in enumerate(expected_markets):
            if expected_market.upper() == 'MATCH BETTING':
                expected_markets[i] = 'Match Result'
            elif expected_market.upper() == 'FIRST HALF RESULT':
                expected_markets[i] = 'First-Half Result'
            elif 'OVER/UNDER TOTAL GOALS' in expected_market.upper():
                expected_markets[i] = re.sub(r'OVER/UNDER TOTAL GOALS', 'TOTAL GOALS OVER/UNDER', expected_market.upper())

        # Update the expected_market_selectors variable with the updated markets names
        self.__class__.expected_market_selectors = [market_selector.upper() for market_selector in expected_markets]

        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on Coupon page')

    def test_007_click_on_coupon_switcher_and_verifylist_of_coupons_displayed_and_selectable_from_the_list__respective_coupon_data_displays(
            self):
        """
        DESCRIPTION: Click on coupon switcher and verify
        DESCRIPTION: list of coupons displayed and selectable from the list , respective coupon data displays
        EXPECTED: List of coupons displayed in coupon switcher and coupons are selectable from the list respective coupon data displayed
        """
        # covered in step 6

    def test_008_click_on_market_switcher_and_verifylist_of_markets_displayed_and_selectable_from_the_drop_down(self):
        """
        DESCRIPTION: Click on market switcher and verify
        DESCRIPTION: list of markets displayed and selectable from the drop down
        EXPECTED: List of coupons displayed in market switcher and markets are selectable from the drop down, respective data displayed
        """
        self.site.header.scroll_to_top()
        self.assertTrue(self.site.coupon.has_market_selector_module,
                        msg='Coupon doesn\'t have market selector')
        market_selector_list = []
        if self.device_type == 'desktop' and self.brand == 'bma':
            self.site.coupon.market_selector_module.click()
            market_selector = self.site.coupon.market_selector_module.text.split('\n')
            for item in market_selector:
                market_selector_list.append(item.strip().upper())
            result = set(sorted(market_selector_list)).issubset(set(sorted(self.expected_market_selectors)))
            self.assertTrue(result,
                            msg=f'Actual sections from FE: {sorted(market_selector_list)} is not in from FE:{sorted(self.expected_market_selectors)}')
        elif self.device_type == 'mobile':
            self.site.coupon.market_selector_module.click()
            market_selector = self.site.coupon.coupons_market_selector_list.items_as_ordered_dict
            for market_name, markets in market_selector.items():
                market_selector_list.append(market_name.upper())
            result = set(sorted(market_selector_list)).issubset(set(sorted(self.expected_market_selectors)))
            self.assertTrue(result,
                            msg=f'Actual sections from FE: {sorted(market_selector_list)} is not in from FE:{sorted(self.expected_market_selectors)}')
            name = random.choice(list(market_selector.keys()))
            market_selector.get(name).click()
            self.assertTrue(market_selector.get(name).is_selected(), msg=f'Market Selector is not selected')

        else:
            options = self.site.football.tab_content.dropdown_market_selector
            self.assertTrue(options, msg=f'No markets are available in Market sector drop down')
            markets_dropdown_list = list(options.items_as_ordered_dict.keys())
            result = set(
                sorted([markets_dropdownlist.upper() for markets_dropdownlist in markets_dropdown_list])).issubset(
                set(sorted(self.expected_market_selectors)))
            self.assertTrue(result,
                            msg=f'Actual sections from FE: {sorted([markets_dropdownlist.upper() for markets_dropdownlist in markets_dropdown_list])} is not in from FE:{sorted(self.expected_market_selectors)}')
            for market in markets_dropdown_list:
                options.select_value(value=market)
                wait_for_haul(2)
                options = self.site.football.tab_content.dropdown_market_selector

        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event found on Coupon page')
