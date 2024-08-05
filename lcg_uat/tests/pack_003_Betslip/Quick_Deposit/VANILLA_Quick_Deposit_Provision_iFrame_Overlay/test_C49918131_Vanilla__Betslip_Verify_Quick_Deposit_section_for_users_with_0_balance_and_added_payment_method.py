import datetime
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import switch_to_main_page
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C49918131_Vanilla__Betslip_Verify_Quick_Deposit_section_for_users_with_0_balance_and_added_payment_method(BaseBetSlipTest):
    """
    TR_ID: C49918131
    NAME: [Vanilla] - [Betslip] Verify Quick Deposit section for users with 0 balance and added payment method
    DESCRIPTION: This test case verifies Quick Deposit section within Betslip for users with 0 balance and added payment method
    """
    keep_browser_open = True
    deposit_amount = 5
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1.  User account with **0 balance and at least one registered Credit Card** (Additional pop-up Quick Deposit)
        PRECONDITIONS: 2.  User account with **positive balance and at least one registered Credit Card**
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next((market['market']['children'] for market in event['event']['children']
                            if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name, self.__class__.selection_id = list(selection_ids.items())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[1]

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_added_payment_method_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and added payment method to his account
        EXPECTED: User is logged in
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username = username,
                                                                 amount = 5,
                                                                 card_number = "5190023456735555",
                                                                 card_type = 'mastercard',
                                                                 expiry_month = self.expiry_month,
                                                                 expiry_year = self.expiry_year, cvv='111')
        self.site.login(username=username)
        user_balance = self.site.header.user_balance
        if user_balance:
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.bet_amount = user_balance
            self.place_single_bet()
            self.navigate_to_page("Homepage")

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.site.wait_content_state_changed(timeout=5)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        self.assertIn(self.selection_name, singles_section.keys(),
                      msg=f'Actual list "{singles_section.items()}" does not contain Added selection "{self.selection_name}"')
        if self.device_type == 'mobile':
            if not self.get_betslip_content().has_deposit_form():
                self.site.close_betslip()
                self.site.wait_content_state_changed(10)
                self.site.open_betslip()
        result = wait_for_result(lambda: self.get_betslip_content().has_deposit_form(),
                                 name='Quick deposit to be displayed', timeout=15)
        self.assertTrue(result, msg='Quick Deposit is not displayed')

    def test_004_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Quick Deposit iFrame is automatically opened in Betslip
        """
        # covered in step test_003

    def test_005_enter_any_value_in_deposit_amount_fieldenter_cvvclicktap_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Enter any value in Deposit amount field
        DESCRIPTION: Enter CVV
        DESCRIPTION: Click/Tap 'Deposit and Place Bet' button
        EXPECTED: For Coral 'Please Enter A Stake For At Least One Bet' message appears above the Total Stake
        EXPECTED: For Ladbrokes 'Please Enter A Stake For At Least One Bet' message appears in the top for few seconds
        EXPECTED: Deposit is successful
        """
        quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        if self.device_type == 'mobile':
            quick_deposit.amount.input.click()
            quick_deposit.keyboard.enter_amount_using_keyboard(value=self.deposit_amount)
            quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
            quick_deposit.cvv_2.click()
            quick_deposit.keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
            quick_deposit.keyboard.enter_amount_using_keyboard(value='enter')
        else:
            quick_deposit.amount.input.value = self.deposit_amount
            quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv
        deposit_button = quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        deposit_button.click()
        self.site.wait_content_state_changed()
        switch_to_main_page()
        user_balance = self.site.header.user_balance
        self.assertEqual(user_balance, self.deposit_amount, msg=f'Actual user balance: "{user_balance}" is not same as '
                                                                f'Expected user balance: "{self.deposit_amount}"')

        # cannot automate for ladbrokes as the message disappears with in seconds.
        if self.brand == 'bma':
            self.site.wait_content_state_changed()
            alert_msg = self.get_betslip_content().suspended_account_warning_message.text
            self.assertEqual(alert_msg, vec.betslip.PLACE_BET_ALERT_MESSAGE,
                             msg=f'Warning "{alert_msg}" is not the same '
                                 f'as expected: "{vec.betslip.PLACE_BET_ALERT_MESSAGE}"')
        section = self.get_betslip_sections().Singles
        self.assertTrue(section, msg='"sections" not displayed')
        _, stake = list(section.items())[0]
        stake.amount_form.input.value = user_balance
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
