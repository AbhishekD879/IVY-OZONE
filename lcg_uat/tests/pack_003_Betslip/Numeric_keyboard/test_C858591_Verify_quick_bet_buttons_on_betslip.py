import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
# @pytest.mark.crl_stg2
@pytest.mark.crl_prod  # Coral only (Quick Stakes are not available in ladbrokes)
@pytest.mark.crl_hl
@pytest.mark.numeric_keyboard
@pytest.mark.quick_stake
@pytest.mark.quick_stake_buttons
@pytest.mark.bet_placement
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C858591_Verify_quick_bet_buttons(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C858591
    VOL_ID: C9697750
    NAME: Verify 'Quick Stakes' buttons on bet slip keyboard
    DESCRIPTION: This test case verifies 'Quick Stakes' buttons on bet slip keyboard for £/$/€ currencies
    """
    keep_browser_open = True
    username = None
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    user_currency_sign = None
    betnow_section = None
    quick_stake_keys = None
    usd_currency = u'+$'
    eur_currency = u'+€'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,all_available_events=True)
            for event in events:
                market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
                outcomes = market['market']['children']
                self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                             outcome['outcome'].get('outcomeMeaningMinorCode') and
                                             outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
                if self.team1:
                    break
            else:
                 raise SiteServeException('No Home team found')
                 self._logger.info(f'*** Found selections: {self.selection_ids}')
        else:
            params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = params.team1, params.selection_ids

    def test_001_log_in(self, username=None):
        """
        DESCRIPTION: Log in
        EXPECTED: User is successfully logged in
        """
        username = username if username else tests.settings.betplacement_user

        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_one_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add one selection to Bet Slip
        EXPECTED: Bet Slip slide is opened
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1]))

    def test_003_verify_betslip_elements(self, currency=u'+£'):
        """
        DESCRIPTION: Verify Bet Slip elements
        EXPECTED: 'Singles (1)' section with added selection is displayed
        """
        number_of_stakes = self.get_betslip_content().selections_count
        self.assertEqual(number_of_stakes, '1', msg=f'Singles selections count is "{number_of_stakes}" not "1"')
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertEqual(len(self.singles_section.items()), 1, msg='Only one Stake must be found in betslip Singles '
                                                                   'section')
        self.__class__.stake = list(self.zip_available_stakes(section=self.singles_section,
                                                              number_of_stakes=1).items())[0]

    def test_004_verify_quick_bet_buttons(self, currency=u'+£'):
        """
        DESCRIPTION: Set focus on the 'Stake' field. Verify if all buttons are shown with '+' sign
        EXPECTED: Keyboard with 'Quick stakes' buttons are displayed with correct text:
        """
        self.stake[1].amount_form.click()
        self.__class__.quick_stake_keys = self.get_betslip_content().betnow_section.quick_stake_panel.items_as_ordered_dict
        for stake in self.quick_stakes:
            expected_key = currency + str(stake)
            self.assertIn(expected_key, self.quick_stake_keys,
                          msg=f'"{expected_key}" not found in "{self.quick_stake_keys.keys()}"')

    def test_005_verify_each_quick_bet_button(self, currency=u'+£'):
        """
        DESCRIPTION: Tap each button
        EXPECTED: Correct Value  is added to 'Stake' field
        EXPECTED: 'Est. Returns' value is calculated according to added value
        """
        for self.__class__.bet_amount in self.quick_stakes:
            self.quick_stake_keys[currency + str(self.bet_amount)].click()
            wait_for_result(lambda: self.stake[1].est_returns != '0.00',
                            name='est returns was changed',
                            timeout=1)
            params = self.collect_stake_info(stake=self.stake)
            stake_value = params['bet_amount']
            self.assertEqual(stake_value, self.bet_amount,
                             msg=f'Amount in stake input field "{stake_value}" doesn\'t match expected '
                                 f'"{self.bet_amount}" for user with "{currency}"" currency')

            # We need such big delta for bet with 50 and 100 amount + odds changing on prod envs
            self.verify_estimated_returns(est_returns=params['estimate_returns'], odds=params['odds'],
                                          bet_amount=params['bet_amount'], delta=0.5)
            self.clear_input_using_keyboard()

    def test_006_verify_few_quick_bet_buttons(self, currency=u'+£'):
        """
        DESCRIPTION: Add several amounts from 'Quick stakes' buttons
        EXPECTED: Amounts on the 'Stake' field are added. Sum of all entered 'quick stake' amounts are shown
        """
        for self.__class__.bet_amount in self.quick_stakes:
            self.quick_stake_keys[currency + str(self.bet_amount)].click()
            self.__class__.bet_amount += self.bet_amount
            params = self.collect_stake_info(stake=self.stake)
            stake_value = params['bet_amount']
            self.assertEqual(stake_value, self.bet_amount, msg=f'Amount in stake input field "{stake_value}" '
                                                               f'doesn\'t match expected "{self.bet_amount}"')

    def test_007_enter_stake_manually_and_tap_quick_bet_button(self, currency=u'+£'):
        """
        DESCRIPTION: Enter any amount manually from keyboard and tap on the any 'quick stakes' button
        EXPECTED: Quick stake value is added on top of entered manually value. Sum of entered amount is shown
        """
        quick_bet_value = self.quick_stakes[0]
        self.__class__.bet_amount = quick_bet_value + self.bet_amount
        self.enter_value_using_keyboard(value=self.bet_amount)
        self.quick_stake_keys[currency + str(quick_bet_value)].click()
        params = self.collect_stake_info(stake=self.stake)
        stake_value = params['bet_amount']
        self.assertEqual(stake_value, self.bet_amount, msg=f'Amount in stake input field "{stake_value}" '
                                                           f'doesn\'t match expected "{self.bet_amount}"')
        self.clear_input_using_keyboard()

    def test_008_tap_quick_bet_button_and_enter_stake_manually(self, currency=u'+£'):
        """
        DESCRIPTION: Enter any amount from 'quick stakes' buttons and then enter any amount from keyboard
        EXPECTED: Manually entered stake overwrites the previously selected quick stake value
        """
        self.__class__.bet_amount = 0.05
        quick_bet_value = self.quick_stakes[0]
        self.quick_stake_keys[currency + str(quick_bet_value)].click()
        self.enter_value_using_keyboard(value=self.bet_amount)
        params = self.collect_stake_info(stake=self.stake)
        stake_value = params['bet_amount']
        self.assertEqual(stake_value, self.bet_amount, msg=f'Amount in stake input field "{stake_value}" '
                                                           f'doesn\'t match expected "{self.bet_amount}"')

    def test_009_click_bet_now(self):
        """
        DESCRIPTION: Click 'Bet Now' button
        EXPECTED: Bet is placed successfully
        EXPECTED: Bet Receipt is displayed
        EXPECTED: Balance is reduced accordingly
        """
        expected_user_balance = self.user_balance - self.bet_amount
        self.get_betslip_content().betnow_section.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.site.logout()

    def test_010_repeat_all_steps_for_user_with_usd_currency(self):
        """
        DESCRIPTION: Perform all actions and verifications for user with USD currency ($)
        """
        self.test_001_log_in(username=tests.settings.user_with_usd_currency_and_card)
        self.test_002_add_one_selection_to_bet_slip()
        self.test_003_verify_betslip_elements(currency=self.usd_currency)
        self.test_004_verify_quick_bet_buttons(currency=self.usd_currency)
        self.test_005_verify_each_quick_bet_button(currency=self.usd_currency)
        self.test_006_verify_few_quick_bet_buttons(currency=self.usd_currency)
        self.test_007_enter_stake_manually_and_tap_quick_bet_button(currency=self.usd_currency)
        self.test_008_tap_quick_bet_button_and_enter_stake_manually(currency=self.usd_currency)
        self.test_009_click_bet_now()

    def test_011_repeat_all_steps_for_user_with_eur_currency(self):
        """
        DESCRIPTION: Perform all actions and verifications for user with EUR currency (€)
        """
        self.test_001_log_in(username=tests.settings.user_with_euro_currency_and_card)
        self.test_002_add_one_selection_to_bet_slip()
        self.test_003_verify_betslip_elements(currency=self.eur_currency)
        self.test_004_verify_quick_bet_buttons(currency=self.eur_currency)
        self.test_005_verify_each_quick_bet_button(currency=self.eur_currency)
        self.test_006_verify_few_quick_bet_buttons(currency=self.eur_currency)
        self.test_007_enter_stake_manually_and_tap_quick_bet_button(currency=self.eur_currency)
        self.test_008_tap_quick_bet_button_and_enter_stake_manually(currency=self.eur_currency)
        self.test_009_click_bet_now()
