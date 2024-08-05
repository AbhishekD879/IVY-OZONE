import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C9315105_Verify_validation_errors_for_CVV_and_Amount_fields_on_Quick_Deposit_stand_alone(BaseBetSlipTest):
    """
    TR_ID: C9315105
    NAME: Verify validation errors for 'CVV' and 'Amount' fields on 'Quick Deposit' stand alone
    DESCRIPTION: This test case verifies validation errors for 'CVV' and 'Amount' fields
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has credit cards added to his account
    PRECONDITIONS: 3. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is logged in
        PRECONDITIONS: 2. User has credit cards added to his account
        PRECONDITIONS: 3. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
        """
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
        user_balance = self.site.header.user_balance
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = user_balance + 5
        if int(user_balance):
            self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit popup is not displayed')

    def test_001_enter_less_than_3_digits_in_cvv_field(self):
        """
        DESCRIPTION: Enter less than 3 digits in 'CVV' field
        EXPECTED: - 'CVV' field is populated with entered value
        EXPECTED: - 'Deposit' button remains disabled
        """
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            keyboard = self.quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value='1')
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = '1'
        sleep(2)
        actual_entered_value = self.quick_deposit.cvv_2.input.value
        self.assertEqual(actual_entered_value, '1',
                         msg=f'Actual entered value: "{actual_entered_value}" is not same as Expected value: "1"')
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(
            expected_result=False), msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not disabled')

    def test_002_enter_value_less_than_5_into_deposit_account_field(self):
        """
        DESCRIPTION: Enter value less than '5' into 'Deposit Account' field
        EXPECTED: - 'Deposit Account' field is populated with entered value
        EXPECTED: - 'Deposit' button becomes enabled
        """
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            keyboard = self.quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value='delete', delay=1)
            keyboard.enter_amount_using_keyboard(value='0000')
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = '0000'
        sleep(2)
        actual_entered_value = self.quick_deposit.cvv_2.input.value
        self.assertEqual(actual_entered_value, '000',
                         msg=f'Actual entered value: "{actual_entered_value}" is not same as Expected value: "000"')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        # removing one digit from three digits to check the scenario with less than 5 digits as CVV filed accepting only three digits of any combination
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            keyboard = self.quick_deposit.keyboard
            keyboard.enter_amount_using_keyboard(value='delete', delay=0.5)
        else:
            self.quick_deposit.cvv_2.input.value = '00'

    def test_003_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: - 'Your CV2 is incorrect.' validation message is displayed below 'CVV' field
        EXPECTED: - The minimum deposit amount is <currency symbol> '5' validation message is displayed below 'Deposit Amount' field ('50' for currencies other than GBP, USD, EUR)
        EXPECTED: - Deposit is unsuccessful
        EXPECTED: where <currency symbol> - currency that was set during registration
        EXPECTED: ![](index.php?/attachments/get/36335)
        """
        self.quick_deposit.deposit_and_place_bet_button.click()
        self.assertFalse(self.site.is_bet_receipt_displayed(timeout=0),
                         msg='Deposit is successful as no quick deposit pop up present')
        warning_message = self.quick_deposit.warning_panel
        expected_warning_message = vec.gvc.FUNDS_NEEDED_FOR_BET.format(5)
        self.assertEqual(warning_message, expected_warning_message,
                         msg=f'Incorrect warning message. \nActual:\n[{warning_message}]\nExpected:\n[{expected_warning_message}]')
