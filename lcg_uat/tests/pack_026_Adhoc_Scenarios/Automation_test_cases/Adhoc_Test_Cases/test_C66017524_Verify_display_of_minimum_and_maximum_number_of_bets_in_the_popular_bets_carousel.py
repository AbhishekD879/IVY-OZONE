import pytest
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.adhoc_suite
@pytest.mark.trending_bets
@pytest.mark.adhoc24thJan24
@pytest.mark.timeout(900)
@pytest.mark.other
@vtest
class Test_C66017524_Verify_display_of_minimum_and_maximum_number_of_bets_in_the_popular_bets_carousel(BaseBetSlipTest):
    """
    TR_ID: C66017524
    NAME: Verify display of minimum and maximum number of bets in the popular bets carousel
    DESCRIPTION: This testcase is to verify display of minimum and maximum number of bets in the popular bets carousel
    PRECONDITIONS: 1. Trending Bets Carousel is configured in the CMS
    PRECONDITIONS: 2. Navigation to CMS -&gt; Most Popular/Trending Bets -&gt; Bet slip -&gt; Enable -&gt; Bet receipt -&gt; Enable for Bet receipt -&gt; Enable for Quick Bet receipt
    PRECONDITIONS: 3. Configure Min and Max Selections for Bet Slip and Bet Receipt in CMS
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    bet_amount = '0.1'
    end_date = f'{get_date_time_as_string(days=5)}T00:00:00.000Z'

    def get_active_selection(self):
        accordion_name, accordion = self.site.sports_page.tab_content.accordions_list.first_item
        event_name, event = accordion.first_item
        selection = next((selection for selection in event.template.items_as_ordered_dict.values() if selection.name.upper() not in ['N/A', 'SUSP']), None)
        if not selection:
            events = accordion.items_as_ordered_dict
            for event_name, event in events.items():
                selection = next((selection for selection in event.template.items_as_ordered_dict.values() if
                                  selection.name.upper() not in ['N/A', 'SUSP']), None)
                if selection:
                    break
        return selection


    def test_000_preconditions(self):
        trending_carousel_betslip = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('active')
        if not trending_carousel_betslip:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(active=True)
        trending_carousel_betreceipt = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get(
            'active')
        if not trending_carousel_betreceipt:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(active=True)

        trending_carousel_quickbet = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('isQuickBetReceiptEnabled')
        if not trending_carousel_quickbet:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(isQuickBetReceiptEnabled=True)

        self.__class__.max_trending_selections_betslip = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('maxSelections')
        self.__class__.max_trending_selections_bet_receipt = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('maxSelections')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)
        for event in events:
            if event.get('event') and event.get('event').get('children'):
                market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
                outcomes_resp = market['market']['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
                self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        self.site.login()

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.site.open_sport('Football')
        self.site.wait_content_state('football')

    def test_003_click_on_any_selection_and_add_to_betslip(self):
        """
        DESCRIPTION: Click on any Selection and Add to Betslip
        EXPECTED: Single Selection is added to Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_004_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Able to navigate to the Betslip and should see the Trending Bets carousel
        """
        #covered on above step

    def test_005_verify_noof_display_bets_in_popular_bets_carousel(self):
        """
        DESCRIPTION: Verify no.of display bets in Popular bets carousel
        EXPECTED: Popular bets carousel should display 2 bets only as per CMS config
        """
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')
        total_trending_bets_betslip = self.site.betslip.trending_bets_section.count_of_items
        self.assertEqual(total_trending_bets_betslip, self.max_trending_selections_betslip, msg=f' no.of "{self.max_trending_selections_betslip}" configured in cms are not equal to "{total_trending_bets_betslip}" in front end')

    def test_006_place_bet_in_betslip(self):
        """
        DESCRIPTION: Place bet in betslip
        EXPECTED: Should able to place bet and bet receipt should be loaded
        """
        self.place_single_bet()

    def test_007_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify bet receipt
        EXPECTED: Popular bets carousel should display under the &ldquo;Bet placed successfully&rdquo; message section in bet slip section
        """
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')

        total_trending_bets_betreceipt = self.site.bet_receipt.trending_bets_section.count_of_items
        self.assertEqual(total_trending_bets_betreceipt, self.max_trending_selections_bet_receipt,
                         msg=f' no.of "{self.max_trending_selections_bet_receipt}" configured in cms are not equal to "{total_trending_bets_betreceipt}" in front end')

    def test_008_configure_min_selection_as_2_for_bet_slip_and_bet_receipt_in_cms(self):
        """
        DESCRIPTION: Configure Min Selection as 2 for Bet Slip and Bet Receipt in CMS
        EXPECTED: Able to configure the Min selection as 2
        """
        if self.max_trending_selections_betslip != 2:
             self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(maxSelections=2)
        self.__class__.updated_max_trending_betslip_selections = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('maxSelections')

        if self.max_trending_selections_bet_receipt != 2:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(maxSelections=2)
        self.__class__.updated_max_trending_betreceipt_selections = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('maxSelections')
        self.device.driver.refresh()
        # Should give wait because even after refresh its taking time to reflect in front end so after waiting refreshing is again
        wait_for_haul(15)
        self.device.driver.refresh()
        self.device.driver.refresh()

    def test_009_verify_noof_display_bets_in_popular_bets_carousel(self):
        """
        DESCRIPTION: Verify no.of display bets in Popular bets carousel
        EXPECTED: Popular bets carousel should display 2 bets only as per CMS config
        """
        self.site.open_sport('Football')
        self.site.wait_content_state('football')
        selection = self.get_active_selection()
        selection.click()
        self.site.quick_bet_panel.close()
        self.site.open_betslip()
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')
        total_trending_bets_betslip = self.site.betslip.trending_bets_section.count_of_items
        self.assertEqual(total_trending_bets_betslip, self.updated_max_trending_betslip_selections,
                         msg=f' no.of "{self.updated_max_trending_betslip_selections}" configured in cms are not equal to "{total_trending_bets_betslip}" in front end')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        wait_for_result(lambda: self.updated_max_trending_betreceipt_selections, bypass_exceptions=VoltronException)
        trending_bet_sections = self.site.bet_receipt.trending_bets_section
        self.assertTrue(trending_bet_sections, msg='Trending bets sections are not display in Quick bet receipt')
        self.assertTrue(self.site.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')
        self.assertTrue(trending_bet_sections.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.bet_receipt.trending_bets_section.is_chevron_down,
                        msg='chevron did not turned down')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.bet_receipt.trending_bets_section.is_chevron_up,
                        msg='chevron did not turned up')
        total_trending_bets_betreceipt = len(self.site.bet_receipt.trending_bets_section.items_as_ordered_dict)
        self.assertEqual(total_trending_bets_betreceipt, self.updated_max_trending_betreceipt_selections,
                         msg=f' no.of "{self.updated_max_trending_betreceipt_selections}" configured in cms are not equal to "{total_trending_bets_betreceipt}" in front end')
        self.site.bet_receipt.close_button.click()

    def test_010_for_mobile_click_on_any_football_selection(self):
        """
        DESCRIPTION: For Mobile: Click on any Football Selection
        EXPECTED: Able to see the Quick Bet overlay
        """
        selection = self.get_active_selection()
        selection.click()
        wait_for_result(lambda: self.site.quick_bet_panel, bypass_exceptions=VoltronException)

    def test_011_enter_the_stake_and_place_a_quick_bet(self):
        """
        DESCRIPTION: Enter the stake and place a quick bet
        EXPECTED: Able to place a quick bet
        """
        quick_bet = self.site.quick_bet_panel.selection
        self.assertFalse(quick_bet.keyboard.is_displayed(name='Betslip keyboard shown',
                                                              timeout=3, expected_result=False),
                         msg='Keyboard is not collapsed by default')
        input_box = wait_for_result(lambda: quick_bet.content.amount_form.input, bypass_exceptions=VoltronException)
        self.assertTrue(input_box, 'input is not displayed')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='PLACE BET button is not disabled')
        input_box.click()
        if not quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10):
            input_box.click()
        self.assertTrue(quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10),
                        msg='Numeric keyboard is not opened')
        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP buttons is not enabled')
        self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

    def test_012_verify_the_quick_bet_receipt(self):
        """
        DESCRIPTION: Verify the quick bet receipt
        EXPECTED: Popular bets carousel should display under the &ldquo;Bet placed successfully&rdquo; message section in bet slip section
        """
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')
        trending_bet_sections = self.site.quick_bet_panel.bet_receipt.trending_bets_section
        self.assertTrue(trending_bet_sections, msg='Trending bets sections are not display in Quick bet receipt')
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')

        self.assertTrue(trending_bet_sections.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.trending_bets_section.is_chevron_down,
                        msg='chevron did not turned down')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.quick_bet_panel.bet_receipt.trending_bets_section.is_chevron_up,
                        msg='chevron did not turned up')

    def test_013_verify_noof_display_bets_in_popular_bets_carousel(self):
        """
        DESCRIPTION: Verify no.of display bets in Popular bets carousel
        EXPECTED: Popular bets carousel should display 2 bets only as per CMS config
        """
        trending_bets_quick_bet = self.site.quick_bet_panel.bet_receipt.trending_bets_section.count_of_items
        self.assertEqual(trending_bets_quick_bet, self.updated_max_trending_betreceipt_selections,
                         msg=f' no.of "{self.updated_max_trending_betreceipt_selections}" configured in cms are not equal to "{trending_bets_quick_bet}" in front end')

    def test_014_configure_max_selection_as_5_for_bet_slip_and_bet_receipt_in_cms(self):
        """
        DESCRIPTION: Configure Max Selection as 5 for Bet Slip and Bet Receipt in CMS
        EXPECTED: Able to configure the Min selection as 5
        """
        if self.max_trending_selections_betslip < 5:
            self.cms_config.update_most_popular_or_trending_bets_bet_slip_config(maxSelections=5)
        self.__class__.re_updated_max_trending_betslip_selections = self.cms_config.get_most_popular_or_trending_bets_bet_slip_config().get('maxSelections')

        if self.max_trending_selections_bet_receipt < 5:
            self.cms_config.update_most_popular_or_trending_bets_bet_receipt_config(maxSelections=5)
        self.__class__.re_updated_max_trending_betreceipt_selections = self.cms_config.get_most_popular_or_trending_bets_bet_receipt_config().get('maxSelections')
        self.device.driver.refresh()
        #Should give wait because even after refresh its taking time to reflect in front end so after waiting refreshing is again
        wait_for_haul(15)
        self.device.driver.refresh()

    def test_015_verify_noof_display_bets_in_popular_bets_carousel(self):
        """
        DESCRIPTION: Verify no.of display bets in Popular bets carousel
        EXPECTED: Popular bets carousel should display 5 bets only as per CMS config
        """
        self.test_010_for_mobile_click_on_any_football_selection()
        self.test_011_enter_the_stake_and_place_a_quick_bet()
        self.test_012_verify_the_quick_bet_receipt()
        trending_bets_quick_bet = self.site.quick_bet_panel.bet_receipt.trending_bets_section.count_of_items
        self.assertEqual(trending_bets_quick_bet, self.re_updated_max_trending_betreceipt_selections,
                         msg=f' no.of "{self.re_updated_max_trending_betreceipt_selections}" configured in cms are not equal to "{trending_bets_quick_bet}" in front end')

    def test_016_for_mobile_click_on_any_football_selection(self):
        """
        DESCRIPTION: For Mobile: Click on any Football Selection
        EXPECTED: Able to see the Quick Bet overlay
        """
        self.site.quick_bet_panel.close()
        selection = self.get_active_selection()
        selection.click()
        self.site.quick_bet_panel.close()
        self.site.open_betslip()

    def test_017_enter_the_stake_and_place_a_quick_bet(self):
        """
        DESCRIPTION: Enter the stake and place a quick bet
        EXPECTED: Able to place a quick bet
        """
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')
        trending_bet_sections = self.site.betslip.trending_bets_section
        self.assertTrue(trending_bet_sections, msg='Trending bets sections are not display in Quick bet receipt')
        self.assertTrue(self.site.betslip.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')

        self.assertTrue(trending_bet_sections.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.betslip.trending_bets_section.is_chevron_down,
                        msg='chevron did not turned down')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.betslip.trending_bets_section.is_chevron_up,
                        msg='chevron did not turned up')

    def test_018_verify_the_quick_bet_receipt(self):
        """
        DESCRIPTION: Verify the quick bet receipt
        EXPECTED: Popular bets carousel should display under the &ldquo;Bet placed successfully&rdquo; message section in bet slip section
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available in betslip')
        trending_bet_sections = self.site.bet_receipt.trending_bets_section
        self.assertTrue(trending_bet_sections, msg='Trending bets sections are not display in Quick bet receipt')
        self.assertTrue(self.site.bet_receipt.has_trending_bet_carousel(),
                        msg=f'Trending Bets Carousel section is not available')

        self.assertTrue(trending_bet_sections.chevron_arrow.is_displayed(), msg='Chevron arrow is not displayed')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.bet_receipt.trending_bets_section.is_chevron_down,
                        msg='chevron did not turned down')
        trending_bet_sections.chevron_arrow.click()
        self.assertTrue(self.site.bet_receipt.trending_bets_section.is_chevron_up,
                        msg='chevron did not turned up')

    def test_019_verify_noof_display_bets_in_popular_bets_carousel(self):
        """
        DESCRIPTION: Verify no.of display bets in Popular bets carousel
        EXPECTED: Popular bets carousel should display 5 bets only as per CMS config
        """
        total_trending_bets_betreceipt = self.site.bet_receipt.trending_bets_section.count_of_items
        self.assertEqual(total_trending_bets_betreceipt, self.re_updated_max_trending_betreceipt_selections,
                         msg=f' no.of "{self.re_updated_max_trending_betreceipt_selections}" configured in cms are not equal to "{total_trending_bets_betreceipt}" in front end')
        self.site.bet_receipt.close_button.click()
        self.test_010_for_mobile_click_on_any_football_selection()
        self.test_011_enter_the_stake_and_place_a_quick_bet()
        self.test_012_verify_the_quick_bet_receipt()
        trending_bets_quick_bet = self.site.quick_bet_panel.bet_receipt.trending_bets_section.count_of_items
        self.assertEqual(trending_bets_quick_bet, self.re_updated_max_trending_betreceipt_selections,
                         msg=f' no.of "{self.re_updated_max_trending_betreceipt_selections}" configured in cms are not equal to "{trending_bets_quick_bet}" in front end')
