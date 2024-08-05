import pytest
import tests
import voltron.environments.constants as vec
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C29068_Betslip_Reflection_on_Sport_Price_Changed(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C29068
    VOL_ID: C9698104
    NAME: Betslip reflection on <Sport> Price Changed
    """
    keep_browser_open = True
    prices = OrderedDict([('odds_home', '1/2'),
                          ('odds_draw', '1/3'),
                          ('odds_away', '4/1')])
    section_name = tests.settings.football_autotest_league
    output_prices_values_dict = {}
    new_output_prices_values_dict = {}
    new_price_home = '15/1'
    new_price2_home = '17/1'
    new_price_draw = '1/17'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        start_time = self.get_date_time_formatted_string(seconds=10)
        self.__class__.event_info = self.ob_config.add_autotest_premier_league_football_event(is_live=True, lp=self.prices,
                                                                                              start_time=start_time)

        self.__class__.team1, self.__class__.selection_ids = self.event_info.team1, self.event_info.selection_ids
        self.__class__.initial_output_prices_dict = {self.team1: self.ob_config.event.prices['odds_home'],
                                                     'Draw': self.ob_config.event.prices['odds_draw'],
                                                     self.event_info.team2: self.ob_config.event.prices['odds_away']}
        self.__class__.created_event_name = self.event_info.team1 + ' v ' + self.event_info.team2

    def test_001_add_selections_to_betslip(self):
        """
        DESCRIPTION: Add selections to Betslip
        """
        self.open_betslip_with_selections(selection_ids=list(self.event_info.selection_ids.values()))

    def test_002_check_betslip_counter(self):
        """
        DESCRIPTION: Check BetSlip counter
        """
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get(self.team1)
        self.assertTrue(self.stake, msg=f'"{self.team1}" stake was not found on the Betslip')

    def test_003_change_price_for_selection(self):
        """
        DESCRIPTION: Change output price of Home selection (increase price)
        """
        self.__class__.outcome = self.selection_ids[self.team1]
        self.ob_config.change_price(selection_id=self.outcome, price=self.new_price_home)

    def test_004_verify_error_message_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: The selection price change is displayed via push
        EXPECTED: Notification box is displayed at the bottom of the betslip
        EXPECTED: Notification box is displayed at the top of the betslip with animations - this is removed after 5 seconds
        EXPECTED: 'Log In & Bet' button is disabled
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.outcome, price=self.new_price_home)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.team1}" with id "{self.outcome}" is not received')

        general_error_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(general_error_msg, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual error message: "{general_error_msg}" '
                             f'is not equal to expected: "{vec.betslip.PRICE_CHANGE_BANNER_MSG}"')

        error = self.stake.error_message
        expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(
            old=self.initial_output_prices_dict[self.team1], new=self.new_price_home)
        self.assertEqual(error, expected_error,
                         msg=f'Received error "{error}" is not the same as expected "{expected_error}"')

        betnow_button = self.get_betslip_content().bet_now_button
        self.assertEqual(betnow_button.name, vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Found "{betnow_button.name}" button name, expected "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        self.assertFalse(betnow_button.is_enabled(expected_result=False), msg='Bet Now button is not disabled')

    def test_005_close_and_open_betslip_again(self):
        """
        DESCRIPTION: Close and open betslip and verify odds
        EXPECTED: Updated Odds are still displaying
        """
        if self.device_type == 'mobile':
            self.get_betslip_content().close_button.click()
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
            self.site.header.bet_slip_counter.click()
            self.assertTrue(self.site.has_betslip_opened(expected_result=True), msg='Betslip is not opened')
        else:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section[self.team1] if self.team1 in singles_section else None
        self.assertTrue(self.stake, msg=f'No stake with name "{self.team1}" found')
        betslip_prices_current = self.get_price_odds_on_betslip(section=singles_section)
        self._logger.debug('*** Odds on sport page %s' % self.initial_output_prices_dict)
        self._logger.debug('*** Odds on betslip %s' % betslip_prices_current)
        self.assertEqual(betslip_prices_current[self.team1], self.new_price_home)

    def test_006_enter_stake_and_trigger_price_update(self):
        """
        DESCRIPTION: Enter stake and trigger price update
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: 'Log In & Bet' button becomes enabled
        """
        self.stake.amount_form.input.value = 1
        self.ob_config.change_price(selection_id=self.outcome, price=self.new_price2_home)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.outcome, price=self.new_price2_home)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.team1}" with id "{self.outcome}" is not received')

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get(self.team1)
        self.assertTrue(self.stake, msg=f'No stake with name "{self.team1}" found')

        betslip_prices_current = self.get_price_odds_on_betslip(section=singles_section)
        self._logger.debug('*** Odds on sport page %s' % self.initial_output_prices_dict)
        self._logger.debug('*** Odds on betslip %s' % betslip_prices_current)
        self.assertEqual(betslip_prices_current[self.team1], self.new_price2_home)

        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(timeout=5),
                        msg='Bet Now button is not enabled')

    def test_007_login_with_user_with_positive_balance(self):
        """
        DESCRIPTION: Login with user with positive balance
        EXPECTED: User is logged in
        """
        self.site.close_betslip()
        self.site.login(async_close_dialogs=False)
        self.site.header.bet_slip_counter.click()
        self.assertTrue(self.site.has_betslip_opened(expected_result=True), msg='Betslip is not opened')

    def test_008_repeat_steps_for_logged_in_user_change_price_for_draw_selection(self):
        """
        DESCRIPTION: Repeat steps for logged in user
        """
        self.__class__.outcome2 = self.selection_ids['Draw']
        self.ob_config.change_price(selection_id=self.outcome2, price=self.new_price_draw)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.outcome2)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "Draw" with id "{self.outcome2}" is not received')

    def test_009_verify_general_error_message(self):
        """
        DESCRIPTION: Verify general error message in Betslip
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.outcome2)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "Draw" with id "{self.outcome2}" is not received')
        general_error_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(general_error_msg, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual error message: "{general_error_msg}" '
                             f'is not equal to expected: "{vec.betslip.PRICE_CHANGE_BANNER_MSG}"')

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get('Draw')
        error = self.stake.error_message
        expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(
            old=self.prices['odds_draw'], new=self.new_price_draw)
        self.assertEqual(error, expected_error,
                         msg=f'Received error "{error}" is not the same as expected "{expected_error}"')

        self.assertTrue(self.stake, msg=f'No stake with name "Draw" found')

        betslip_prices_current = self.get_price_odds_on_betslip(section=singles_section)
        self._logger.debug('*** Odds on sport page %s' % self.initial_output_prices_dict)
        self._logger.debug('*** Odds on betslip %s' % betslip_prices_current)
        self.assertEqual(betslip_prices_current['Draw'], self.new_price_draw)

    def test_010_verify_accept_and_bet_button(self):
        """
        DESCRIPTION: Verify Bet Now button
        EXPECTED: Bet Now button should read as 'Accept and Bet'
        """
        betnow_button = self.get_betslip_content().bet_now_button
        self.assertEqual(betnow_button.name, vec.betslip.ACCEPT_BET,
                         msg=f'Found "{betnow_button.name}" button name, expected "{vec.betslip.ACCEPT_BET}"')
        self.assertTrue(betnow_button.is_enabled(timeout=5), msg='Bet Now button is disabled')
