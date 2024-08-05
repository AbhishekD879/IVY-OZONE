import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29029_Quick_Deposit_Fields_Validation(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29029
    NAME: Quick Deposit Fields Validation
    DESCRIPTION: This test case verifies all elements are present within Quick Deposit section and Fields Validation
    DESCRIPTION: AUTOTEST: [C2352380]
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load app and log in with a user that has at list one credit card added
        PRECONDITIONS: 2. Add selection to Betslip
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next((market['market']['children'] for market in event['event']['children']
                            if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(self.selection_ids.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = list(event.selection_ids.values())[0]
        self.site.login(username=tests.settings.quick_deposit_user)
        self.site.wait_content_state('Homepage')
        user_balance = self.site.header.user_balance
        if user_balance == 0:
            self.open_betslip_with_selections(selection_ids=self.selection_id)

            result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                     name='Quick deposit section to be displayed', timeout=10)
            self.assertTrue(result, msg='Quick Deposit is not displayed')

            quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()

            quick_deposit.amount.input.click()
            if self.device_type == 'mobile':
                quick_deposit.keyboard.enter_amount_using_keyboard(value='5')
                quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
            else:
                quick_deposit.amount.input.value = '5'

            quick_deposit.cvv_2.click()
            if self.device_type == 'mobile':
                quick_deposit.keyboard.enter_amount_using_keyboard(value='123')
                quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
            else:
                quick_deposit.cvv_2.input.value = '123'
            actual_entered_value = quick_deposit.cvv_2.input.value
            self.assertEqual(len(actual_entered_value), 3, msg='CVV filed allowed user to enter more than 3 digits')

            self.assertTrue(quick_deposit.deposit_and_place_bet_button.is_enabled(),
                            msg="deposit and place bet button is disabled")
            quick_deposit.deposit_and_place_bet_button.click()
            result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(expected_result=False),
                                     name='Quick deposit section to disappear', timeout=10)
            self.assertFalse(result, msg='Quick Deposit is still displaying')
        else:
            self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        additional_amount = 5   # this is the minimum amount that we can deposit in Deposit section
        self.__class__.user_balance = self.site.header.user_balance
        place_bet_button = wait_for_result(lambda: self.site.betslip.bet_now_button.name.strip(), name='place_bet_button not available', timeout=10)
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = self.user_balance + additional_amount
        entered_stake_value = stake.amount_form.input.value
        self.assertEqual(float(entered_stake_value), float(self.user_balance + additional_amount),
                         msg=f'Actual entered stake: "{entered_stake_value}" is not same as Expected stake: "{self.user_balance + additional_amount}"')
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(additional_amount)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        self.__class__.make_deposit_button = wait_for_result(lambda: self.site.betslip.make_quick_deposit_button.name.strip(),
                                                             name='make_quick_deposit_button not available',
                                                             timeout=10)
        self.assertNotEqual(place_bet_button, self.make_deposit_button,
                            msg=f'Place bet button name: "{place_bet_button}" is not changed to Make deposit button: {self.make_deposit_button}')

    def test_002_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: *  'Quick Deposit' section is expanded and displayed at the bottom of the Betslip
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button and is disabled by default
        """
        self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit is not displayed')
        quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        deposit_and_place_bet_button = wait_for_result(lambda: quick_deposit.deposit_and_place_bet_button.name.strip(),
                                                       name='place_bet_button not available',
                                                       timeout=10)
        self.assertNotEqual(self.make_deposit_button, deposit_and_place_bet_button, msg=f'Make deposit button name: "{self.make_deposit_button}" was not changed to Deposit and place bet : "{deposit_and_place_bet_button}"')

    def test_003_edit_stakeless_than_min_amount_5_gbp_eur_usd_or_50_sek(self):
        """
        DESCRIPTION: Edit 'Stake' (less than min amount: 5 GBP, EUR, USD or 50 SEK)
        EXPECTED: - 'Please deposit a min...' message is updated
        EXPECTED: - Quick Deposit Section remains expanded
        EXPECTED: - 'Deposit Amount' field contains a '<currency symbol> 5/50 Min' greyed out placeholder
        """
        switch_to_main_page()
        self.get_betslip_content().quick_deposit.close_button.click()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = self.user_balance + 4
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit is not displayed')

    def test_004_edit_deposit_amount_field_in_quick_deposit_section_type_more_than_7_digits_and_2_decimals_000_001_499__1__49__50a_z_a_z___plus_space(self):
        """
        DESCRIPTION: Edit 'Deposit Amount' Field in Quick Deposit section
        DESCRIPTION: * type <more than 7 digits and 2 decimals>
        DESCRIPTION: * 0.00, 0.01, 4.99, -1 / 49, -50
        DESCRIPTION: *<a-z, A-Z, ~!@#$%^&*()`__+={}|[]\:";'<>, <space>>"
        EXPECTED: -   Max number of digits is 7 and 2 decimal (e.g. "XXXXXXX.XX")
        EXPECTED: -   It is not allowed to enter letters or symbols
        """
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.quick_deposit.amount.input.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='123456.11')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.amount.input.value = '123456.11'
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(), msg="As deposit and place bet button is enableDeposit Amount filed was allowed 7 digits and 2 decimals")

    def test_005_select_card_by_using_the_card_dropdown(self):
        """
        DESCRIPTION: Select card by using the card dropdown
        EXPECTED: -  Card is chosen
        EXPECTED: -  It is possible to choose any other registered card to deposit from
        """
        self.quick_deposit.accounts.select_button.click()
        payment_methods = self.quick_deposit.accounts.select_menu.items_as_ordered_dict
        if len(payment_methods) > 2:
            list(self.quick_deposit.accounts.select_menu.items_as_ordered_dict.values())[1].click()
        else:
            self._logger.info('No other Registered card was not available to choose')
            list(self.quick_deposit.accounts.select_menu.items_as_ordered_dict.values())[0].click()

    def test_006_edit_cvv_field_type_more_than_3_digitsa_z_a_z___plus_space_12_00_9_0_9(self):
        """
        DESCRIPTION: Edit 'CVV' field
        DESCRIPTION: * type <more than 3 digits>
        DESCRIPTION: *<a-z, A-Z, ~!@#$%^&*()`__+={}|[]\:";'<>, <space>>"
        DESCRIPTION: * 12, 00, 9, 0, 9
        EXPECTED: -   It is not allowed to enter more than 3 digits on iOS
        EXPECTED: -   It is allowed to enter more than 3 digits on Android
        EXPECTED: (123.0, 9999, 0.0.0.0.0)
        EXPECTED: -   It is not allowed to enter symbols or letters
        """
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='1234')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = '1234'
        actual_entered_value = self.quick_deposit.cvv_2.input.value
        self.assertEqual(len(actual_entered_value), 3, msg='CVV filed allowed user to enter more than 3 digits')

    def test_007_enter_at_least_1_symbol_in_cvv_and_deposit_amount_fieldsand_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter at least 1 symbol in 'CVV*' and 'Deposit Amount' fields
        DESCRIPTION: and tap 'DEPOSIT & PLACE BET' button
        EXPECTED: - 'DEPOSIT & PLACE BET' button becomes enabled when at least 1 symbol is entered into 'CVV' and 'Deposit Amount' fields
        EXPECTED: - As value in 'Deposit Amount' field is less than 5/50 an error message appears below 'Deposit Amount' field: "The minimum deposit amount is <currency symbol>5"
        EXPECTED: - As value in 'CVV' is incorrect an error appears below 'CVV' field: "Your CV2 is incorrect."
        """
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='1')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = '1'
        cvv_error_message = self.quick_deposit.cvv_error
        self.assertNotEqual(cvv_error_message, ' ', msg=f'CVV error message: "{cvv_error_message}" is not displayed')
        self.quick_deposit.amount.input.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='1')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.amount.input.value = '1'
        deposit_amount_error_message = self.quick_deposit.deposit_amount_error
        self.assertTrue(deposit_amount_error_message, msg=f'Deposit amount error message: "{deposit_amount_error_message}" is not displayed')
