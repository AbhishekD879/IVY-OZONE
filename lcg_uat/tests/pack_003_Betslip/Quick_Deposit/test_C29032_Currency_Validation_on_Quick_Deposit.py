import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.creditcard
@pytest.mark.desktop
@pytest.mark.currency
@pytest.mark.medium
@pytest.mark.slow
@vtest
class Test_C29032_Currency_Validation_on_Quick_Deposit(BaseBetSlipTest):
    """
    TR_ID: 29032
    NAME: Currency Validation on Quick Deposit
    DESCRIPTION: This test case verifies Currency in the Quick Deposit section
    DESCRIPTION: and on Quick Deposit Validation messages in Betslip
    PRECONDITIONS: Four User accounts with different currencies (GBP, EUR, USD, SEK) and registered credit card
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**;
    PRECONDITIONS: *   'SEK': symbol = '**Kr**'
    """
    keep_browser_open = True
    addition = 5.00
    selection_name = ''
    min_deposit_error = vec.Quickdeposit.MIN_DEPOSIT_ERROR
    min_deposit_for_bet_message = vec.Quickdeposit.EXPECTED_MIN_DEPOSIT_FOR_BET_MESSAGE_CURRENCY

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        self.__class__.event_params = self.ob_config.add_american_football_event_to_ncaa_bowls()
        self.__class__.selection_name = self.event_params.team1
        self.__class__.event_name = f'{self.event_params.team1} v {self.event_params.team2}'

    def test_001_log_in_with_user_account_from_preconditions(self, username=None):
        """
        DESCRIPTION: Log in with user account (from preconditions)
        EXPECTED: User is logged in
        """
        username = tests.settings.betplacement_user_small_balance if username is None else username
        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_any_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add any selection to the Bet Slip -> go to the Bet Slip page/widget
        EXPECTED: Made selection is displayed correctly within Bet Slip content area
        """
        self.navigate_to_edp(event_id=self.event_params.event_id)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg=f'No one market section found on event: "{self.event_name}" EDP')
        market = markets.get(self.expected_market_sections.money_line)
        self.assertTrue(market,
                        msg=f'Market: "{self.expected_market_sections.money_line}" '
                            f'section not found in: {list(markets.keys())}')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes,
                        msg=f'No one outcome found in market: "{self.expected_market_sections.money_line}" section')
        team1 = self.event_params.team1.upper() if self.brand == 'ladbrokes' else self.event_params.team1
        self.assertIn(team1, outcomes, msg=f'"{team1}" is not displayed in markets')
        outcomes[team1].bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.site.header.bet_slip_counter.click()
        self.assertTrue(self.get_betslip_content(),
                        msg='Betslip widget was not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No one added selection found on Betslip')
        self.__class__.stake = singles_section.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found on the Betslip')

    def test_003_enter_stake_amount_greater_than_current_users_balance(self, currency='£'):
        """
        DESCRIPTION: Enter 'Stake' amount greater than current user's balance
        EXPECTED: 'GBP' currency is displayed next to:
        EXPECTED: 'Please deposit a min £XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip
        EXPECTED: where, 'XX.XX' - the difference between entered stake value and users balance
        """
        self.__class__.bet_amount = self.user_balance + self.addition
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        expected_message = self.min_deposit_for_bet_message.format(currency, '{0:.2f}'.format(self.addition))
        if self.brand == 'bma':
            self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"QUICK DEPOSIT" was not found')
            actual_message = self.get_betslip_content().quick_deposit.info_panels_text[0]
            self.assertEqual(actual_message, expected_message,
                             msg=f'Actual message: "{actual_message}" does not match expected: "{expected_message}"')
        elif self.brand == 'ladbrokes':
            result = self.get_betslip_content().bet_amount_warning_message
            self.assertEqual(result, expected_message, msg=f'Current message "{result}" '
                                                           f'is not equal to expected: "{expected_message}"')
        actual_stake_amount = self.stake.amount_form.input.value
        expected_stake_amount = '{0:.2f}'.format(self.bet_amount)
        self.assertEqual(actual_stake_amount, expected_stake_amount,
                         msg=f'Actual stake input amount: "{actual_stake_amount}", expected: "{expected_stake_amount}"')

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is displayed at the bottom of the Bet Slip with all content
        EXPECTED: - 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        """
        self.assertEqual(self.get_betslip_content().make_quick_deposit_button.name, vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION,
                         msg=f'"{self.get_betslip_content().make_quick_deposit_button.name}" is no the same as '
                             f'expected "{vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION}"')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().quick_deposit.is_expanded(),
                        msg='"Quick Deposit" section not displayed')
        self.assertFalse(self.get_betslip_content().has_make_quick_deposit_button(expected_result=False),
                         msg=f'"{vec.Quickdeposit.DEPOSIT_AND_PLACEBET_BUTTON_CAPTION}" still displayed')

    def test_005_verify_currency_set_within_quick_deposit_section(self, currency='£'):
        """
        DESCRIPTION: Verify currency set within Quick Deposit section
        EXPECTED: GBP' currency is displayed next to:
        EXPECTED: * 'Please deposit a min £XX.XX to continue placing your bet' error message
        EXPECTED: * 'Deposit Amount' field
        EXPECTED: where,
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        """
        expected_message_text = self.min_deposit_for_bet_message.format(currency, '{0:.2f}'.format(self.addition))
        message_text = self.get_betslip_content().quick_deposit.warning_panel.text
        self.assertEqual(message_text, expected_message_text,
                         msg=f'Info panel message {message_text} '
                             f'is not the same as expected {expected_message_text}')

    def test_006_enter_invalid_amount_into_amount_field_less_than_5_and_tap_deposit_place_bet_button(self, currency='£'):
        """
        DESCRIPTION: Enter invalid amount into 'Amount' field (less than 5) and tap 'DEPOSIT & PLACE BET'  button
        EXPECTED: Error message  'The minimum deposit amount is **£** **5/50.**' is displayed under 'Amount' field
        """
        self.get_betslip_content().quick_deposit.amount_form.input.value = 1.0
        self.get_betslip_content().quick_deposit.cvv.click()
        self.get_betslip_content().quick_deposit.enter_cvv(value=121)
        self.get_betslip_content().deposit_and_place_bet_button.click()
        actual_amount_validation_error = self.get_betslip_content().quick_deposit.amount_validation_error
        self.assertEqual(actual_amount_validation_error, self.min_deposit_error.format(currency=currency),
                         msg=f'Actual error text "{actual_amount_validation_error}", '
                             f'expected: "{self.min_deposit_error.format(currency=currency)}"')

    def test_007_logout(self):
        """
        DESCRIPTION: Close Betslip and Log Out
        EXPECTED: Betslip closed
        """
        self.clear_betslip()
        self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
        self.site.logout()

    def test_008_repeat_steps_1_7_for_accounts_with_different_currencies(self):
        """
        DESCRIPTION: Repeat steps №1-7 for
        DESCRIPTION: *   'USD': symbol = **$**;
        DESCRIPTION: *   'EUR': symbol = **€**;
        DESCRIPTION: *   'SEK': symbol = **Kr**
        """
        # Repeat steps №1-7 for Accounts with USD currency
        self.test_001_log_in_with_user_account_from_preconditions(
            username=tests.settings.user_with_usd_currency_and_card)
        self.test_002_add_any_selection_to_the_bet_slip()
        self.test_003_enter_stake_amount_greater_than_current_users_balance(currency='$')
        self.test_004_tap_make_a_deposit_button()
        self.test_005_verify_currency_set_within_quick_deposit_section(currency='$')
        self.test_006_enter_invalid_amount_into_amount_field_less_than_5_and_tap_deposit_place_bet_button(currency='$')
        self.test_007_logout()
        # Repeat steps №1-7 for Accounts with EUR currency
        self.test_001_log_in_with_user_account_from_preconditions(
            username=tests.settings.user_with_euro_currency_and_card)
        self.test_002_add_any_selection_to_the_bet_slip()
        self.test_003_enter_stake_amount_greater_than_current_users_balance(currency='€')
        self.test_004_tap_make_a_deposit_button()
        self.test_005_verify_currency_set_within_quick_deposit_section(currency='€')
        self.test_006_enter_invalid_amount_into_amount_field_less_than_5_and_tap_deposit_place_bet_button(currency='€')
        self.test_007_logout()
        # Repeat steps №1-7 for Accounts with SEK currency
        if self.brand != 'ladbrokes':
            self.test_001_log_in_with_user_account_from_preconditions(
                username=tests.settings.user_with_sek_currency_and_card)
            self.test_002_add_any_selection_to_the_bet_slip()
            self.test_003_enter_stake_amount_greater_than_current_users_balance(currency='Kr')
            self.test_004_tap_make_a_deposit_button()
            self.__class__.min_deposit_error = vec.Quickdeposit.MIN_DEPOSIT_ERROR.replace('5', '50')
            self.test_005_verify_currency_set_within_quick_deposit_section(currency='Kr')
            self.test_006_enter_invalid_amount_into_amount_field_less_than_5_and_tap_deposit_place_bet_button(currency='Kr')
            self.test_007_logout()
