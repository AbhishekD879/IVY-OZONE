import pytest
import voltron.environments.constants.base.bet_history as vec
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65763315_Verify_if_the_lucky_dip_bet_has_a_cashout_in_My_bets_pagecashout_shouldnt_be_available(BaseGolfTest):
    """
    TR_ID: C65763315
    NAME: Verify if the lucky dip bet has a cashout in My bets page(cashout shouldn't be available)
    DESCRIPTION: This test case verifies if the lucky dip bet has a cashout in My bets page(cashout shouldn't be available)
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'Lucky Dip is not enabled in CMS')
        event = self.get_active_lucky_dip_events(number_of_events=1)[0]['event']
        self.__class__.event_name = event['name'].upper()
        self.__class__.start_time_local = self.convert_time_to_local(date_time_str=event['startTime'],
                                                      ob_format_pattern=self.ob_format_pattern,
                                                      future_datetime_format=self.my_bets_event_future_time_format_pattern,
                                                      ss_data=True).upper()
        self.__class__.eventID = event['id']

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes Application
        EXPECTED: User logs in successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_edp_for_which_lucky_dip_is_configured_and_place_a_bet_on_luck_dip_market(self):
        """
        DESCRIPTION: Navigate to Golf EDP for which lucky dip is configured and place a bet on luck dip market
        EXPECTED: User should be able to place a bet on lucky dip market
        """
        self.navigate_to_edp(event_id=self.eventID)
        # reading and verifying the LUCKY DIP market present in EDP
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        
        # scrolling to the lucky dip market and clocking on the odds button
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        
        # waiting for the quick bet to come
        quick_bet = self.site.quick_bet_panel
        wait_for_haul(3)
        
        # adding the stake and verifying the stake
        quick_bet.selection.content.amount_form.input.value = self.bet_amount
        bet_amount_string = '{:.2f}'.format(float(self.bet_amount))
        betslip_stake = '{:.2f}'.format(float(quick_bet.selection.content.amount_form.input.value))
        self.assertEqual(betslip_stake, bet_amount_string,
                         msg=f'Actual amount "{betslip_stake}" does not match '
                             f'expected "{bet_amount_string}"')
                             
        # clicking on place bet
        quick_bet.place_bet.click()
        
        # verifying if Lucky Dip got it Animation is coming or not
        luckey_dip_got_it_panel = wait_for_result(
            lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5),
            timeout=5)
        self.assertTrue(luckey_dip_got_it_panel, msg='Lucky Dip Animation is not displayed to the user')
        self.__class__.expected_lucky_dip_player_name = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.lucky_dip_player_name.upper(), timeout=10)
        
        # clicking on lucky Dip got it button
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        
        #waiting for lucky dip bet receipt to be displayed and closing it
        self.assertTrue(wait_for_result(lambda: quick_bet.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10), msg='Bet Receipt is not shown')
        quick_bet.lucky_dip_outright_bet_receipt.lucky_dip_close_button.click()

    def test_003_navigate_to_my_betsampgtopen_bets_and_check_whether_the_lucky_dip_bet_has_cash_out_available(self):
        """
        DESCRIPTION: Navigate to My bets&amp;gt;Open bets and check whether the lucky dip bet has cash out available
        EXPECTED: Lucky dip bet shouldn't have cash out available
        """
        # Navigate to My bets Open bets and checking basic bet details
        self.site.open_my_bets_open_bets()
        open_bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list,
                                    name='waiting for bets found on "Open Bets" page', expected_result=True,
                                    timeout=20)
        self.assertTrue(open_bets, msg='No bets found in open bet')
        open_bet_items = open_bets.items_as_ordered_dict
        event_name_with_date= f"{vec.BetHistory.MY_BETS_SINGLE_STAKE_TITLE} - [{self.event_name} {self.start_time_local}]"
        open_bet_events_names = [open_bet_event.upper() for open_bet_event in open_bet_items.keys()]
        self.assertIn(event_name_with_date, open_bet_events_names,
                      msg=f"{event_name_with_date} is not available in  {open_bet_events_names}')")
        event_name_with_date = next((event_name_key for event_name_key in open_bet_items if event_name_key.upper() == event_name_with_date),
                          None)
        bet_leg = open_bet_items.get(event_name_with_date)
        lucky_dip_icon_text = bet_leg.lucky_dip_icon
        self.assertEqual(lucky_dip_icon_text.upper(), "LUCKY DIP",
                      msg=f'Actual lucky dip icon text is:"{lucky_dip_icon_text.upper()}" not same as Expected : '
                          f'"LUCKY DIP"')
        player_name = bet_leg.outcome_name.upper()
        self.assertIn(player_name, self.expected_lucky_dip_player_name,
                      msg=f'Actual player name:"{player_name.upper()}" is not same as'
                          f'Expected player name: "{self.expected_lucky_dip_player_name}"')
                          
        # Navigating to My bets cashout and checking whether the lucky dip bet has cash out available
        self.site.open_my_bets_cashout()
        cashout_bet_items = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        cashout_bets_names = [cashout_bet_event.upper() for cashout_bet_event in cashout_bet_items.keys()]
        self.assertNotIn(event_name_with_date, cashout_bets_names, msg=f"{event_name_with_date} is available in {cashout_bets_names}")
