import pytest
import datetime
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.deposit
@pytest.mark.deposit_limits
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.quick_deposit
@pytest.mark.mobile_only
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1769')
@vtest
class Test_C23820437_Vanilla_Verify_unsuccessful_deposit_via_Quick_Deposit_with_Users_Limits(BaseSportTest, BaseUserAccountTest):
    """
    TR_ID: C23820437
    VOL_ID: C48912020
    NAME: [Vanilla] Verify unsuccessful deposit via Quick Deposit with User's Limits
    DESCRIPTION: This test case verifies unsuccessful deposit via Quick Deposit with User's Limits
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user's settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in and has set Deposit Limits
    PRECONDITIONS: 4. Users have Creditcard added to his account
    PRECONDITIONS: 5. App is loaded
    """
    keep_browser_open = True
    big_stake_value = '30.00'
    stake_value = '25.00'
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find/create sport event that will be added to Quick Bet
        DESCRIPTION: Register user with Creditcard and daily limit
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            market_name = next((market['market']['name'] for market in event['event']['children']
                                if market.get('market').get('templateMarketName') == 'Match Betting'), None)
            self._logger.info(f'*** Found football event with event id "{self.eventID}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        username = self.gvc_wallet_user_client.register_new_user(limit_type='Daily', daily_limit='25').username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=str(20),
                                                                     card_number=tests.settings.quick_deposit_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')

        self.site.login(username=username)
        self.__class__.user_balance = float(self.site.header.user_balance)
        self.navigate_to_edp(event_id=self.eventID)

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_002_enter_value_in_stake_field_that_exceeds_users_balance_and_is_greater_than_deposit_limits_daily_weekly_monthly(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance and is greater than Deposit limits (daily/weekly/monthly)
        EXPECTED: 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below 'QUICK BET' header
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.big_stake_value
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(float(self.big_stake_value) - self.user_balance)
        if self.brand == 'ladbrokes':
            info_panel_texts = self.site.quick_bet_panel.deposit_info_message.texts
            result = self.site.quick_bet_panel.wait_for_deposit_message_to_change()
        else:
            info_panel_texts = self.site.quick_bet_panel.info_panels_text
            result = self.site.quick_bet_panel.wait_for_message_to_change()
        self.assertTrue(result, msg='Notification message is not found')
        self.assertTrue(len(info_panel_texts) > 0, msg='Quick Bet deposit notification is not found')
        message = info_panel_texts[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

    def test_003_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: Quick Deposit iFrame is displayed
        EXPECTED: 'MAKE A DEPOSIT' changed to 'DEPOSIT AND PLACE BET' button disabled by default
        """
        self.assertTrue(self.site.quick_bet_panel.has_make_quick_deposit_button(),
                        msg='"Make a deposit" button is not displayed')
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" panel is not displayed')
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_displayed(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not displayed')
        result = wait_for_result(lambda: self.quick_deposit.deposit_and_place_bet_button.name == vec.gvc.DEPOSIT_AND_PLACE_BTN,
                                 name='Deposit & Place Bet button name',
                                 timeout=3)
        self.assertTrue(result, msg=f'Actual button name: "{self.quick_deposit.deposit_and_place_bet_button.name}"'
                                    f'is not the same as expected: "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False),
                         msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not disabled by default')

    def test_004_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: 'Deposit Amount' and 'CVV' fields are populated with values
        EXPECTED: 'DEPOSIT & PLACE BET' button becomes enabled
        """
        self.quick_deposit.cvv_2.click()
        keyboard = self.quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv, delay=0.7)
        keyboard.enter_amount_using_keyboard(value='enter')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')

    def test_005_tap_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT AND PLACE BET' button
        EXPECTED: Warning message that self-set deposit limit exceeded is displayed
        EXPECTED: - Quick Deposit remains opened
        EXPECTED: - User Balance is not changed
        EXPECTED: - Entered amount is not cleared
        EXPECTED: - CVV field is cleared
        """
        self.quick_deposit.deposit_and_place_bet_button.click()
        self.quick_deposit.switch_to_main_page()
        self.assertEqual(self.user_balance, self.site.header.user_balance,
                         msg=f'"User Balance" was changed. Actual: "{self.site.header.user_balance}" is not the '
                             f'same as expected: "{self.user_balance}"')
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" panel does not remain opened')
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.assertEqual(self.quick_deposit.deposit_limit_error, vec.gvc.DEPOSIT_DAILY_LIMIT_EXCEEDED,
                         msg=f'Actual "Deposit limit error": "{self.quick_deposit.deposit_limit_error}"'
                             f'is not the same as expected: "{vec.gvc.DEPOSIT_DAILY_LIMIT_EXCEEDED}"')
        self.assertFalse(self.quick_deposit.cvv_2.input.value,
                         msg=f'"CVV field" is not cleared')
        expected_deposit_amount = float(self.big_stake_value) - self.user_balance
        self.assertEqual(expected_deposit_amount, float(self.quick_deposit.amount.input.value),
                         msg=f'"Deposit amount" field was cleared: "{expected_deposit_amount}"')

    def test_006_place_bet_with_a_stake_value_that_will_force_you_to_deposit_your_daily_limit_sum(self):
        """
        DESCRIPTION: Place Bet with a stake value that will force you to deposit your 'Daily' limit sum
        EXPECTED: Bet is placed successfully
        EXPECTED: Placed bet value is deducted from user's Balance if user's balance was positive
        """
        self.quick_deposit.switch_to_main_page()
        self.site.quick_bet_panel.quick_deposit_panel.close_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.stake_value
        self.site.wait_splash_to_hide(timeout=5)
        self.test_003_tap_make_a_deposit_button()
        self.test_004_enter_valid_cvv_in_cvv_field()
        self.quick_deposit.deposit_and_place_bet_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(),
                        msg='"Bet receipt" is not displayed')
        self.verify_user_balance(expected_user_balance=0)
