import random
from collections import OrderedDict

import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_filter
@pytest.mark.football_bet_filter
@pytest.mark.retail
@pytest.mark.desktop
@vtest
class Test_C2161210_Verify_footer_of_Football_Filter_Results_page_depending_on_In_Shop_Online_betting_journey(BaseFootballBetFilter, BaseSportTest):
    """
    TR_ID: C2161210
    NAME: Verify footer of Football Filter Results page depending on In-Shop/ Online betting journey
    DESCRIPTION: This test case verify differences of Football Filter Results page depending on selected betting journey: online or in-shop
    DESCRIPTION: Only footer looks different, the rest is the same
    DESCRIPTION: [Bet Types](https://confluence.egalacoral.com/display/SPI/Bet+Types)
    DESCRIPTION: [Work Around for calculating payout potential of Multiple Bet Types](https://confluence.egalacoral.com/display/SPI/Work+Around+for+calulating+payout+potential+of+Multiple+Bet+Types)
    PRECONDITIONS: 1. Open Football -> Coupons tab -> Select any coupon that has couponSortCode parameter equal to "MR"
    PRECONDITIONS: 2. Tap Football Bet Filter
    PRECONDITIONS: 3. Scroll down and tap 'Find Bets'
    """
    keep_browser_open = True

    def check_off_one_several_selections(self):
        """
        Selects a couple of selections and verifies that Bets type, Calculated Odds and Est Returns are displayed correctly
        """
        odds = ['1/1' if self.last_item.odds.name == 'EVS' else self.last_item.odds.name]

        selections = random.sample(self.results.items(), 3) if len(self.results.items()) >= 3 \
            else list(self.results.items())[:-1]
        for selection in selections:
            if selection[1].checkbox.is_selected():
                continue
            else:
                selection[1].checkbox.click()
                odds.append('1/1' if selection[1].odds.name == 'EVS' else selection[1].odds.name)

        accumulator_odds = self.accumulator_odds(odds=odds)
        accumulation_sum = self.accumulation_sum(odds=odds)

        bet_filter_results_page = self.site.football_bet_filter_results_page

        accumulator_bet_type = bet_filter_results_page.accumulator_bet_type
        self.assertIn(accumulator_bet_type,
                      [vec.bet_finder.FB_BET_FILTER_SINGLE, vec.bet_finder.FB_BET_FILTER_DOUBLE,
                       vec.bet_finder.FB_BET_FILTER_TREBLE, vec.bet_finder.FB_BET_FILTER_FOURFOLD],
                      msg=f'Incorrect bet type "{accumulator_bet_type}" is displayed when {len(odds)} selections are selected')
        self.assertAlmostEqual(bet_filter_results_page.accumulator_quantity.replace(',', ''), accumulator_odds, delta=0.01,
                               msg=f'Incorrect accumulator odds. '
                                   f'\nExpected [{bet_filter_results_page.accumulator_quantity.replace(",", "")}, '
                                   f'\nActual [{accumulator_odds}]')
        self.assertEqual(bet_filter_results_page.accumulator_estimated_returns.replace(',', ''), accumulation_sum,
                         msg=f'Incorrect accumulation sum. '
                             f'\nExpected [{bet_filter_results_page.accumulator_estimated_returns.replace(",", "")}], '
                             f'\nActual [{accumulation_sum}]')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Make sure Football Bet Filter feature is turned on in CMS
        DESCRIPTION: Navigate to Coupons football
        DESCRIPTION: Tap Football Bet Filter
        DESCRIPTION: Scroll down and tap 'Find Bets'
        """
        content_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not content_config:
            content_config = self.cms_config.get_system_configuration_item('Connect')
        if content_config.get('footballFilter') is not True:
            raise CmsClientException('"footballFilter" is disabled in CMS')

        coupons = self.get_coupons()
        coupon_name = None
        for coupon in coupons:
            if coupon.get('coupon', {}).get('couponSortCode', '') == 'MR':
                coupon_name = coupon['coupon']['name']
                break

        if not coupon_name:
            raise SiteServeException('No sufficient coupon data found for test')
        self.__class__.coupon_name = coupon_name
        self.navigate_to_page('sport/football/coupons')
        self.site.wait_content_state(state_name='Football')

        coupon_groups = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_groups, msg='No event groups found on Coupon page')

        all_coupons = OrderedDict([])
        for coupon_group_name, coupon_group in coupon_groups.items():
            coupons = coupon_group.items_as_ordered_dict
            self.assertTrue(coupons, msg=f'No coupons found in {coupon_group_name} group')
            all_coupons.update(coupons)

        self.assertIn(self.coupon_name, all_coupons,
                      msg=f'"{self.coupon_name}" is not found in list of coupons "{all_coupons.keys()}"')

        coupons.get(self.coupon_name).click()
        self.site.wait_content_state(state_name='CouponPage')
        self.assertTrue(self.site.coupon.has_bet_filter_link(), msg='Can not find bet filter button')

        self.site.coupon.bet_filter_link.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=10),
                        msg='Can not find find bets button')

        self.site.football_bet_filter.find_bets_button.click()

    def test_001_verify_football_filter_results_page_for_online_betting_journey(self):
        """
        DESCRIPTION: Verify Football Filter Results page for online betting journey
        """
        self.site.wait_content_state(state_name='FootballBetFilterResultsPage')
        self.__class__.results = self.site.football_bet_filter_results_page.items_as_ordered_dict
        self.assertTrue(self.results, msg='Can not find any result on bet filter page')

    def test_002_verify_football_filter_results_footer(self):
        """
        DESCRIPTION: Verify 'Football filter results' footer
        EXPECTED: Footer contains:
        EXPECTED: - '£10 bet pays' label and estimated returns are represented as '-' next to it
        EXPECTED: - 'Maximum payout is £1,000,000' text
        EXPECTED: - 'ADD TO BETSLIP' button (inactive until at least one selection is selected)
        """
        self.site.football_bet_filter_results_page.accumulator_bet_pays.scroll_to()
        bet_pays = self.site.football_bet_filter_results_page.accumulator_bet_pays.name
        self.assertEqual(bet_pays, vec.bet_finder.FB_BET_FILTER_BET_PAYS,
                         msg=f'"{bet_pays}" is not equal to expected "{vec.bet_finder.FB_BET_FILTER_BET_PAYS}"')

        estimated_returns = self.site.football_bet_filter_results_page.accumulator_estimated_returns
        self.assertEqual(estimated_returns, '—',
                         msg=f'"{estimated_returns}" is not equal to expected "—"')

        accumulator_warning = self.site.football_bet_filter_results_page.accumulator_warning
        self.assertEqual(accumulator_warning, vec.bet_finder.FB_BET_FILTER_MAXIMUM_PAYOUT,
                         msg=f'"{bet_pays}" is not equal to expected "{vec.bet_finder.FB_BET_FILTER_MAXIMUM_PAYOUT}"')
        self.assertFalse(self.site.football_bet_filter_results_page.button.is_selected(expected_result=False),
                         msg=f'Button "ADD TO BETSLIP" is enabled')

        name, self.__class__.last_item = list(self.results.items())[-1]
        self.last_item.checkbox.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(timeout=3),
                        msg=f'Button "ADD TO BETSLIP" is disabled')

    def test_003_check_off_one_several_selections(self):
        """
        DESCRIPTION: Check off one/ several selections
        EXPECTED: * Bets type is displayed correctly and corresponds to quantity of selected selections
        EXPECTED: * Calculated Odds (next to bet type) are displayed correctly and corresponds to Odds of selected selections
        EXPECTED: * '£10 bet pays' label and calculated estimated returns next to it
        EXPECTED: * 'ADD TO BETSLIP' button is active
        """
        self.check_off_one_several_selections()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(timeout=3),
                        msg=f'Button "ADD TO BETSLIP" becomes disabled')

    def test_004_homepage_select_connect_from_header_sports_ribbon_tap_football_bet_filter_scroll_down_tap_find_bets(self):
        """
        DESCRIPTION: Verify Football Filter Results page for in-shop betting journey:
        DESCRIPTION: Homepage -> Select 'Connect' from header sports ribbon -> Tap Football Bet Filter -> Scroll down -> tap 'Find Bets'
        """
        # connect not available for ladbrokes
        if self.brand == 'bma':
            self.__class__.bet_filter_disabled = next((item['disabled'] for item in self.cms_config.get_connect_menu_items()
                                                       if item['targetUri'] == '/bet-filter'), None)
        else:
            self.__class__.bet_filter_disabled = True

        if not self.bet_filter_disabled:
            self.navigate_to_page(name='/bet-filter')
            selections = self.get_all_selections(coupon_name=self.coupon_name)
            if not selections:
                raise SiteServeException(f'There are no available selections for coupon "{self.coupon_name}"')
            self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=10),
                            msg='Can not find find bets button')
            self.site.football_bet_filter.find_bets_button.click()
            self.site.wait_content_state(state_name='FootballBetFilterResultsPage')

    def test_005_verify_football_filter_results_footer(self):
        """
        DESCRIPTION: Verify 'Football filter results' footer
        EXPECTED: Footer contains:
        EXPECTED: - '£10 bet pays' label and estimated returns are represented as '-' next to it
        EXPECTED: - 'Maximum payout is £1,000,000' text
        EXPECTED: - 'Place your bet in any Coral shop and track your bet with Bet Tracker. Odds may vary in-shop.' text
        EXPECTED: - 'SHOP LOCATOR' button (inactive until at least one selection is selected)
        """
        if not self.bet_filter_disabled:
            self.__class__.results = self.site.football_bet_filter_results_page.items_as_ordered_dict
            self.assertTrue(self.results, msg='Can not find any result on bet filter page')
            self.site.football_bet_filter_results_page.accumulator_bet_pays.scroll_to()
            bet_pays = self.site.football_bet_filter_results_page.accumulator_bet_pays.name
            self.assertEqual(bet_pays, vec.bet_finder.FB_BET_FILTER_BET_PAYS,
                             msg=f'"{bet_pays}" is not equal to expected "{vec.bet_finder.FB_BET_FILTER_BET_PAYS}"')
            estimated_returns = self.site.football_bet_filter_results_page.accumulator_estimated_returns
            self.assertEqual(estimated_returns, '—',
                             msg=f'"{estimated_returns}" is not equal to expected "—"')
            accumulator_warning = self.site.football_bet_filter_results_page.accumulator_warning
            self.assertEqual(accumulator_warning, vec.bet_finder.FB_BET_FILTER_MAXIMUM_PAYOUT,
                             msg=f'"{bet_pays}" is not equal to expected "{vec.bet_finder.FB_BET_FILTER_MAXIMUM_PAYOUT}"')
            self.assertFalse(self.site.football_bet_filter_results_page.button.is_selected(expected_result=False),
                             msg=f'Button "SHOP LOCATOR" is enabled')
            name, self.__class__.last_item = list(self.results.items())[-1]
            self.last_item.checkbox.click()
            self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(timeout=3),
                            msg=f'Button "SHOP LOCATOR" is disabled')

    def test_006_check_off_one_several_selections(self):
        """
        DESCRIPTION: Check off one/ several selections
        EXPECTED: * Bets type is displayed correctly and corresponds to quantity of selected selections
        EXPECTED: * Calculated Odds (next to bet type) are displayed correctly and corresponds to Odds of selected selections
        EXPECTED: * '£10 bet pays' label and calculated estimated returns next to it
        EXPECTED: * 'SHOP LOCATOR' button is active
        """
        if not self.bet_filter_disabled:
            self.check_off_one_several_selections()
            self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(timeout=3),
                            msg=f'Button "SHOP LOCATOR" becomes disabled')
