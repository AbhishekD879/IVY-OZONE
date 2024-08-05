import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65827639_Verify_flow_of_outright_bet_placement_after_Lucky_Dip_bet_placement(BaseGolfTest):
    """
    TR_ID: C65827639
    NAME: Verify flow of outright bet placement after Lucky Dip bet placement
    PRECONDITIONS: Lucky Dip should be configured in CMS
    PRECONDITIONS: Create a Event with Lucky Dip market and Outright market
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']
        self.__class__.decimalodds = self.get_decimal_and_fractional_prices_in_ob_config_by_event(event=event).get('decimalPrice') #decimalPrice and fractionalPrice
        self.__class__.obPlayername = self.get_selected_golfer_name_in_ob_config(event=event)
    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User logs in successfully
        """
        self.site.login()


    def test_002_navigate_to_golf_event_in_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Navigate to Golf event in which Lucky Dip Market is configured
        EXPECTED: Golf EDP page is displayed with Luck Dip Market and respective Odds
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_click_on_lucky_dip_odds(self):
        """
        DESCRIPTION: Click on the Odds
        EXPECTED: Lucky Dip Animation is displayed to the user with ODDS and prompts the user to enter stake and Place bet
        """
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        outright_market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'OUTRIGHT'),
                          None)
        outright_section = edp_market_sections.get(outright_market_key)
        if outright_section.has_show_all_button:
            outright_section.show_all_button.scroll_to()
            outright_section.show_all_button.click()
        outright_section.scroll_to()
        outright_players = outright_section.items_as_ordered_dict
        self.__class__.outright_player_names = [player_name.upper() for player_name in outright_players]
        self.assertIn("LUCKY DIP", edp_market_sections_name, msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'), None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        self.assertTrue(self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(expected_result=True),msg=f"Lucky Dip animation is not displayed")

    def test_004_give_some_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Give some stake and click on 'Place bet' button
        EXPECTED: After place Bet Animation Panel with got it button
        EXPECTED: Bet will be placed successfully. Bet receipt is displayed
        """
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(3)
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.__class__.odds = self.quick_bet.content.odds_value
        self.__class__.total_stake = self.quick_bet.bet_summary.total_stake
        self.__class__.total_est_return = self.quick_bet.bet_summary.total_estimate_returns
        self.__class__.market_name = self.quick_bet.content.market_name
        self.__class__.event_name = self.quick_bet.content.event_name
        self.site.quick_bet_panel.place_bet.click()
        lucky_dip_got_it_animation = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5), timeout=5)
        self.assertTrue(lucky_dip_got_it_animation, msg='Lucky Dip Animation is not displayed to the user')
        self.__class__.expected_lucky_dip_player_name = self.site.lucky_dip_got_it_panel.lucky_dip_player_name
        self.assertNotEqual(self.expected_lucky_dip_player_name, self.obPlayername,
                            msg=f'expected player name: "{self.expected_lucky_dip_player_name}" is same as OBplayer name "{self.obPlayername}"')
        self.assertIn(self.expected_lucky_dip_player_name, self.outright_player_names,
                      msg=f'expected player name : "{self.expected_lucky_dip_player_name}" is not in Outright players names:"{self.outright_player_names}"')

        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
    def test_005_Verify_Bet_receipt(self):
        """
        DESCRIPTION: verify Lucky dip bet receipt
        EXPECTED: need to be display bet receipt
        """
        self.__class__.bet_receipt_displayed = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10)
        self.assertTrue(self.bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt = self.site.quick_bet_panel.lucky_dip_outright_bet_receipt
        self.assertEqual(self.bet_receipt.lucky_dip_bet_placement_messeage, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.bet_receipt.lucky_dip_bet_placement_messeage}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        self.assertEqual(self.bet_receipt.lucky_dip_market_name, self.market_name,
                         msg=f'Actual Outcome name: "{self.bet_receipt.lucky_dip_market_name}" '
                             f'does not match expected: "{self.market_name}"')
        self.assertEqual(self.bet_receipt.lucky_dip_event_name, self.event_name,
                         msg=f'Actual Market name" "{self.bet_receipt.lucky_dip_event_name}" '
                             f'does not match expected: "{self.event_name}"')
        self.assertTrue(self.bet_receipt.lucky_dip_bet_id, msg='Bet ID is not shown')
        self.assertEqual(self.bet_receipt.lucky_dip_odds, self.odds,
                         msg=f'Actual Odds: "{self.bet_receipt.lucky_dip_odds}" '
                             f'does not match expected: "{self.odds}"')
        self.assertEqual(self.bet_receipt.lucky_dip_total_stake, self.total_stake,
                         msg=f'Actual Total Stake: "{self.bet_receipt.lucky_dip_total_stake}" '
                             f'does not match expected: "{self.total_stake}"')
        self.assertAlmostEqual(float(self.bet_receipt.lucky_dip_estimate_returns), float(self.total_est_return),
                               delta=0.01,
                               msg=f'Actual Est./Pot. Returns: "{float(self.bet_receipt.lucky_dip_estimate_returns)}"'
                                   f'does not match expected: "{float(self.total_est_return)}" with delta 0.01')
        self.__class__.lucky_dip_bet_receipt_player_name = self.bet_receipt.lucky_dip_player_name.split('to')[0].strip()
        self.assertEqual(self.lucky_dip_bet_receipt_player_name.upper(), self.expected_lucky_dip_player_name.upper(),
                         msg=f'Actual Market name" "{self.lucky_dip_bet_receipt_player_name.upper()}" '
                             f'does not match with expected: "{self.expected_lucky_dip_player_name.upper()}"')

    def test_006_verify_lucky_dip_on_mybets(self):
        """
        DESCRIPTION: Open "MyBets"
        DESCRIPTION: Verify LUCKY DIP bet receipt in MyBets
        """
        self.bet_receipt.lucky_dip_close_button.click()
        self.site.open_my_bets_open_bets()
        open_bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict,
                                    name='waiting for bets found on "Open Bets" page', expected_result=True,
                                    timeout=20)
        self.assertTrue(open_bets, msg='No bets found in open bet')
        bet_leg = list(open_bets.values())[0]
        player_name = bet_leg.outcome_name
        self.assertIn(player_name, self.lucky_dip_bet_receipt_player_name,
                      msg=f'Actual outcome:"{player_name}" is not same as'
                          f'Expected outcome: "{self.lucky_dip_bet_receipt_player_name}"')
        lucky_dip_icon_text = bet_leg.lucky_dip_icon
        self.assertIn(lucky_dip_icon_text, "LUCKY DIP",
                      msg=f'Actual outcome:"{lucky_dip_icon_text}" is not same as'
                          f'Expected outcome: "{"LUCKY DIP"}"')
        actual_odd = bet_leg.odds_value
        if actual_odd != self.decimalodds:
            self.assertEqual(actual_odd, self.odds,
                         msg=f'Actual price "{actual_odd}" is not same as Expected price "{self.odds}"')
        else:
            self.assertEqual(actual_odd, self.decimalodds,
                             msg=f'Actual price "{actual_odd}" is not same as Expected price "{self.decimalodds}"')
        actual_stake = bet_leg.stake.stake_value
        self.assertEqual(actual_stake, self.total_stake,
                         msg=f'Actual stake "{actual_stake}" is not same as '
                             f'Expected stake "{self.total_stake}"')
        actual_est_returns = bet_leg.est_returns.stake_value
        self.assertEqual(actual_est_returns, self.total_est_return,
                         msg=f'Actual stake "{actual_est_returns}" is not same as '
                             f'Expected stake "{self.total_est_return}"')
        self.site.back_button_click()

    def test_007_navigate_to_the_golf_edp_page_where_outright_market_is_configured(self):
        """
        DESCRIPTION: Navigate to the Golf EDP page where outright market is configured
        EXPECTED: outright market is displayed with selections
        """
        edp_markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        market_names = [market.upper() for market in edp_markets.keys()]
        self.assertIn("OUTRIGHT", market_names,
                      msg=f'Expected OUTRIGHT Market is not displayed in EDP page')
        outright_tab = next((section_name for section_name in edp_markets if section_name.upper() == 'OUTRIGHT'), None)
        outright_section = edp_markets.get(outright_tab)
        outright_section.scroll_to()
        self.__class__.outright_players = outright_section.items_as_ordered_dict
        if len(self.outright_players) == 0:
            raise SiteServeException('No Outright events')
        self.__class__.outright_player = list(self.outright_players.values())[0]

    def test_008_click_on_the_outright_odds(self):
        """
        DESCRIPTION: Click on the odds
        EXPECTED: QB will be displayed
        """
        self.outright_player.odds.click()

    def test_009_give_some_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Give some stake and click on 'place bet' button
        EXPECTED: Bet should place successfully without any delay
        """
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(3)
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.__class__.outright_market_name = self.quick_bet.content.market_name
        self.__class__.outright_odds = self.quick_bet.content.odds_value
        self.__class__.outright_total_stake = self.quick_bet.bet_summary.total_stake
        self.__class__.outright_total_est_return = self.quick_bet.bet_summary.total_estimate_returns
        self.site.quick_bet_panel.place_bet.click()
        outright_bet_receipt_displayed = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10, expected_result=True)
        self.assertTrue(outright_bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.outright_bet_receipt = self.site.quick_bet_panel.lucky_dip_outright_bet_receipt
        wait_for_result(lambda: self.outright_bet_receipt.lucky_dip_bet_placement_messeage, timeout=10)
        actual_bet_placement_message = self.outright_bet_receipt.lucky_dip_bet_placement_messeage
        self.assertEqual(actual_bet_placement_message, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{actual_bet_placement_message}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')

    def test_010_verify_outright_on_mybets(self):
        """
        DESCRIPTION: Open "MyBets"
        DESCRIPTION: Verify Outright bet receipt in MyBets
        """
        self.outright_bet_receipt.lucky_dip_close_button.click()
        self.site.open_my_bets_open_bets()
        open_bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict,
                        name='waiting for bets found on "Open Bets" page', expected_result=True,
                        timeout=20)
        self.assertTrue(open_bets, msg='No bets found in open bet')
        bet_leg = list(open_bets.values())[0]
        outright_market = bet_leg.market_name
        self.assertIn(outright_market, self.outright_market_name,
                      msg=f'Actual outcome:"{outright_market}" is not same as'
                          f'Expected outcome: "{self.outright_market_name}"')
        actual_outright_odd = bet_leg.odds_value
        self.assertEqual(actual_outright_odd, self.outright_odds,
                         msg=f'Actual price "{actual_outright_odd}" is not same as Expected price "{self.outright_odds}"')
        actual_outright_stake = bet_leg.stake.stake_value
        self.assertEqual(actual_outright_stake, self.outright_total_stake,
                         msg=f'Actual stake "{actual_outright_stake}" is not same as '
                             f'Expected stake "{self.outright_total_stake}"')
        actual_outright_est_returns = bet_leg.est_returns.stake_value
        self.assertEqual(actual_outright_est_returns, self.outright_total_est_return,
                         msg=f'Actual stake "{actual_outright_est_returns}" is not same as '
                             f'Expected stake "{self.outright_total_est_return}"')