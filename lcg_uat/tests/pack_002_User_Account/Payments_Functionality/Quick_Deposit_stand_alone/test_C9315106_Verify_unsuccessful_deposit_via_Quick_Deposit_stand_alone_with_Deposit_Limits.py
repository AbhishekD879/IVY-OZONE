import datetime

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
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.portal_dependant
@vtest
class Test_C9315106_Verify_unsuccessful_deposit_via_Quick_Deposit_stand_alone_with_Deposit_Limits(BaseBetSlipTest):
    """
    TR_ID: C9315106
    NAME: Verify unsuccessful deposit via 'Quick Deposit' stand alone with 'Deposit Limits'
    DESCRIPTION: Verify unsuccessful deposit via 'Quick Deposit' stand alone with set Deposit Limits
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has credit cards added to his account
    PRECONDITIONS: 3. User has set 'Deposit Limits' in 'Account One' portal
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True
    daily_limit = 20
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is logged in
        PRECONDITIONS: 2. User has credit cards added to his account
        PRECONDITIONS: 3. User has set 'Deposit Limits' in 'Account One' portal
        PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
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

        username = self.gvc_wallet_user_client.register_new_user(limit_type='Daily', daily_limit='25').username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=str(20),
                                                                     card_number=tests.settings.quick_deposit_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')

        self.site.login(username=username)
        user_balance = self.site.header.user_balance
        self.open_betslip_with_selections(selection_ids=selection_ids[0], timeout=5)
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = user_balance + 5
        if int(user_balance):
            self.site.betslip.make_quick_deposit_button.click()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit section to be displayed', timeout=10)
        self.assertTrue(result, msg='Quick Deposit popup is not displayed')

    def test_001_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: - 'CVV' field is populated with entered value
        EXPECTED: - 'Deposit' button remains disabled
        """
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.quick_deposit.cvv_2.click()
        if self.device_type == 'mobile':
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
            self.quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv
        actual_entered_value = self.quick_deposit.cvv_2.input.value
        self.assertEqual(actual_entered_value, tests.settings.quick_deposit_card_cvv,
                         msg=f'Actual entered value: "{actual_entered_value}" is not same as Expected value: "{tests.settings.quick_deposit_card_cvv}"')
        self.quick_deposit.minus_button.click()
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False),
                         msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not disabled')

    def test_002_enter_value_in_deposit_amount_field_that_exceeds_set_deposit_limits_dailyweeklymonthly(self):
        """
        DESCRIPTION: Enter value in 'Deposit Amount' field that exceeds set Deposit limits (daily/weekly/monthly)
        EXPECTED: - 'Deposit Amount' field becomes populated with entered value
        EXPECTED: - 'Deposit' button becomes enabled
        """
        for i in range(int(self.daily_limit) // 5 + 1):
            self.quick_deposit.plus_button.click()
        sleep(2)
        actual_deposit_amount = self.quick_deposit.amount.input.value
        self.assertEqual(int(float(actual_deposit_amount)), int(self.daily_limit) + 5,
                         msg=f'Actual entered value: "{actual_deposit_amount}" is not same as Expected value: "{int(self.daily_limit) + 5}"')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')

    def test_003_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: **'This deposit would exceed your self-imposed deposit limit. You can check your current limit *here*'** message and info (i) red icon are shown above the credit card placeholder/dropdown.
        EXPECTED: ![](index.php?/attachments/get/36323)
        EXPECTED: WHERE *here* is a tappable/clickable link-label, that redirects user to Account One - Responsible Gaming section, closing 'Quick Deposit' section once tapped/clicked.
        """
        self.quick_deposit.deposit_and_place_bet_button.click()
        self.assertEqual(self.quick_deposit.deposit_limit_error, vec.gvc.DEPOSIT_DAILY_LIMIT_EXCEEDED,
                         msg=f'Actual "Deposit limit error": "{self.quick_deposit.deposit_limit_error}"'
                             f'is not the same as expected: "{vec.gvc.DEPOSIT_DAILY_LIMIT_EXCEEDED}"')
