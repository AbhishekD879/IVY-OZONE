import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29031_Unsuccessful_Deposit_Payments_Cancellation(BaseBetSlipTest):
    """
    TR_ID: C29031
    NAME: Unsuccessful Deposit Payments Cancellation
    DESCRIPTION: This test case verifies Unsuccessful Depositing functionality on the Bet Slip page via credit/debit cards and cancellation from payments system.
    PRECONDITIONS: * Load app and log in with a user that has at list one credit card added
    PRECONDITIONS: * Add selection to Betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * Load app and log in with a user that has at list one credit card added
        PRECONDITIONS: * Add selection to Betslip
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next((market['market']['children'] for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = [i['outcome']['id'] for i in outcomes]
        else:
            selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.site.login(username=tests.settings.quick_deposit_user)
        self.open_betslip_with_selections(selection_ids=selection_ids[0])

    def test_001_enter_stake_amount_that_exceeds_the_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount that exceeds the user`s balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        self.__class__.user_balance = self.site.header.user_balance
        if not int(self.user_balance):
            wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                            name='Quick deposit section to be displayed', timeout=10)
            self.device.refresh_page()
            self.site.open_betslip()
        if self.get_betslip_content().has_deposit_form():
            self.site.betslip.quick_deposit.close_button.click()
        place_bet_button = self.site.betslip.bet_now_button.name
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = self.user_balance + 5
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(actual_message_text, expected_message_text,
                         msg=f'Actual deposit message: "{actual_message_text}" is not same as Expected deposit message: "{expected_message_text}"')
        self.__class__.make_deposit_button = self.site.betslip.make_quick_deposit_button.name
        self.assertNotEqual(place_bet_button, self.make_deposit_button,
                            msg=f'Place bet button name: "{place_bet_button}" is not changed to Make deposit button: {self.make_deposit_button}')

    def test_002_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET'
        """
        self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit popup is not displayed')
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        deposit_and_place_bet_button = self.quick_deposit.deposit_and_place_bet_button.name
        self.assertNotEqual(self.make_deposit_button, deposit_and_place_bet_button,
                            msg=f'Make deposit button name: "{self.make_deposit_button}" was not changed to Deposit and place bet : "{deposit_and_place_bet_button}"')

    def test_003_enter__valid_cvv_into_cvv_field__an_amount_that_is_more_than_the_selected_card_limitpayment_method_limit_into_deposit_amount_field(self):
        """
        DESCRIPTION: Enter:
        DESCRIPTION: - valid CVV into 'CVV' field
        DESCRIPTION: - an amount that is more than the Selected Card limit(payment method limit) into 'Deposit Amount' field
        EXPECTED: - No error messages appear
        """
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='123')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = '123'

        self.quick_deposit.amount.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='delete')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='0')
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.amount.input.value = '50'
        self.assertEqual(self.quick_deposit.deposit_amount_error, '', msg=f'Actual Deposit Amount error message: "{self.quick_deposit.deposit_amount_error}" which is expected as Empty')

    def test_004_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: -   User remains on the 'Bet Slip' page
        EXPECTED: -   User Balance is unchanged
        EXPECTED: -   'Deposit Amount' field remains unchanged
        EXPECTED: -  'CVV' field is cleared
        EXPECTED: -  [Coral]/[Ladbrokes] Error message appears within 'Quick Deposit' content area inside the 'i' information message
        EXPECTED: (e.g.
        EXPECTED: "Sorry, the maximum MC deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Sorry, the maximum VISA deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Sorry, the maximum MAESTRO deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Sorry, the maximum ELECTRON deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Canceled by the Payment Method System")
        EXPECTED: also check Error from in WebSockets. The "**message**" part of the error response is shown.  (e.g. "errorMessage":"Canceled by the Payment Method System".)
        EXPECTED: Note: If "message" part is absent, "errorMessage"/"description"/"errorDescription" part is shown (next available value in mentioned order)
        EXPECTED: WS/ Response ID: 33014
        """
        self.quick_deposit.deposit_and_place_bet_button.click()
        result = wait_for_result(lambda: self.quick_deposit.cvv_2.input.value == '', timeout=10, name='page loading to be completed')
        self.assertTrue(self.quick_deposit.cvv_2.is_displayed(), msg='User was not on the betslip page')
        deposit_value = self.quick_deposit.amount.input.value
        self.assertEqual(deposit_value, '5.00', msg=f'Actual Deposit value:"{deposit_value}" is not same as Expected deposit value: "5.00"')
        self.quick_deposit.cvv_2.click()
        self.assertTrue(result, msg=f'Actual CVV value:"{self.quick_deposit.cvv_2.input.value}" is not same as Expected CVV value: ""')
        self.navigate_to_page('/')
        self.verify_user_balance(expected_user_balance=self.user_balance)
