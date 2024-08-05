import pytest

from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.retail
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.bet_filter
@pytest.mark.connect
@pytest.mark.desktop
@pytest.mark.football_bet_filter
@vtest
class Test_C2496181_Verify_navigation_to_Football_filter_from_Coupons_details_page(BaseCouponsTest, BaseFootballBetFilter):
    """
    TR_ID: C2496181
    NAME: Verify navigation to Football filter from Coupons details page
    PRECONDITIONS: Make sure Football Bet Filter feature is turned on in CMS: System configuration -> Connect -> football Filter
    PRECONDITIONS: following API returns events for applying Football filters on (After navigating to Football Filter search in console: *retailCoupon*):
    PRECONDITIONS: https://sandbox-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADb3b4313883004240a754070676e25258
    PRECONDITIONS: 1. Load SportBook App
    PRECONDITIONS: 2. Open Football landing page
    PRECONDITIONS: 3. Select 'Coupons' tab
    """
    keep_browser_open = True

    def found_and_open_coupon_by_name(self, coupon_name: str):
        coupon_groups = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_groups, msg='No event groups found on Coupon page')

        all_coupons = {}
        for coupon_group_name, coupon_group in coupon_groups.items():
            coupons = coupon_group.items_as_ordered_dict
            self.assertTrue(coupons, msg=f'No coupons found in {coupon_group_name} group')
            all_coupons.update(coupons)

        self.assertIn(coupon_name, all_coupons,
                      msg=f'"{coupon_name}" is not found in list of coupons "{all_coupons.keys()}"')
        found_coupon = all_coupons.get(coupon_name)
        self.assertTrue(found_coupon, msg=f'Coupon "{coupon_name}" not found in {all_coupons.keys()}')
        found_coupon.click()
        self.site.wait_content_state(state_name='CouponPage')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get coupons with suitable type
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('footballFilter'):
            raise CmsClientException('"Football Bet Filter" is disabled')

        coupon_resp = self.get_coupons()
        self.__class__.coupon_mr = None
        self.__class__.coupon_not_mr = None
        for coupon in coupon_resp:
            if coupon.get('coupon', {}).get('couponSortCode', '') == 'MR':
                self.__class__.coupon_mr = coupon['coupon']['name']
                break

        if not self.coupon_mr:
            raise SiteServeException('Coupon with couponSortCode MR not found')

        for coupon in coupon_resp:
            if coupon.get('coupon', {}).get('couponSortCode', '') != 'MR':
                self.__class__.coupon_not_mr = coupon['coupon']['name']
                break
        if not self.coupon_mr or not self.coupon_not_mr:
            raise SiteServeException('No sufficient coupon data found for test')

        if not self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                   category_id=self.ob_config.football_config.category_id):
            raise CmsClientException('Coupons tab disabled in CMS.')

        self.__class__.tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                                          self.ob_config.football_config.category_id)

    def test_001_select_any_coupon_that_has_coupon_sort_code_parameter_equal_to_mrto_find_it_search_coupons_in_console(self):
        """
        DESCRIPTION: Select any coupon
        DESCRIPTION: that has **couponSortCode** parameter equal to "MR"
        DESCRIPTION: (to find it search 'Coupons' in console)
        EXPECTED: Coupons details page is opened
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        result = self.site.football.tabs_menu.click_button(self.tab_name)
        self.assertTrue(result, msg=f'"{self.tab_name}" tab was not opened, active is "{self.site.football.tabs_menu.current}"')
        self.found_and_open_coupon_by_name(coupon_name=self.coupon_mr)

    def test_002_verify_that_bet_filter_link_is_displayed(self):
        """
        DESCRIPTION: Verify that 'Bet Filter' link is displayed
        EXPECTED: 'Bet Filter' link is placed at the top right corner
        """
        self.assertTrue(self.site.coupon.has_bet_filter_link(), msg='Bet filter link is not displayed')

    def test_003_tap_bet_filter_link(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link
        EXPECTED: * Bet Filter page is opened
        EXPECTED: * Proper call to API is made (see precondition), parameter 'filter' is set with selected coupon's name
        """
        self.site.coupon.bet_filter_link.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        events = self.get_events_for_coupon(coupon_name=self.coupon_mr)
        self.__class__.event_names = [event['eventName'] for event in events]

    def test_004_tap_find_bets_button(self):
        """
        DESCRIPTION: Tap 'Find bets' button
        EXPECTED: * Result page is displayed and it contains only events that belongs to selected coupons (and events correspond to API response in the same time)
        EXPECTED: * 'Add to Betslip' button at the bottom
        """
        self.assertFalse(self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=5),
                         msg='Spinner has not disappeared from Find Bets button')
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterResultsPage')
        events_ui = []
        selections = self.site.football_bet_filter_results_page.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')
        for selection_name, selection in selections.items():
            events_ui.append(selection.event_name)

        events_ui = list(set(events_ui))
        self.assertListEqual(sorted(events_ui), sorted(self.event_names),
                             msg=f'Results page contains list of events {sorted(events_ui)} '
                             f'which is not the same as expected list {sorted(self.event_names)}')

        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')

    def test_005_go_back_to_coupons_tab_and_select_any_coupon_where_coupon_sort_code_parameter_is_not_equal_to_mr(self):
        """
        DESCRIPTION: Go back to 'Coupons' tab and select any coupon
        DESCRIPTION: where **couponSortCode** parameter is NOT equal to "MR"
        DESCRIPTION: (to find it search 'Coupons' in console)
        DESCRIPTION: (Usually it's 'Over/ Under total goals')
        EXPECTED: Coupons details page is opened
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

        self.site.football.tabs_menu.click_button(self.tab_name)
        self.assertEqual(self.site.football.tabs_menu.current, self.tab_name, msg='COUPONS tab is not active')

        if not self.coupon_not_mr:
            raise SiteServeException('Coupon with couponSortCode not MR not found')
        self.found_and_open_coupon_by_name(coupon_name=self.coupon_not_mr)

    def test_006_verify_presence_of_bet_filter_link(self):
        """
        DESCRIPTION: Verify presence of 'Bet Filter' link
        EXPECTED: 'Bet Filter' link is absent
        """
        self.assertFalse(self.site.coupon.has_bet_filter_link(expected_result=False),
                         msg='Bet filter link is displayed')
