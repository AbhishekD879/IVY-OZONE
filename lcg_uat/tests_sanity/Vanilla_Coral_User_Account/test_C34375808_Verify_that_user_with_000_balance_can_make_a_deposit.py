import pytest
import tests
import datetime
from faker import Faker
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.failure_exception import TestFailure


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.critical
@pytest.mark.user_account
@pytest.mark.deposit
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.hotfix
# @pytest.mark.sanity
@vtest
class Test_C34375808_Verify_that_user_with_000_balance_can_make_a_deposit(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C34375808
    NAME: Verify that user with 0.00 balance can make a deposit
    DESCRIPTION: Verify that the user with 0.00 balance can make a deposit
    """
    keep_browser_open = True
    bet_amount = '5'
    deposit_amount = 10
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    vexpiry_month = f'{now.month:02d}'

    def navigate_to_right_menu_and_deposit(self, select_deposit, deposit_amount):
        self.site.header.right_menu_button.click()
        right_menu = self.site.right_menu
        self.assertTrue(right_menu,
                        msg='Right menu is not opened')
        self.assertTrue(right_menu.has_deposit_button(),
                        msg='Quick Deposit button is not displayed in right menu')
        right_menu.deposit_button.click()

        if select_deposit:
            self.assertTrue(self.site.select_deposit_method.deposit_title.is_displayed(),
                            msg='"Deposit page" is not displayed')
            deposit_method = self.site.select_deposit_method
            self.assertTrue(deposit_method.visa_button.is_displayed(), msg='"Visa card" is not available')
            self.assertTrue(deposit_method.master_card_button.is_displayed(), msg='"Master card" is not available')
            self.assertTrue(deposit_method.maestro_button.is_displayed(), msg='"Maestro card" is not available')
            deposit_method.visa_button.click()
            self.assertTrue(self.site.deposit.deposit_title.is_displayed(),
                            msg='Deposit page with visa card payment method is not opened')

            self.site.deposit.add_new_card_and_deposit(amount=deposit_amount, card_number=tests.settings.visa_card,
                                                       cvv_2=tests.settings.visa_card_cvv, expiry_date=self.card_date)
        else:
            self.site.deposit.add_new_card_and_deposit(amount=5, cvv_2=tests.settings.visa_card_cvv)
        expected_deposit_message = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(deposit_amount)
        actual_deposit_message = self.site.deposit_transaction_details.successful_message
        self.assertEqual(expected_deposit_message, actual_deposit_message,
                         msg=f'Actual message "{actual_deposit_message}" is not same as '
                             f'Expected "{expected_deposit_message}"')
        self.site.wait_content_state('Homepage')
        user_balance = self.site.header.user_balance
        self.assertEqual(user_balance, float(self.deposit_amount),
                         msg=f'Actual user balance "{user_balance}" is not equal to '
                             f'Expected "{float(self.deposit_amount)}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        """
        self.__class__.username = self.generate_user()
        self.__class__.birth_date = '1-06-1977'
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'
        self.__class__.first_name = Faker().first_name_female()
        if tests.settings.gvc_wallet_env == 'prod':
            self.site.register_new_user(username=self.username, birth_date=self.birth_date, first_name=self.first_name, password=tests.settings.default_password)
        else:
            self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
            self.site.login(username=self.username, async_close_dialogs=False)

        self.navigate_to_right_menu_and_deposit(select_deposit=True, deposit_amount=self.deposit_amount)

    def test_001_login_to_oxygen_app_with_a_user_that_has_a_credit_card_added_as_payment_method_but_has_no_funds_on_users_account(self):
        """
        DESCRIPTION: Login to Oxygen app with a user that has a credit card added as payment method, but has no funds on user's account
        EXPECTED: 'Low balance' tooltip is displayed within Betslip
        EXPECTED: (Handled on GVC side)
        """
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category()
        else:
            event_params = self.ob_config.add_tennis_event_to_autotest_trophy()
            selection_ids = event_params.selection_ids
        selection_id = list(selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_single_bet(stake_bet_amounts={list(selection_ids.keys())[0]: self.bet_amount})
        try:
            self.assertTrue(self.site.has_low_balance(), msg='Low balance tooltip is not displayed')
        except TestFailure:
            self._logger.info('*** Low balance tooltip probably is not configured on GVC side')
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_002_click_on_deposit_button_from_navigation_bar_for_desktop_or_deposit_button_from_my_account_menu_for_desktopmobiletablet(self):
        """
        DESCRIPTION: Click on 'Deposit' button from Navigation bar (For Desktop) or 'Deposit' button from 'My Account' menu (For Desktop/Mobile/Tablet)
        EXPECTED: 'Deposit' pop-up is displayed
        """
        self.navigate_to_page("Homepage")
        self.navigate_to_right_menu_and_deposit(select_deposit=False, deposit_amount=5)

    def test_003_enter_an_amount_eg_10enter_a_cv2_eg_123click_on_deposit(self):
        """
        DESCRIPTION: Enter an amount (e.g. 10£)
        DESCRIPTION: Enter a CV2 (e.g. 123)
        DESCRIPTION: Click on Deposit
        EXPECTED: "Transaction successful" message is displayed on green background
        """
        # covered in above step

    def test_004_observe_the_balance_of_the_account(self):
        """
        DESCRIPTION: Observe the balance of the account
        EXPECTED: The balance is correctly updated within seconds
        """
        # covered in step 2

    def test_005_click_on_user_menu_logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
