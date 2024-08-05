import pytest
import tests
import datetime
from faker import Faker
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.sanity
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C36621198_Account_Closure_flow(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C36621198
    NAME: Account Closure flow
    DESCRIPTION: This test case verifies Account Closure functionality
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to My Account menu -> select 'Gambling control' item
    PRECONDITIONS: * Select 'Account Closure & Reopening' section and click 'Choose'
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def navigate_to_right_menu_and_click_on_deposit(self):
        self.site.header.right_menu_button.click()
        right_menu = self.site.right_menu
        self.assertTrue(right_menu,
                        msg='Right menu is not opened')
        self.assertTrue(right_menu.has_deposit_button(),
                        msg='Quick Deposit button is not displayed in right menu')
        right_menu.deposit_button.click()

    def test_000_precondition(self):
        """
        PRECONDITIONS: - App is loaded
        PRECONDITIONS: - User is logged in
        PRECONDITIONS: - User opens My Account -> Gambling Controls -> Account Closure
        PRECONDITIONS: - User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option and continues
        PRECONDITIONS: ! BE AWARE - that you'll NOT be able to login after self-exclusion, so use/create disposable test account
        """
        if tests.settings.gvc_wallet_env == 'prod':
            self.__class__.user_name = self.generate_user()
            birth_date = '1-06-1977'
            now = datetime.datetime.now()
            shifted_year = str(now.year + 5)
            card_date = f'{now.month:02d}/{shifted_year[2:]}'
            first_name = Faker().first_name_female()
            self.site.register_new_user(username=self.user_name, birth_date=birth_date, first_name=first_name,
                                        password=tests.settings.default_password)
            self.navigate_to_right_menu_and_click_on_deposit()
            self.assertTrue(self.site.select_deposit_method.deposit_title.is_displayed(),
                            msg='"Deposit page" is not displayed')
            deposit_method = self.site.select_deposit_method
            self.assertTrue(deposit_method.visa_button.is_displayed(), msg='"Visa card" is not available')
            self.assertTrue(deposit_method.master_card_button.is_displayed(), msg='"Master card" is not available')
            self.assertTrue(deposit_method.maestro_button.is_displayed(), msg='"Maestro card" is not available')
            deposit_method.visa_button.click()
            self.assertTrue(self.site.deposit.deposit_title.is_displayed(),
                            msg='Deposit page with visa card payment method is not opened')
            self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.visa_card,
                                                       cvv_2=tests.settings.visa_card_cvv, expiry_date=card_date)
            expected_deposit_message = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
            actual_deposit_message = self.site.deposit_transaction_details.successful_message
            self.assertEqual(expected_deposit_message, actual_deposit_message,
                             msg=f'Actual message "{actual_deposit_message}" is not same as '
                                 f'Expected "{expected_deposit_message}"')

            self.site.deposit_transaction_details.ok_button.click()
            self.site.wait_content_state('Homepage')
            user_balance = self.site.header.user_balance
            self.assertEqual(user_balance, float(self.deposit_amount),
                             msg=f'Actual user balance "{user_balance}" is not equal to '
                                 f'Expected "{float(self.deposit_amount)}"')

        else:
            self.__class__.user_name = self.gvc_wallet_user_client.register_new_user().username
            self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                                                     card_type='mastercard', expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv=tests.settings.master_card_cvv)
            self.site.login(username=self.user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        list_of_right_menu_items = self.site.right_menu.items_names
        self.assertTrue((item in vec.bma.EXPECTED_LIST_OF_RIGHT_MENU for item in list_of_right_menu_items),
                        msg=f'Actual right menu items: "{list_of_right_menu_items}" are not same as Expected right menu items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')

        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_content_state_changed(timeout=20)
        self.assertTrue(wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'), timeout=20),
                        msg='User is not navigated to "Gambling Controls" page')

        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        options = self.site.account_closure.items_names
        self.assertTrue(options, msg=f'Expected options: "{options}" not available')
        self.assertEqual(options[0], vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1,
                         msg=f'Expected option: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1}" is not same as Actual option: "{options[0]}"')
        self.assertEqual(options[1], vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2,
                         msg=f'Expected option: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2}" is not same as Actual option: "{options[1]}"')

    def test_001_select_i_want_to_close_my_account_or_section_of_itclick_continue(self):
        """
        DESCRIPTION: Select 'I want to close my Account or section of it'
        DESCRIPTION: Click 'Continue'
        EXPECTED: ![](index.php?/attachments/get/111269050)
        """
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1)
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(), msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.account_closure.continue_button.click()

    def test_002_click_close_all(self):
        """
        DESCRIPTION: Click 'Close All'
        EXPECTED: * Option is selected and displayed within 'Please select a closure reason below' drop-down
        EXPECTED: * 'CONTINUE' button becomes enabled
        """
        self.site.service_closure.close_all_button.click()
        self.__class__.duration = list(self.site.service_closure.duration_options.items_as_ordered_dict.values())
        self.assertTrue(self.duration, msg='"Duration options" are not available')
        self.__class__.reason = list(self.site.service_closure.reason_options.items_as_ordered_dict.values())
        self.assertTrue(self.duration, msg='"Reason options" are not available')

    def test_003_select_duration_indefinite_closureselect_reasonclick_continue(self):
        """
        DESCRIPTION: Select duration: indefinite closure
        DESCRIPTION: Select reason
        DESCRIPTION: Click 'Continue'
        EXPECTED: confirmation page is opened
        EXPECTED: ![](index.php?/attachments/get/111269051)
        """
        self.duration[0].click()
        self.reason[0].click()
        self.assertTrue(self.site.service_closure.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.service_closure.continue_button.click()

    def test_004_clicktap_close_my_account(self):
        """
        DESCRIPTION: Click/tap 'Close my account'
        EXPECTED: Account is closed
        """
        self.site.service_closure.close_button.click()
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT,
                         msg=f'Actual text: "{actual_info_text}" is not same as '
                             f'Expected text: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT}"')

    def test_005_log_in_with_closed_account_and_try_to_make_deposit_place_a_bet_via_quick_betbetslipjackpot_and_so_on(self):
        """
        DESCRIPTION: Log in with closed account and try to make
        DESCRIPTION: * deposit
        DESCRIPTION: * place a bet (via Quick Bet/Betslip/Jackpot and so on)
        EXPECTED: * User is not able to deposit
        EXPECTED: * User is not able to place any bet
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        self.site.logout()
        self.site.wait_logged_out(10)
        self.site.wait_content_state_changed(timeout=15)
        self.site.login(username=self.user_name)
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        self.site.right_menu.deposit_button.click()
        self.site.wait_content_state_changed()
        select_deposit_method = self.site.select_deposit_method
        available_deposit_options = select_deposit_method.items_as_ordered_dict
        self.assertFalse(available_deposit_options, msg='deposit options are available')
        self.navigate_to_page('Homepage')

        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        outcomes = next(((market['market']['children']) for market in event['event']['children']
                         if market['market'].get('children')), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes
                                     if outcome['outcome'].get('outcomeMeaningMinorCode') and
                                     outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
        if not self.team1:
            raise SiteServeException('No Home team found')
        self._logger.debug(f'*** Found Football event with selection ids "{self.selection_ids}" and team "{self.team1}"')

        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg='Log In & Bet button is not disabled')

        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)
        self.get_betslip_content().bet_now_button.click()
        self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False), msg='Bet Receipt is displayed')
