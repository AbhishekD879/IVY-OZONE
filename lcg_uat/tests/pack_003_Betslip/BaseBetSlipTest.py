import re
from collections import namedtuple
from collections import OrderedDict
from datetime import datetime
from typing import List
from time import sleep
from fractions import Fraction

from crlat_ob_client.bet_intercept import BetInterceptRequests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.Common import Common
from voltron.pages.shared import get_device_properties
from voltron.utils.exceptions.failure_exception import TestFailure
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result, wait_for_haul


class BaseBetSlipTest(Common):
    expected_bet_slip_page_title = vec.betslip.BETSLIP_BTN
    expected_my_bets_page_title = vec.bet_history.TAB_TITLE
    expected_active_tab = vec.bet_history.CASHOUT
    required_bet_slip_tabs = ['BETSLIP', 'MY BETS']
    expected_active_btn_open_bets = vec.bma.SPORTS
    expected_active_btn_settled_bets = vec.bma.SPORTS
    expected_sorting_types_btns_open_bets = vec.bet_history.SORTING_BUTTON_TYPES_OPEN_BETS
    expected_sorting_types_btns_settled_bets = vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS
    expected_betslip_counter_value = 0
    max_number_of_symbols_in_stake_input = 15
    betslip_counter = None
    quick_stakes = [5, 10, 50, 100]
    bet_amount = 0.05 if tests.settings.backend_env == 'prod' else 1
    now = datetime.now()
    today = now.strftime('%d/%m/%Y')
    expected_bet_type = None
    event_names_betslip = []
    outcome_names = []
    bet_id = None
    total_stake = None
    total_stake_betreceipt = None
    total_stake_betslip = None
    total_est_return_betslip = None
    freebet_stake = None
    stake = None
    expected_overask_messages = []
    new_overask_prices = []
    __bet_intercept = None

    @property
    def bet_intercept(self):
        if not self.__bet_intercept:
            self.__class__.__bet_intercept = BetInterceptRequests(env=tests.settings.backend_env,
                                                                  brand=self.brand)
        return self.__bet_intercept

    def is_betslip_icon_shown(self):
        icon_shown = self.site.header.bet_slip_counter.is_displayed()
        self.assertTrue(icon_shown, msg='Betslip icon is not shown')

    def reload_betslip(self):
        """
        Closes and opens betslip
        """
        if self.device_type != 'mobile':
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage')
            result = self.site.has_betslip_opened()
        else:
            self.site.close_betslip()
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
            self.site.header.bet_slip_counter.click()
            result = self.get_betslip_content()
        self.assertTrue(result, msg='Betslip is not displayed')

    def open_betslip_with_selections(self, selection_ids, timeout: int = 0):
        """
        :param selection_ids: either a string (single value) or tuple
        :param timeout: time to sleep before method execution
        """
        sleep(timeout)  # We need this to handle some issue with deeplinks when we're closing betslip
        selections = ''
        if isinstance(selection_ids, (str, int)):
            selections = selection_ids
            self.__class__.expected_betslip_counter_value += 1
        else:
            selections += ''.join(['%s,' % selection for selection in selection_ids])
            selections = selections.rstrip(',')
            self.__class__.expected_betslip_counter_value += len(selection_ids)
        url = f'https://{tests.HOSTNAME}/betslip/add/{selections}'
        self._logger.info('*** Opening betslip by deeplink via URL: %s' % url)
        self.device.navigate_to(url=url)
        self.site.wait_splash_to_hide(timeout=60)
        if self.device_type == 'mobile':
            self.site.has_betslip_opened()
        wait_for_result(lambda: self.get_betslip_content(),
                        timeout=1,
                        name='Betslip sections to load',
                        bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                        )
        wait_for_result(lambda: int(self.site.header.bet_slip_counter.counter_value) == self.expected_betslip_counter_value,
                        name=f'Betslip counter to change from "{int(self.site.header.bet_slip_counter.counter_value)}" '
                             f'to "{self.expected_betslip_counter_value}"',
                        timeout=tests.settings.betslip_counter_timeout, bypass_exceptions=(ValueError, NoSuchElementException, StaleElementReferenceException))
        self.__class__.betslip_counter = int(self.site.header.bet_slip_counter.counter_value)
        self._logger.debug(f'*** Bet Slip counter value: "{self.betslip_counter}"')
        self.assertEqual(self.betslip_counter, self.expected_betslip_counter_value,
                         msg=f'Betslip counter "{self.betslip_counter}" is not the same as number '
                             f'of added selections "{self.expected_betslip_counter_value}"')

    def get_expected_my_bets_tabs(self) -> list:
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut')
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        if not cashout_cms:
            is_cashout_tab_enabled = False
        else:
            is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')

        in_shop_bet_history = system_config.get('Connect', {}).get('shopBetHistory')

        available_tabs = [vec.bet_history.OPEN_BETS_TAB_NAME]
        if is_cashout_tab_enabled:
            available_tabs.append(vec.bet_history.CASH_OUT_TAB_NAME)
        available_tabs.append(vec.bet_history.SETTLED_BETS_TAB_NAME)

        if in_shop_bet_history:
            available_tabs.append(vec.bet_history.IN_SHOP_BETS_TAB_NAME)
        return available_tabs

    def add_outright_selection(self, number_of_selections=1, **kwargs):
        selection_name = kwargs.get('selection_name', '')
        selected_outputprices = []
        markets_list = wait_for_result(lambda: self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict,
                                       name='Sections to appear',
                                       timeout=2)
        market_name_ss = kwargs.get('market_name', self.expected_market_sections.outright)
        market_name = market_name_ss if self.device_type == 'mobile' else market_name_ss.upper()
        section = markets_list.get(market_name)
        self.assertTrue(section, msg='Can not find outright section on page')
        output_prices_list = section.outcomes.items_as_ordered_dict
        self.assertTrue(output_prices_list, msg='No outright selections are present on page')
        for output_price_name, output_price in output_prices_list.items():
            if len(selected_outputprices) >= number_of_selections:
                    break
            if selection_name:
                if output_price_name == selection_name:
                    selected_outputprices.append(output_price), \
                        self._logger.debug('*** Outcome name is: "%s", output price is: "%s"'
                                           % (output_price_name, output_price.output_price))\
                        if output_price.bet_button.is_enabled() else \
                        self._logger.debug('*** Outcome with name "%s" is suspended'
                                           % output_price_name)
                    break
            else:
                if output_price.bet_button.is_enabled():
                    selected_outputprices.append(output_price)
                    self._logger.debug('*** Outcome name is: "%s", output price is: "%s"'
                                       % (output_price_name, output_price.output_price))
                else:
                    self._logger.debug('*** Outcome with name "%s" is suspended' % output_price_name)

        for output_price in selected_outputprices:
            output_price.bet_button.click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            self.assertTrue(output_price.bet_button.is_selected(), msg='Output price is not highlighted after selection')
        self.__class__.expected_betslip_counter_value = len(selected_outputprices)

    def select_sp_price(self):
        singles_section = self.get_betslip_sections().Singles
        for stake_index in range(0, len(singles_section.items())):
            stake_name, stake = list(singles_section.items())[stake_index]
            stake.odds_dropdown.select_value('SP')
            self.site.betslip._load_complete()

            singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(singles_section.items())[stake_index]
            selected_option = stake.odds
            self.assertEqual(selected_option, 'SP', msg=f'"SP" is not selected have "{selected_option}" instead')

    def get_betslip_sections(self, multiples=False, all_available=False, timeout=3):
        betslip_sections = wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                           timeout=timeout,
                                           name='Betslip sections to load')
        self.assertTrue(len(betslip_sections) > 0, msg='No bets found')
        singles_name, multiples_name, = vec.betslip.BETSLIP_SINGLES_NAME, vec.betslip.MULTIPLES
        self.assertTrue(singles_name in betslip_sections.keys(), msg=f'"{singles_name}" section is not found')
        singles_section_stakes = betslip_sections[singles_name]
        self.assertTrue(len(singles_section_stakes) > 0, msg='No stakes found in betslip Singles section')
        singles_section_stakes.wait_until_refreshed(timeout=0.5)
        if all_available:
            return betslip_sections
        sections_list = list()
        sections_list.append(betslip_sections[singles_name])
        SectionsNamed = namedtuple("stakes", ["Singles", "Multiples"])

        def sections(Singles, Multiples=None):
            return SectionsNamed(Singles, Multiples)
        if multiples:
            self.assertTrue(multiples_name in betslip_sections.keys(), msg=f'"{multiples_name}" section is not found')
            multiples_section_stakes = betslip_sections[multiples_name]
            self.assertTrue(len(multiples_section_stakes) > 0,
                            msg=f'No stakes found in betslip "{multiples_name}" section')
            sections_list.append(betslip_sections[multiples_name])
        return sections(*sections_list)

    def zip_available_stakes(self, section, number_of_stakes=None):
        stakes = OrderedDict()
        for stake_name in list(section.keys())[:number_of_stakes]:
            if section[stake_name].is_suspended(timeout=0):
                msg = f'*** Skipping Stake "{stake_name}" as it is suspended'
                self._logger.info(msg)
                continue
            else:
                stakes[stake_name] = section[stake_name]
        return stakes

    def select_each_way_checkbox(self, stake):
        stake_name, stake_we = stake
        self.assertTrue(stake_we.has_each_way_checkbox,
                        msg=f'Each way checkbox is not present for "{stake_name}"')
        stake_we.each_way_checkbox.input.click()
        self.assertTrue(stake_we.each_way_checkbox.is_selected(),
                        msg='Each way checkbox is not checked')

    def enter_stake_amount(self, stake, stake_bet_amounts=None, each_way=None):
        """
        :param each_way:
        :param stake_bet_amounts:
        :param stake: tuple (stake name, stake web element)
        :return:
        """
        stake_name, stake_ = stake
        expected_bet_amount = stake_bet_amounts[stake_name] \
            if stake_bet_amounts and stake_name in stake_bet_amounts.keys() else self.bet_amount
        try:
            stake_.amount_form.input.value = expected_bet_amount
            if each_way:
                self.select_each_way_checkbox(stake=stake)
        except StaleElementReferenceException:
            for section_name, section in self.get_betslip_content().betslip_sections_list.items():
                section.wait_until_refreshed(timeout=1)
                self.assertTrue(section, msg=f'No one stake was found in section: "{section_name}"')
                stake_ = section[stake_name] if stake_name in section.keys() else None
                if stake_:
                    stake_.amount_form.input.value = expected_bet_amount
                    input_value = stake_.amount_form.input.value
                    if input_value != expected_bet_amount:
                        wait_for_haul(2)
                        stake_.amount_form.input.value = expected_bet_amount
                    if each_way:
                        self.select_each_way_checkbox(stake=stake)
                    break
            else:
                raise TestFailure(f'No stake with name "{stake_name}" found')
        except InvalidElementStateException as e:
            if self.device_type == 'mobile' and get_device_properties().get('allow_emulation'):
                self.enter_value_using_keyboard(expected_bet_amount)
            else:
                raise VoltronException(f'Can not set value in stake. {e}')
        expected_bet_amount = '{:.2f}'.format(float(expected_bet_amount))
        result = wait_for_result(lambda: '{:.2f}'.format(float(str(stake_.amount_form.input.value))) == expected_bet_amount,
                                 name=f'Stake amount field value "{stake_.amount_form.input.value}" to change',
                                 bypass_exceptions=(ValueError, StaleElementReferenceException, NoSuchElementException),
                                 timeout=1.5)
        input_value = stake_.amount_form.input.value
        try:
            amount_form_value = '{:.2f}'.format(float(str(input_value)))
        except ValueError:
            raise GeneralException(f'Could not convert string to float: "{input_value}"')
        self.assertTrue(result, msg=f'Stake amount field value "{amount_form_value}" '
                                    f'is not the same as expected: "{expected_bet_amount}"')

    def select_freebet_for_stake(self, stake):
        """
        :param stake: tuple (stake name, stake web element)
        """
        stake_name, stake = stake
        if stake.has_use_free_bet_link():
            stake.amount_form.click()  # to dismiss freebet tooltip
            stake.use_free_bet_link.click()
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
            self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
            selected_free_bet = dialog.select_first_free_bet()
            self.assertTrue(dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" '
                                                             f'dialog is not closed')
            return selected_free_bet
        else:
            raise VoltronException('Use Free Bet link is not displayed')

    def place_single_bet(self, number_of_stakes=None, each_way=False, sp=False, freebet=False, stake_bet_amounts=None):
        """
        :param each_way: True or False. Each way factor
        :param sp: True or False. Only for selection that have both SP/LP prices. if True - will change to SP
        :param number_of_stakes: int
        :param freebet: True or False. if True - will place bet using freebet
        :param stake_bet_amounts: dictionary where key is selection name and value is bet amount for this selection
        :return: None
        """
        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance if self.site.wait_logged_in(
                login_criteria='betslip_balance', timeout=3) else 0
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        if sp:
            self.select_sp_price()
        section = self.get_betslip_sections().Singles
        number_of_stakes = number_of_stakes if number_of_stakes and number_of_stakes < len(section.keys()) else len(
            section.keys())
        available_stakes = list(self.zip_available_stakes(section=section, number_of_stakes=number_of_stakes).items())
        for stake in available_stakes:
            if freebet:
                self.select_freebet_for_stake(stake=stake)
            else:
                self.enter_stake_amount(stake=stake, stake_bet_amounts=stake_bet_amounts, each_way=each_way)

        betslip = self.get_betslip_content()
        bet_now_button = betslip.bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=5), msg='Place Bet button is not enabled')
        bet_now_button.click()
        try:
            if self.get_betslip_content().has_bet_now_button():
                if 'ACCEPT' in self.get_betslip_content().bet_now_button.name:
                    self.get_betslip_content().bet_now_button.click()
        except VoltronException:
            pass

    def collect_stake_info(self, stake, multiples=False):
        stake_name, stake_we = stake
        bet_amount = self.bet_amount
        unit_stake = bet_amount
        est_returns = float(stake_we.est_returns) if stake_we.est_returns not in ['N/A', ''] else stake_we.est_returns

        info_dict = {
            'event_name': None if multiples else stake_we.event_name,
            'outcome_name': stake_we.outcome_name,
            'market_name': None if multiples else stake_we.market_name,
            'odds': stake_we.odds,
            'bet_amount': bet_amount,
            'unit_stake': unit_stake,
            'estimate_returns': est_returns
        }
        return info_dict

    def verify_estimated_returns(self, est_returns, odds, bet_amount, freebet_amount=0,
                                 each_way_coef=0, is_double=False, delta=0.04):
        """
        Verifies that estimated returns value is calculated correctly.
        :param est_returns: actual estimated returns for the stake
        :param odds: given price(s)
        :param bet_amount: bet amount entered to amount field for stake
        :param freebet_amount: freebet value
        :param each_way_coef: Each way coefficient. 0 if each way is not selected
        :param is_double: Specifies if est. returns is calculated for multiple (double) or single stake
        """
        if isinstance(odds, str):
            odds = [odds, ]
        if 'SP' in odds or '' in odds:
            self.assertEqual(est_returns, 'N/A',
                             msg=f'Estimate returns for odds "{odds}" is "{est_returns}", but expected N/A')
        else:
            expected_est_returns = self.calculate_estimated_returns(odds=odds,
                                                                    bet_amount=bet_amount,
                                                                    freebet_amount=freebet_amount,
                                                                    each_way_coef=each_way_coef,
                                                                    is_double=is_double)
            self.assertAlmostEqual(float(est_returns), expected_est_returns, delta=delta,
                                   msg=f'Actual estimated returns "{est_returns}" doesn\'t match expected '
                                       f'"{expected_est_returns}" within "{delta}" delta')

    def calculate_estimated_returns(self, odds, bet_amount, freebet_amount=0, each_way_coef=0, is_double=False):
        """
        Calculates estimated returns value for given parameters for a single stake.
        If estimated returns for a couple of stakes is needed just call
        this function for every stake and add the results.
        Note: if is_double = True est return will be calculated correctly only for case when 2 stakes are added
        :param odds: given price(s)
        :param bet_amount: bet amount entered to amount field for stake
        :param freebet_amount: freebet value
        :param each_way_coef: Each way odds. 0 if each way is not selected
        :param is_double: Specifies if est. returns is calculated for  multiple (double) or single stake
        :return: Calculated value for estimated returns
        """
        prices = list(odds)
        try:
            payout_first_stake = float(prices[0])
        except ValueError:
            payout_first_stake = self.convert_fraction_price_to_decimal(initial_price=prices[0]) + 1
        bet_amount = float(bet_amount)
        bet_winnings = (payout_first_stake - 1) * bet_amount  # amount of money that player wins
        bet_returns = bet_amount + bet_winnings  # stake + winnings
        freebet_returns = (payout_first_stake - 1) * freebet_amount  # only winnings as freebet is not player's money
        est_returns = bet_returns + freebet_returns
        if each_way_coef:
            ew_bet_winnings = bet_amount * (payout_first_stake - 1) * each_way_coef  # side winnings
            ew_freebet_winnings = freebet_amount * (payout_first_stake - 1) * each_way_coef  # side freebet winnings
            ew_bet_returns = bet_amount * 2 + bet_winnings + ew_bet_winnings  # double stake + winnings
            ew_freebet_returns = (freebet_returns + ew_freebet_winnings) / 2  # stake is divided (main and side bet)
            est_returns = ew_bet_returns + ew_freebet_returns
        if is_double:
            try:
                payout_second_stake = float(prices[1])
            except ValueError:
                payout_second_stake = self.convert_fraction_price_to_decimal(initial_price=prices[1]) + 1
            est_returns *= payout_second_stake
        expected_est_returns = round(est_returns, ndigits=2)
        self._logger.info(f'*** Calculated Est. returns: "{expected_est_returns}"')
        return expected_est_returns

    def calculate_combined_odd(self, prices_list: list):
        """
        :param prices_list: all prices in list of dictionaries
        :return: combined odd(str)
        """
        combined_odd = 1.0
        for odd in range(len(prices_list)):
            if list(prices_list[odd].keys())[0] == 0:
                odds = float(Fraction(prices_list[odd][0])) + 1.0
            else:
                odds = float(Fraction(prices_list[odd]['odds_home'])) + 1.0
            combined_odd *= odds
        combined_odd -= 1
        return str(Fraction(combined_odd))

    def place_and_validate_single_bet(self, number_of_stakes=None, each_way=False, ew_coef=0, sp=False, freebet=0,
                                      stake_bet_amounts=None, **kwargs):
        """
        :param number_of_stakes: specifies number of stakes, int
        :param each_way: specifies each way factor, True or False
        :param ew_coef: specifies each way coefficient, if no entered calculated based on ew_terms from BaseRacingTest
        :param sp: True or False. Only for selection that have both SP/LP prices. if True - will change to SP
        :param freebet: specifies freebet amount, if 0 - will place bet without using freebet
        :param stake_bet_amounts:
        :return: ordered dictionary with bet info
        """
        bet_info = OrderedDict()
        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance if self.site.wait_logged_in(
                login_criteria='betslip_balance', timeout=3) else 0
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        if sp:
            self.select_sp_price()
        section = self.get_betslip_sections().Singles
        number_of_stakes = number_of_stakes if number_of_stakes and number_of_stakes < len(section.keys()) else len(
            section.keys())

        expected_total_stake = 0
        for stake in self.zip_available_stakes(section=section, number_of_stakes=number_of_stakes).items():
            if freebet:
                self.select_freebet_for_stake(stake=stake)
            else:
                self.enter_stake_amount(stake=stake, stake_bet_amounts=stake_bet_amounts, each_way=each_way)
                if each_way:
                    ew_coef = float(self.ew_terms['ew_fac_num']) / float(self.ew_terms['ew_fac_den']) if not ew_coef \
                        else ew_coef
            params = self.collect_stake_info(stake=stake)

            market_name = stake[1].market_name
            if market_name == f'{vec.betslip.REVERSE_FORECAST} 2':
                reverse_multiplier = 2
            elif market_name == f'{vec.betslip.COMBINATION_TRICAST} 6':
                reverse_multiplier = 6
            else:
                reverse_multiplier = 1
            expected_total_stake += round((self.bet_amount * (2 if each_way else 1) * reverse_multiplier), 2)

            self.verify_estimated_returns(est_returns=params['estimate_returns'], odds=params['odds'],
                                          bet_amount=params['bet_amount'], freebet_amount=freebet,
                                          each_way_coef=ew_coef)
            bet_info[stake[0]] = params  # stake[0] -> stake_name

        betslip = self.get_betslip_content()
        total_stake_betslip = float(betslip.total_stake)
        bet_info['total_stake'] = total_stake_betslip
        total_est_returns = betslip.total_estimate_returns
        bet_info['total_estimate_returns'] = 'N/A' if total_est_returns == 'N/A' else float(total_est_returns)
        expected_total_stake = sum(stake_bet_amounts.values()) if stake_bet_amounts else expected_total_stake

        self.assertAlmostEqual(total_stake_betslip, expected_total_stake, delta=kwargs.get("delta", 0.01),
                               msg=f'Total stake "{total_stake_betslip}" is not correct, expected '
                               f'"{expected_total_stake}" with delta "{kwargs.get("delta", 0.01)}"')
        wait_for_result(lambda: betslip.bet_now_button.is_enabled(timeout=0.5),
                        name='Betnow button to be enabled')
        betslip.bet_now_button.click()
        try:
            if self.get_betslip_content().has_bet_now_button():
                if 'ACCEPT' in self.get_betslip_content().bet_now_button.name:
                    self.get_betslip_content().bet_now_button.click()
        except VoltronException:
            pass
        return bet_info

    def place_multiple_bet(self, number_of_stakes=None, each_way=False, sp=False, freebet=False,
                           multiples=True, stake_bet_amounts=None, **kwargs):
        """
        :param number_of_stakes: int
        :param each_way: True or False. Each way factor
        :param sp: True or False. True if selection have both SP/LP prices and it's needed to place bet on SP
        :param multiples: True or False.
        :param freebet: True or False. if True - will place bet using freebet
        :param stake_bet_amounts
        :return: None
        """
        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance if self.site.wait_logged_in(
                login_criteria='betslip_balance', timeout=3) else 0
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        if sp:
            self.select_sp_price()

        sections = self.get_betslip_sections(multiples=multiples)
        multiples_section = sections.Multiples

        number_of_stakes = number_of_stakes if number_of_stakes and number_of_stakes < len(
            multiples_section.keys()) else len(multiples_section.keys())
        if kwargs.get('stake_name'):
            for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=number_of_stakes).items():
                if stake[0] == kwargs['stake_name']:
                    if freebet:
                        self.select_freebet_for_stake(stake=stake)
                    else:
                        self.enter_stake_amount(stake=stake, stake_bet_amounts=stake_bet_amounts, each_way=each_way)
                    break
        else:
            for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=number_of_stakes).items():
                if freebet:
                    self.select_freebet_for_stake(stake=stake)
                else:
                    self.enter_stake_amount(stake=stake, stake_bet_amounts=stake_bet_amounts, each_way=each_way)
        betslip = self.get_betslip_content()
        bet_now_button = betslip.bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=5), msg='Place Bet button is not enabled')
        bet_now_button.click()
        try:
            if self.get_betslip_content().has_bet_now_button():
                if 'ACCEPT' in self.get_betslip_content().bet_now_button.name:
                    self.get_betslip_content().bet_now_button.click()
        except VoltronException:
            pass

    def place_and_validate_multiple_bet(self, number_of_stakes=None, each_way=False, ew_coef=0, sp=False,
                                        multiples=True, freebet=0, stake_bet_amounts=None):
        """
        :param number_of_stakes: int
        :param each_way: True or False. Each way factor
        :param ew_coef: specifies each way coefficient, if no entered calculated based on ew_terms from BaseRacingTest
        :param sp: True or False. True if selection have both SP/LP prices and it's needed to place bet on SP
        :param multiples: True or False.
        :param freebet: specifies freebet amount, if 0 - will place bet without using freebet
        :param stake_bet_amounts:
        :return: ordered dictionary with bet info
        """
        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance if self.site.wait_logged_in(
                login_criteria='betslip_balance', timeout=3) else 0
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        n_a_bets = ['Flag', 'Single Stakes About', 'Double Stakes About']  # details in BMA-21910
        bet_info = OrderedDict()
        bet_info_singles = OrderedDict()
        if sp:
            self.select_sp_price()

        sections = self.get_betslip_sections(multiples=multiples)
        singles_section, multiples_section = sections.Singles, sections.Multiples

        number_of_stakes = number_of_stakes if number_of_stakes and number_of_stakes < len(
            multiples_section.keys()) else len(multiples_section.keys())
        for single_stake in self.zip_available_stakes(section=singles_section,
                                                      number_of_stakes=len(singles_section.keys())).items():
            params_singles = self.collect_stake_info(stake=single_stake)
            bet_info_singles[single_stake[0]] = params_singles  # single_stake[0] -> single stake name
        odds_list = [outcome['odds'] for outcome_name, outcome in bet_info_singles.items()]
        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=number_of_stakes).items():
            stake_name = stake[0]
            if freebet:
                self.select_freebet_for_stake(stake=stake)
            else:
                self.enter_stake_amount(stake=stake, stake_bet_amounts=stake_bet_amounts, each_way=each_way)
                if each_way:
                    ew_coef = float(self.ew_terms['ew_fac_num']) / float(self.ew_terms['ew_fac_den']) if not ew_coef \
                        else ew_coef
            params = self.collect_stake_info(stake=stake, multiples=True)
            bet_info[stake_name] = params
            est_returns = multiples_section[stake_name].est_returns
            if 'Double' in stake_name and len(singles_section.keys()) <= 2:
                self.verify_estimated_returns(est_returns=params['estimate_returns'], odds=odds_list,
                                              each_way_coef=ew_coef, bet_amount=params['bet_amount'],
                                              freebet_amount=freebet, is_double=True)
            if next(i for i in n_a_bets) in stake_name:
                self.assertEqual(est_returns, 'N/A', msg='Estimated return for stake "%s" is not N/A' % stake_name)

        betslip = self.get_betslip_content()
        total_stake_betslip = float(betslip.total_stake)
        bet_info['total_stake'] = total_stake_betslip
        total_est_returns = betslip.total_estimate_returns
        bet_info['total_estimate_returns'] = 'N/A'\
            if any(i in multiples_section.keys() for i in n_a_bets) or 'SP' in odds_list \
            else float(total_est_returns)
        betslip.bet_now_button.is_enabled(timeout=20)
        betslip.bet_now_button.click()
        bet_info.update(bet_info_singles.items())
        return bet_info

    def place_bet_on_all_available_stakes(self, each_way=False):
        """
        Placing bet on all available stakes (singles, multiples)
        :return:
        """
        bet_info = OrderedDict()
        all_sections = self.get_betslip_sections(all_available=True)
        for section_name, section in all_sections.items():
            stake_info = OrderedDict()
            section.wait_until_refreshed(timeout=.5)
            for stake in self.zip_available_stakes(section=section).items():
                stake_name = stake[0]
                self.enter_stake_amount(stake=stake, each_way=each_way)
                one_stake_info = self.collect_stake_info(stake=stake,
                                                         multiples=stake_name not in ['Double', 'Trixie', 'Round Robin',
                                                                                      'Flag', 'Single Stakes About',
                                                                                      'Double Stakes About'])
                stake_info.update({stake_name: one_stake_info})
            bet_info.update({section_name: stake_info})

        betslip = self.get_betslip_content()
        bet_now_button = betslip.bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=3), msg='Place Bet button is not enabled')
        bet_now_button.click()
        try:
            if self.get_betslip_content().has_bet_now_button():
                if 'ACCEPT' in self.get_betslip_content().bet_now_button.name:
                    self.get_betslip_content().bet_now_button.click()
        except VoltronException:
            pass
        return bet_info

    def remove_stake(self, name):
        """
        :param name: name of stake from Singles section (it is only possible to remove stakes from Singles)
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(name, singles_section, msg=f'Stake "{name}" was not found')
        singles_section[name].remove_button.click()

    def check_acca_offer_for_stake(self, stake_name, offer_type, currency='£', expected_result=True):
        """
        :param stake_name: Double, Treble, Acc4 etc
        :param offer_type: Eligible, Suggested, SuggestedType2
        :param currency:
        :param expected_result: either acca offer is expected to be present (True), or not (False)
        """
        multi_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(len(multi_section) > 0, msg='No Multiples stakes found')
        self.assertTrue(stake_name in multi_section, msg=f'No "{stake_name}" found')
        stake = multi_section[stake_name]
        if expected_result:
            stake.scroll_to()
            self.assertTrue(stake.has_acca_insurance_offer(),
                            msg=f'"{stake_name}" stake does not have Multiples "{offer_type}" offer')
            acca_offer_text = stake.acca_insurance_offer.text

            expected_acca_offer_text = self.cms_config.\
                get_acca_notification(offer_type=offer_type, currency=currency)
            self.assertEqual(acca_offer_text, expected_acca_offer_text,
                             msg=f'\nActual ACCA offer text "{acca_offer_text}"\nExpected ACCA '
                                 f'offer text "{expected_acca_offer_text}"')
        else:
            self.assertFalse(stake.has_acca_insurance_offer(expected_result=False),
                             msg=f'It is not expected "{stake_name}" stake to have ACCA "{offer_type}" offer')
        return stake

    def check_suspended_selections_in_betslip(self, number_of_selections, expected_message, clear_betslip=True):
        """
        This method checks all selections on betslip is suspended and clears betslip after that
        :param number_of_selections: expected number of selections on Betslip
        :param expected_message: expected error message
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section) == number_of_selections, msg=f'Should be "{number_of_selections}" stakes '
                                                                          f'found but present "{len(singles_section)}"')

        for stake_name, stake in singles_section.items():
            self.assertTrue(stake.is_suspended(timeout=30), msg=f'Stake "{stake_name}" is not suspended')
            result = stake.amount_form.input.is_enabled(timeout=10, expected_result=False)
            self.assertFalse(result, msg=f'Amount field is not disabled for "{stake_name}"')

        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg='Bet Now button is not disabled')
        betnow_error = self.get_betslip_content().wait_for_error()
        result = wait_for_result(
            lambda: betnow_error == expected_message,
            name='Betslip error to change',
            timeout=5)
        self.assertTrue(result, msg=f'Bet Now section warning "{betnow_error}"'
                                    f'is not the same as expected: "{expected_message}"')

        if clear_betslip:
            self.clear_betslip()

    def get_price_odds_on_betslip(self, **kwargs):
        betslip_prices = OrderedDict()

        def _make_stake_odds_dict(section):
            for stake_name in section.keys():
                betslip_prices[section[stake_name].outcome_name] = section[stake_name].odds

        if 'section' in kwargs:
            section = kwargs['section']
            _make_stake_odds_dict(section)
        else:
            betslip_sections = self.get_betslip_sections(all_available=True)
            self.assertTrue(betslip_sections, msg='No betslip sections found')
            for section_name, section in betslip_sections.items():
                _make_stake_odds_dict(section)

        self._logger.info(f'*** Current odds "{betslip_prices}"')
        return betslip_prices

    def check_bet_receipt(self, betslip_info, each_way=False, sp=False, freebet=False, forecast_tricast=False, **kwargs):
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        for section_name, section in betreceipt_sections.items():
            receipts = section.items_as_ordered_dict
            self.assertTrue(receipts, msg='No Receipt legs found')
            market_type = []
            if section_name != vec.betslip.SINGLE:
                self.__class__.bet_id = section.bet_id
                self._logger.info(f'*** Bet receipt id "{self.bet_id}" and name type "{section_name}"')
                total_stake = section.total_stake
                betslip_bet = betslip_info[section.multiple_bet_type]['bet_amount'] * section.bet_multiplier
                self.assertAlmostEqual(float(total_stake),
                                       betslip_bet,
                                       delta=0.015,
                                       msg=f'Total stake "{total_stake}" is not the same as on betslip "{betslip_bet}" '
                                       f'within 0.015 delta')
                est_returns = section.estimate_returns
                betslip_est_returns = betslip_info[section.multiple_bet_type]['estimate_returns']
                if betslip_est_returns == 'N/A':
                    self.assertEqual(est_returns, betslip_est_returns,
                                     msg=f'Estimate return on Bet Receipt "{est_returns}" doesn\'t match estimate returns '
                                         f'on Bet Slip "{betslip_est_returns}"')
                else:
                    self.assertAlmostEqual(float(est_returns), betslip_est_returns,
                                           delta=0.015,
                                           msg=f'Estimate return on Bet Receipt "{est_returns}" doesn\'t match estimate returns '
                                               f'on Bet Slip "{betslip_est_returns}" within 0.015 delta')
                self._logger.info(f'*** Total stake: "{total_stake}", est returns: "{est_returns}"')
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                self._logger.info(f'*** Receipt name "{receipt_name}" has type "{receipt_type}"')
                if receipt_type == 'ReceiptSingles':
                    # TODO: fix comparison of stake values on betslip and betreceipt:
                    # TODO:(now stake 1 on betslip can be compared to stake 2 on receipt)
                    outcome_name = receipt_name
                    event_name = receipt.event_name
                    self.assertEqual(event_name, next(iter(betslip_info.values()))['event_name'].strip(),
                                     msg='Event name on bet receipt "%s" is not the same as on Bet Slip "%s"'
                                         % (event_name, next(iter(betslip_info.values()))['event_name'].strip()))
                    self.__class__.bet_id = receipt.bet_id
                    self.assertTrue(self.bet_id is not None, msg='Bet id on Bet Receipt is empty')

                    odds = receipt.odds if not sp else 'SP'
                    if not forecast_tricast:
                        self.assertEqual(odds, next(iter(betslip_info.values()))['odds'],
                                         msg='Odds on bet receipt "%s" is not the same as on BetSlip "%s"'
                                             % (odds, next(iter(betslip_info.values()))['odds']))

                    market = normalize_name(receipt.event_market_name.replace(' /', '').replace('-', ' '))
                    market_type.append(market)
                    if (market.upper() == "MATCH RESULT"):
                        self.assertTrue(
                            next(iter(betslip_info.values()))['market_name'].upper() in [market.upper(), "MATCH BETTING"])
                    else:
                        self.assertEqual(market, next(iter(betslip_info.values()))['market_name'],
                                         msg='Market name on bet receipt "%s" is not the same as on Bet Slip "%s"'
                                             % (market, next(iter(betslip_info.values()))['market_name']))
                    if each_way:
                        ew_terms = receipt.ew_terms
                        self.assertTrue(ew_terms is not None and ew_terms != '',
                                        msg='Each way terms is not found in bet receipt')
                    total_stake = receipt.free_bet_stake if freebet else receipt.total_stake
                    self.assertTrue(float(total_stake) is not None, msg='Total stake is None')
                    est_returns = 'N/A' if receipt.estimate_returns == 'N/A' else float(receipt.estimate_returns)
                    if next(iter(betslip_info.values()))['estimate_returns'] != 'N/A':
                        self.assertAlmostEqual(est_returns, next(iter(betslip_info.values()))['estimate_returns'], delta=0.015,
                                               msg='Estimate return on Bet Receipt "%s" is not the same as '
                                                   'on Bet Slip "%s"' % (
                                                   est_returns, next(iter(betslip_info.values()))['estimate_returns']))
                    self._logger.info('*** Name: "%s", bet id: "%s", event name: "%s", event market: "%s", '
                                      'odds: "%s", total stake: "%s", est returns: "%s"'
                                      % (outcome_name, self.bet_id, event_name,
                                         market_type, odds, total_stake, est_returns))
                elif receipt_type == 'ReceiptMultiples':
                    self._logger.info(f'*** Multiples section header: {receipt.name}')
                    market_type.append(normalize_name(receipt.market_type[:-2]))
                    self._logger.info(f'*** Market type "{market_type}"')
                    self._logger.info(f'*** Multiples receipt leg items: {receipt.event_description}')

            stake_name = kwargs.get('stake_name')
            if stake_name:
                betslip_markets = betslip_info[stake_name]['market_name']
            else:
                betslip_markets = [bet['market_name'] for bet_name, bet in betslip_info.items()
                                   if bet_name not in ['Patent', 'Treble', 'Double', 'Single Stakes About (3)', 'Trixie', 'Round Robin', 'Flag', 'Single Stakes About',
                                                       'Double Stakes About', 'total_stake', 'total_estimate_returns']]
            if self.site.brand == "ladbrokes":
                market_type_modified = []
                for x in market_type:
                    market_type_modified.append(x.replace("Match Result", "Match Betting"))
                market_type = market_type_modified
            else:
                market_type_modified = []
                for x in market_type:
                    market_type_modified.append(x.replace("Not to Nil", "and Both Teams to Score"))
                market_type = market_type_modified
            self.assertListEqual(sorted(market_type), sorted(betslip_markets),
                                 msg=f'Markets on betreceipt "{sorted(market_type)}" and betslip '
                                 f'"{sorted(betslip_markets)}" are not the same')
            footer = self.site.bet_receipt.footer
            total_stake = footer.total_stake
            total_est_returns = footer.total_estimate_returns
            self.__class__.total_stake_betreceipt = float(total_stake.replace(',', ''))
            self._logger.info(f'*** Total stake {self.total_stake_betreceipt}, total est returns {total_est_returns}')
            self.assertEqual(betslip_info['total_stake'], self.total_stake_betreceipt,
                             msg=f'Total stake on betslip {betslip_info["total_stake"]} doesn\'t match with total '
                             f'stake on betreceipt {self.total_stake_betreceipt}')

    def check_bet_sorting_types(self, tab=vec.bet_history.OPEN_BETS_TAB_NAME, expected_active_btn=None):
        expected_sorting_types_btns = self.expected_sorting_types_btns_open_bets if tab == vec.bet_history.OPEN_BETS_TAB_NAME \
            else self.expected_sorting_types_btns_settled_bets
        if not expected_active_btn:
            expected_active_btn = self.expected_active_btn_open_bets if tab == vec.bet_history.OPEN_BETS_TAB_NAME \
                else self.expected_active_btn_settled_bets

        sorting_types_btns = self.site.bet_history.grouping_buttons.items_as_ordered_dict
        active_btn = self.site.bet_history.grouping_buttons.current
        self.assertEqual(len(sorting_types_btns), len(expected_sorting_types_btns),
                         msg=f'The number of sorting type buttons do not match, '
                         f'"{len(sorting_types_btns)}" != "{len(expected_sorting_types_btns)}"')
        self.assertListEqual(list(sorting_types_btns.keys()), expected_sorting_types_btns)
        self.assertEqual(active_btn, expected_active_btn,
                         msg=f'"{expected_active_btn}" sorting type is not selected by default, '
                         f'current active sorting type is: "{active_btn}"')

    def check_bet_receipt_is_displayed(self, timeout=5, poll_interval=0.5):
        result = wait_for_result(lambda: self.site.is_bet_receipt_displayed(timeout=3),
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name='Bet Receipt is shown after clicking "Bet Now" button')
        self.assertTrue(result, msg='Bet receipt is not displayed')

    def enter_value_using_keyboard(self, value, on_betslip=True):
        keyboard = self.get_betslip_content().keyboard if on_betslip \
            else self.site.quick_bet_panel.selection.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=value)

    def clear_input_using_keyboard(self, value=None, on_betslip=True):
        keyboard = self.get_betslip_content().keyboard if on_betslip \
            else self.site.quick_bet_panel.selection.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        value = len(str(value)) if value else self.max_number_of_symbols_in_stake_input
        for i in range(0, value):
            keyboard.enter_amount_using_keyboard(value='delete', delay=0.5)

    def clear_betslip(self):
        betslip_content = self.get_betslip_content()

        if self.brand == 'ladbrokes':
            # sometimes top msg can block btn to clear betslip, so need to wait until it disappear
            if betslip_content.wait_for_top_notification(timeout=1):
                betslip_content.top_notification.wait_for_error(expected_result=False, timeout=6)

        betslip_content.remove_all_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_REMOVE_ALL}" dialog is not shown')
        dialog.click_continue()
        self.assertTrue(dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_REMOVE_ALL}" popup not closed')
        self.__class__.expected_betslip_counter_value = 0
        self.__class__._betslip_content = None
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
        else:
            betslip = self.get_betslip_content()
            no_selections_title = betslip.no_selections_title
            self.assertTrue(no_selections_title, msg=f'"{vec.betslip.NO_SELECTIONS_TITLE}" title is not shown')

    def select_free_bet(self, free_bet_name=None):
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is not shown')
        if free_bet_name:
            dialog.select_free_bet(free_bet_name=free_bet_name)
        else:
            free_bet_name = dialog.select_first_free_bet()
        self.assertTrue(dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" '
                                                         f'dialog is not closed')

        free_bet_value = re.search(r'\d+.\d+\d+', free_bet_name)
        self.assertTrue(free_bet_value, msg=f'Could not extract free bet value from free bet name {free_bet_name}')

        return free_bet_value.group()

    def _verify_top_notification(self, expected_message, is_started=False):
        actual_top_message = self.get_betslip_content().top_notification.wait_for_error(timeout=60)
        msg_to_verify = vec.betslip.EVENT_STARTED if is_started else expected_message
        self.assertEqual(actual_top_message, msg_to_verify,
                         msg=f'Error message "{actual_top_message}" != expected "{msg_to_verify}"')
        self.assertFalse(self.get_betslip_content().top_notification.wait_for_error(expected_result=False,
                                                                                    timeout=6),
                         msg=f'Betslip top error message did not disappear')

    def _verify_event_is_started_notification(self, stake):

        result = wait_for_result(lambda: stake.wait_for_error_message(timeout=0) == vec.betslip.EVENT_STARTED,
                                 name=f'Stake error message to be "{vec.betslip.EVENT_STARTED}"',
                                 timeout=30)
        self.assertTrue(result,
                        msg=f'Actual message "{stake.wait_for_error_message(timeout=0)}" != expected message "{vec.betslip.EVENT_STARTED}"')

    def verify_betslip_is_suspended(self, stakes: List['BetslipStake'], timeout: int = 40, **kwargs):
        """
        This method verifies situation when Betslip content is suspended, it includes the following:
            - All single betslip stakes are suspended and their 'stake' fields are disabled
            - BetSlip button is disabled
            - Error message is displayed at the bottom of betslip
        In additional for ladbrokes:
            - Message is displayed at the top of the betslip with duration: 5s
        :param stakes: Stakes to verify
        :param timeout: timeout waiting for error message
        :param kwargs: accepts:
            - verify_overlay_message: Specifies situation, when top overlay notification message should be verified,
                it's related only to Ladbrokes, True - enable verification, False - disable verification
            - is_started: Specifies situation when event is not just suspended, but already started,
                related mostly to racing events
        """
        is_multiple = len(stakes) > 1
        verify_overlay_message = kwargs.get('verify_overlay_message', True)
        is_started = kwargs.get('is_started', False)

        if self.brand != 'bma':
            expected_message = vec.betslip.BELOW_MULTIPLE_DISABLED if is_multiple else vec.betslip.SINGLE_DISABLED
        else:
            expected_message = vec.betslip.MULTIPLE_DISABLED if is_multiple else vec.betslip.SINGLE_DISABLED
        if verify_overlay_message and self.brand == 'ladbrokes':
            self._verify_top_notification(expected_message=expected_message, is_started=is_started)

        result = self.get_betslip_content().wait_for_specified_error(expected_message=expected_message,
                                                                     timeout=timeout)
        self.assertTrue(result,
                        msg=f'Error message "{self.get_betslip_content().error}" != expected "{expected_message}"')

        for stake in stakes:
            self.assertTrue(stake.is_suspended(timeout=5), msg=f'Stake is not suspended')
            self.assertFalse(stake.amount_form.input.is_enabled(expected_result=False, timeout=5),
                             msg=f'Stake amount input field for suspended event "{stake.event_name}" is not disabled')
            if is_started and self.brand == 'bma':
                self._verify_event_is_started_notification(stake)

        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not disabled')

    def verify_betslip_is_active(self, stakes: List['BetslipStake'], is_stake_filled: bool, timeout: int = 40):
        """
        This method verifies situation when Betslip content is active, it includes the following:
            - All single betslip stakes are active and their 'stake' fields are enabled
            - If stake field contains filled stake BetSlip button is expected to be enabled, otherwise - disabled
            - No Betslip errors are available
        :param stakes: Stakes to verify
        :param is_stake_filled: Indicate whether stake field is filled by value,
                                this means that BetSlip button is expected to be enabled, otherwise - disabled
        :param timeout: timeout waiting for stake to be enabled
        """
        for stake in stakes:
            self.assertFalse(stake.is_suspended(expected_result=False, timeout=timeout), msg=f'Stake is not active')
            self.assertTrue(stake.amount_form.input.is_enabled(expected_result=True, timeout=5),
                            msg=f'Stake amount input field for suspended event "{stake.event_name}" is not enabled')

        result = self.get_betslip_content().bet_now_button.is_enabled(
            expected_result=is_stake_filled, timeout=3) == is_stake_filled
        self.assertTrue(result, msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button '
                                    f'status was expected to be "{is_stake_filled}"')

        error = self.get_betslip_content().error
        self.assertFalse(error, msg=f'Warning message "{error}" still shown in the bottom of Betslip')

        if self.brand == 'ladbrokes':
            self.assertFalse(self.get_betslip_content().top_notification.wait_for_error(expected_result=False,
                                                                                        timeout=1),
                             msg=f'Betslip top error message did not disappear')

    def get_overask_trader_offer(self) -> str:
        """
        Method to get 'traderOfferNotificationMessage' from Overask system config
        :return: str
        """
        overask_system_config = self.get_initial_data_system_configuration().get('Overask')
        if not overask_system_config:
            overask_system_config = self.cms_config.get_system_configuration_item('Overask')
        if overask_system_config is None:
            return ''
        trader_message = overask_system_config.get('traderOfferNotificationMessage').strip()
        return trader_message

    def get_overask_expires_message(self) -> str:
        """
        Method to get 'traderOfferExpiresMessage' from Overask system config
        :return: str
        """
        overask_system_config = self.get_initial_data_system_configuration().get('Overask')
        if not overask_system_config:
            overask_system_config = self.cms_config.get_system_configuration_item('Overask')
        if overask_system_config is None:
            return ''
        trader_message = overask_system_config.get('traderOfferExpiresMessage')
        return trader_message

    def place_single_bet_on_cashout_selection(self, selection_name=None, selection_id=None, category_id=None):
        """
        asdfghjkl
        """
        if not selection_id:
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            selection = self.get_active_event_selections_for_category(
                category_id=category_id if category_id else self.ob_config.football_config.category_id,
                additional_filters=cashout_filter)

            selection_name, selection_id = next(iter(selection.items()))

        if not self.is_browser_opened or self.site.header.has_log_in_button():
            self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_id)
        bet_info = self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        bet_info['selection_name'] = selection_name
        return bet_info
