import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul, wait_for_result
import voltron.environments.constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.mobile_only
@pytest.mark.lad_prod
@pytest.mark.lucky_dip
@pytest.mark.quick_bet
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C65763184_Verify_whether_the_user_is_displayed_with_Lucky_Dip_signposting_in_bet_receipt_popup_beneath_the_receipt_id(BaseSportTest,BaseGolfTest):
    """
    TR_ID: C65763184
    NAME: Verify whether the user is displayed with Lucky Dip signposting in bet receipt popup beneath the receipt id
    DESCRIPTION: This test case verifies whether the user is displayed with Lucky Dip signposting in bet receipt popup beneath the receipt id
    PRECONDITIONS: Lucky dip market should be created in OB for Golf sport
    PRECONDITIONS: Lucky dip should be configured in CMS
    """
    keep_browser_open = True
    bet_amount = 0.10
    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventName = event['event']['name']
        self.__class__.marketName =  'GOLF - ' + event['event']['typeName']

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes Application
        EXPECTED: User logs in successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_edp_and_verify_if_the_lucky_dip_market_is_present(self):
        """
        DESCRIPTION: Navigate to Golf EDP and verify if the lucky dip market is present
        EXPECTED: Lucky dip market should be present in Golf EDP
        """
        self.navigate_to_page(name='sport/golf')
        self.site.golf.tabs_menu.click_button(self.expected_sport_tabs.outrights)
        self.assertEqual(self.site.golf.tabs_menu.current, self.expected_sport_tabs.outrights,
                         msg=f'"{self.expected_sport_tabs.outrights}" tab is not active')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in Outright tab')
        sections_names = [name.upper() for name in sections]
        self.assertIn(self.marketName.upper(), sections_names, msg=f'Required section : "{self.marketName}" not found in Outright tab sections : "{sections_names}"')
        section = sections.get(next((name for name in sections if name.upper() == self.marketName.upper()), None))
        section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in section : "{self.marketName}" of Outright tab')
        event_names = [event_name.upper() for event_name in events]
        self.assertIn(self.eventName.upper(), event_names, msg=f'Required event name : {self.eventName} not found in section : {self.marketName}')
        event = events.get(next((event_name for event_name in events if event_name.upper() == self.eventName.upper()), None))
        event.click()
        self.__class__.edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in self.edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')

    def test_003_click_on_the_lucky_dip_market_selection(self):
        """
        DESCRIPTION: Click on the lucky dip market selection
        EXPECTED: User should be navigated to lucky dip Landing page on clicking the selection
        """
        market_key = next((section_name for section_name in self.edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        lucky_dip_section = self.edp_market_sections.get(market_key)
        lucky_dip_section.scroll_to()
        lucky_dip_section.odds.click()
        self.assertTrue(lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(expected_result=True), msg=f"Lucky Dip animation is not displayed after clicking odds")

    def test_004_verify_if_the_user_is_displayed_with_number_keypad_to_enter_stake_and_place_bet_button_in_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify if the user is displayed with Number keypad to enter stake and place bet button in lucky dip landing page
        EXPECTED: User should be able to enter stake and able to click on place bet
        """
        quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(3)
        quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.__class__.odds = quick_bet.content.odds_value
        self.__class__.total_stake = quick_bet.bet_summary.total_stake
        self.__class__.total_est_return = quick_bet.bet_summary.total_estimate_returns
        self.__class__.market_name = quick_bet.content.market_name
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), f'Place Bet Button is not enabled!!')
        self.site.quick_bet_panel.place_bet.click()

    def test_005_verify_if_the_user_is_displayed_with_lucky_dip_animation_page(self):
        """
        DESCRIPTION: Verify if the user is displayed with lucky dip animation page
        EXPECTED: 'Lucky dip' animation page should be displayed with below content
        EXPECTED: 1. Player name(generated with RNG algorithm)
        EXPECTED: 2. Potential returns
        EXPECTED: 3.'Got it' CTA
        """
        lucky_dip_animation = wait_for_result(lambda: self.site.lucky_dip_got_it_panel, timeout=10)
        self.assertTrue(lucky_dip_animation, msg='Lucky Dip Animation is not displayed to the user')
        is_potential_returns = wait_for_result(lambda :self.site.lucky_dip_got_it_panel.lucky_dip_potential_returns)
        self.assertTrue(is_potential_returns, f'potential returns not displayed')
        is_player_name = wait_for_result(lambda :self.site.lucky_dip_got_it_panel.lucky_dip_player_name)
        self.assertTrue(is_player_name, f'player name is not displayed')
        is_got_it_button = wait_for_result(lambda :self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button)
        self.assertTrue(is_got_it_button, f'got it button is not displayed')

    def test_006_verify_if_the_user_is_displayed_bet_receipt_pop_up_on_clicking_got_it_cta(self):
        """
        DESCRIPTION: Verify if the user is displayed bet receipt pop-up on clicking 'Got it' CTA
        EXPECTED: User should be displayed with bet receipt popup with luck dip market details, stake and potential returns.
        """
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        self.bet_receipt_displayed = wait_for_result(
            lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10)
        self.assertTrue(self.bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt = self.site.quick_bet_panel.lucky_dip_outright_bet_receipt
        self.assertEqual(self.bet_receipt.lucky_dip_bet_placement_messeage, vec.betslip.SUCCESS_BET,
                         msg=f'Actual bet placement message : "{self.bet_receipt.lucky_dip_bet_placement_messeage}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        self.assertEqual(self.bet_receipt.lucky_dip_odds, self.odds, msg=f'Actual Stake : {self.bet_receipt.lucky_dip_odds } is not same as expected stake : {self.odds}')
        self.assertEqual(self.bet_receipt.lucky_dip_total_stake, self.total_stake, msg=f'Actual Stake : {self.bet_receipt.lucky_dip_total_stake } is not same as expected stake : {self.total_stake}')
        self.assertEqual(self.bet_receipt.lucky_dip_estimate_returns, self.total_est_return, msg=f'Actual Potential returns : {self.bet_receipt.lucky_dip_estimate_returns } is not same as expected potential returns : {self.total_est_return}')
        self.assertEqual(self.bet_receipt.lucky_dip_market_name, self.market_name, msg=f'Actual market name : {self.bet_receipt.lucky_dip_market_name } is not same as expected stake : {self.market_name}')


    def test_007_verify_if_the_user_is_displayed_with_lucky_dip_signposting_in__bet_receipt(self):
        """
        DESCRIPTION: Verify if the user is displayed with 'Lucky dip' signposting in  bet receipt
        EXPECTED: User should be displayed with 'Lucky dip' signposting in bet receipt popup beneath the receipt id
        """
        is_signposting = wait_for_result(lambda : self.bet_receipt.lucky_dip_market_name)
        self.assertTrue(is_signposting, f'signposting is not displyed!!')
        lucky_dip_signposting_text = self.bet_receipt.lucky_dip_market_name
        self.assertEqual(lucky_dip_signposting_text.upper(), 'LUCKY DIP', f'actual text in signposting : "{lucky_dip_signposting_text.upper()}" is not same with expected text : "LUCKY DIP" ')




