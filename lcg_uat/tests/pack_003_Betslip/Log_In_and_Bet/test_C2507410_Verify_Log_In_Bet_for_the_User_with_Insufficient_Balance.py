import pytest
import datetime
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.quick_deposit
@pytest.mark.login
@vtest
class Test_C2507410_Verify_Log_In_Bet_for_the_User_with_Insufficient_Balance(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C2507410
    NAME: Verify Log In Bet for the User with Insufficient Balance
    PRECONDITIONS: Make sure you have user account with:
    PRECONDITIONS: Added credit cards with 0/or insufficient balance
    """
    keep_browser_open = True
    bet_increase_amount = 0.1
    deposit_value = 5
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get user balance which can be used further in test steps
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             'Match Betting' in market['market']['templateMarketName'] and market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection = next((outcome['outcome']['name'] for outcome in outcomes if
                                             outcome['outcome'].get('outcomeMeaningMinorCode') and
                                             outcome['outcome'].get('outcomeMeaningMinorCode', '') == 'H'), None)
            if not self.selection:
                raise SiteServeException('No Home team found')
            self._logger.info(f'*** Found Football event with selection ids "{self.selection_ids}" and team "{self.selection}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection, self.__class__.selection_ids = event.team1, event.selection_ids

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=self.username, amount=str(self.deposit_value),
                                                                     card_number=tests.settings.quick_deposit_card,
                                                                     card_type='mastercard', expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')

        self.__class__.user_balance = self.deposit_value
        self.__class__.bet_amount = self.user_balance + self.bet_increase_amount

    def test_001_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.selection]))

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1. Betslip is opened
        EXPECTED: 2. Added single selection(s) present
        EXPECTED: 3. Coral: 'Login & Place Bet' button is disabled
        EXPECTED: 4. Ladbrokes: 'Login and Place bet
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertEqual(self.stake_name, self.selection,
                         msg=f'Selection "{self.selection}" should be present in betslip, got "{self.stake_name}"')
        betslip = self.get_betslip_content()
        self.assertEqual(betslip.bet_now_button.name,
                         vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Bet button caption should be "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        self.assertFalse(betslip.bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not enabled')

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 'Log in & Bet' button becomes enabled
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(timeout=5), msg='Bet now button is not enabled')

    def test_004_tap_on_log_in_bet_button(self):
        """
        DESCRIPTION: Tap on 'Log in & Bet' button
        EXPECTED: 'Log In' pop-up is opened
        """
        self.get_betslip_content().bet_now_button.click()
        self.__class__.login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.login_dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not shown')

    def test_005_log_in_with_user_that_has_added_credit_cards_and_0or_insufficient_balance_to_cover_the_stake(self):
        """
        DESCRIPTION: Log in with user that has **added credit cards and 0/or insufficient balance to cover the stake**
        EXPECTED: 1. Betslip is NOT refreshed
        EXPECTED: 2. Bet is NOT placed automatically
        EXPECTED: 3. Funds value = Stake - Balance
        EXPECTED: 4. 'Login & Bet' button label is changed to 'Make a Quick Deposit'
        EXPECTED: 5. 'Make a Quick Deposit' button is enabled
        """
        self.login_dialog.username = self.username
        self.login_dialog.password = tests.settings.default_password
        self.login_dialog.click_login()
        login_dialog_closed = self.login_dialog.wait_dialog_closed()
        self.assertTrue(login_dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')
        self.site.close_all_dialogs(async_close=False)

        if not self.site.has_betslip_opened():
            self.site.header.bet_slip_counter.click()

        betslip_content = self.get_betslip_content()
        self.assertTrue(betslip_content.has_make_quick_deposit_button(timeout=20),
                        msg='"Make a Quick Deposit" button is not displayed')
        make_quick_deposit_button_name = self.get_betslip_content().make_quick_deposit_button.name
        self.assertEqual(make_quick_deposit_button_name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual message "{make_quick_deposit_button_name}" != '
                         f'Expected "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.assertTrue(self.get_betslip_content().make_quick_deposit_button.is_enabled(),
                        msg=f'"{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}" button is disabled')

    def test_006_tap_on_make_a_quick_deposit_button_or_on_funds_needed_for_bet_message(self):
        """
        DESCRIPTION: Tap on 'Make a Quick Deposit' button or on 'Funds needed for bet' message
        EXPECTED: 1. 'Quick Deposit' section is expanded
        EXPECTED: 2. 'Make a Quick Deposit' button label is changed 'Deposit & Bet'
        EXPECTED: 3. 'Deposit & Bet' button is disabled
        EXPECTED: 4. Funds needed for bet: <currency symbol>XX.XX** message is displayed on the red background, it is anchored to the footer of the Betslip
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(),
                        msg='"Quick Deposit" section is not displayed')

        quick_deposit = self.site.betslip.quick_deposit.stick_to_iframe()
        actual_name = quick_deposit.deposit_and_place_bet_button.name
        self.assertEqual(actual_name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name "{actual_name}" != Expected "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')

        warning_message = quick_deposit.warning_panel
        expected_warning_message = \
            vec.gvc.FUNDS_NEEDED_FOR_BET.format(self.bet_increase_amount)
        self.assertEqual(warning_message, expected_warning_message,
                         msg=f'Incorrect warning message. \nActual:\n[{warning_message}]\nExpected:\n[{expected_warning_message}]')

        button_status = quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False)
        self.assertFalse(button_status, msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not disabled')
        switch_to_main_page()

    def test_007_clear_stake_field(self):
        """
        DESCRIPTION: Clear 'Stake' field
        EXPECTED: 1. 'Quick Deposit' section disappears
        EXPECTED: 2. Button states 'Bet Now'
        EXPECTED: 3. 'Bet Now' button is disabled
        """
        stake_name, stake = list(self.get_betslip_sections().Singles.items())[0]
        stake.amount_form.enter_amount()
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened, but was expected to be opened')
        betslip = self.get_betslip_content()
        self.assertFalse(betslip.has_deposit_form(expected_result=False),
                         msg='"Quick Deposit" section is still displayed')
        self.assertEqual(betslip.bet_now_button.name, vec.betslip.BET_NOW,
                         msg=f'Button name "{betslip.bet_now_button.name}" '
                             f'is not the same as expected "{vec.betslip.BET_NOW}"')
        self.assertFalse(betslip.bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.BET_NOW}" '
                         f'button is disabled though it is expected to be enabled')

    def test_008_place_bet_that_will_make_your_balance_0(self):
        """
        DESCRIPTION: Place a bet that will make your user's balance '0.00'
        EXPECTED: 1. Bet is successfully placed
        EXPECTED: 2. Bet receipt is shown
        """
        self.__class__.bet_amount = self.user_balance
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_009_tap_reuse_button_in_betslip(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTIONS' button shown in Betslip
        EXPECTED: 1. Betslip is reopened
        EXPECTED: 2. 'Quick Deposit' section is expanded
        EXPECTED: 3. 'DEPOSIT' button is disabled
        EXPECTED: https://jira.egalacoral.com/browse/BMA-50509 closed by business
        """
        # commented due to BMA-50509
        # self.site.bet_receipt.footer.reuse_selection_button.click()

        # singles_section = self.get_betslip_sections().Singles
        # stake = list(singles_section.items())[0]
        # self.enter_stake_amount(stake=stake)
        #
        # self.assertEqual(self.get_betslip_content().make_quick_deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
        #                  msg=f'"Make a Deposit" button name {self.get_betslip_content().make_quick_deposit_button.name}'
        #                      f' is not the same as expected {vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}')
        #
        # self.get_betslip_content().make_quick_deposit_button.click()
        #
        # self.assertTrue(self.get_betslip_content().has_deposit_form(timeout=3),
        #                 msg='"Quick Deposit" section is not displayed')

    def test_010_log_out_and_repeat_steps_1_5_with_the_same_user(self):
        """
        DESCRIPTION: Clear Betslip, Log Out and repeat steps 1-5 with the same user(that now has '0.00' Balance)
        EXPECTED: 1. Expected Results for steps 1-4 should match
        EXPECTED: 2. Expected Result for the repeated Step 5 executions is:
        EXPECTED: 3. Betslip is reopened
        EXPECTED: 4. 'Quick Deposit' section is expanded
        EXPECTED: 5. 'DEPOSIT & PLACE BET' button is disabled
        """
        # commented clear_betslip due to BMA-50509. closing betreceipt instead
        # self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0
        self.site.bet_receipt.footer.click_done()
        if self.device_type == "mobile":
            try:
                self.site.timeline.timeline_splash_page.close_button.click()
            except VoltronException:
                pass
        self.site.logout()
        self.test_001_add_selections_to_the_betslip()
        self.test_002_open_betslip()
        self.test_003_enter_at_least_one_stake_for_any_selection()
        self.test_004_tap_on_log_in_bet_button()
        self.login_dialog.username = self.username
        self.login_dialog.password = tests.settings.default_password
        self.login_dialog.click_login()
        login_dialog_closed = self.login_dialog.wait_dialog_closed()
        self.assertTrue(login_dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')
        self.site.close_all_dialogs(async_close=False)
        login_dialog_closed = self.login_dialog.wait_dialog_closed()
        self.assertTrue(login_dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')

        if not self.get_betslip_content().has_deposit_form():
            #  BMA-50509 handling
            self.get_betslip_content().make_quick_deposit_button.click()

        self.assertTrue(self.get_betslip_content().has_deposit_form(),
                        msg='"Quick Deposit" section is not displayed')

        quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        actual_name = quick_deposit.deposit_and_place_bet_button.name
        self.assertEqual(actual_name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name "{actual_name}" != Expected "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')

        button_status = quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False)
        self.assertFalse(button_status, msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not disabled')
