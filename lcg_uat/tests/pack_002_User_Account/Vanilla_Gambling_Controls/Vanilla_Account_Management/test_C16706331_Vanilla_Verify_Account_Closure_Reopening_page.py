import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from datetime import datetime


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16706331_Vanilla_Verify_Account_Closure_Reopening_page(Common):
    """
    TR_ID: C16706331
    NAME: [Vanilla] Verify Account Closure & Reopening page
    DESCRIPTION: This test case verifies Account Closure & Reopening page 1
    PRECONDITIONS: Load app
    PRECONDITIONS: **Prepare users:**
    PRECONDITIONS: (Users should be real-money players - at least one deposit in the past)
    PRECONDITIONS: 1) UK user that don't have any closed products
    PRECONDITIONS: 2) UK user that have some closed products
    PRECONDITIONS: 3) UK user that have all products closed
    PRECONDITIONS: 4) non UK user that don't have any closed products
    PRECONDITIONS: 5) non UK user that have some closed products
    PRECONDITIONS: 6) non UK user that have all products closed
    PRECONDITIONS: Or just simply 2 users - **UK user** and **Non UK user** - check when no product is closed, close one product - check when one product is closed, close all products - check when all products are closed.
    PRECONDITIONS: **For all users:**
    PRECONDITIONS: Navigate to My Account -> Gambling Controls
    PRECONDITIONS: Select 'Account Closure & Reopening' option
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.now()
    shifted_year = str(now.year + 5)
    card_date = f'{now.month:02d}/{shifted_year[-2:]}'

    def product_closing(self, close_all=False):
        self.navigate_to_page(name='en/mobileportal/gamblingcontrols')
        self.site.wait_content_state_changed(timeout=20)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1).click()
        self.site.account_closure.continue_button.click()
        self.site.wait_content_state_changed(timeout=30)
        closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(closure_details, msg="List of products isn't available to the user")

        if close_all:
            product_names = list(closure_details.keys())
            self.assertTrue(product_names, msg='No products displayed')
            expected_info_text = f'Successfully closed: {product_names[0]}, {product_names[1]}, {product_names[2]}'
            self.site.service_closure.close_all_button.click()
            self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')
            self.assertListEqual(self.site.service_closure.reason_options.items_names,
                                 list(vec.account.CLOSURE_REASONS),
                                 msg=f'Actual reasons "{self.site.service_closure.reason_options.items_names}" is not matching with exepected reasons "{list(vec.account.CLOSURE_REASONS)}"')
        else:
            product_name, product = list(closure_details.items())[0]
            self.assertTrue(product.close_button.is_displayed(), msg='"CLOSE button" is not displayed')
            expected_info_text = f'Successfully closed: {product_name}'
            product.close_button.click()

        duration_options = self.site.service_closure.duration_options.items_as_ordered_dict
        self.assertTrue(duration_options, msg='Duration radio buttons aren\'t displayed')
        reason_options = self.site.service_closure.reason_options.items_as_ordered_dict
        self.assertTrue(reason_options, msg='Reason radio buttons aren\'t displayed')
        list(duration_options.values())[0].click()
        list(reason_options.values())[0].click()
        self.site.service_closure.continue_button.click()
        self.site.service_closure.close_button.click()

        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, expected_info_text,
                         msg=f'Actual text: "{actual_info_text}" is not same as Expected text: "{expected_info_text}"')

    def test_000_preconditions(self, uk=True):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
        PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
        """
        if uk:
            user_name = self.gvc_wallet_user_client.register_new_user().username
            self.site.login(username=user_name)
        else:
            self.navigate_to_page(name='home')
            user_name = self.generate_user()
            self.site.register_new_user(birth_date='01-06-1977', country='Ireland', state='County Dublin', post_code='A847545',
                                        username=user_name,
                                        city='Dublin', currency='EUR')
            self.assertTrue(self.site.wait_content_state("Homepage"))
            self.site.header.right_menu_button.click()
            if self.brand == 'bma':
                self.site.right_menu.click_item(item_name='Banking')
            else:
                self.site.right_menu.click_item(item_name='Banking & Balances')
            self.site.right_menu.click_item(item_name='Deposit')
            self.__class__.select_deposit_method = self.site.select_deposit_method
            self.assertTrue(wait_for_result(lambda: self.select_deposit_method.deposit_title.is_displayed(), timeout=5),
                            msg='"Deposit page" is not displayed')
            self.select_deposit_method.master_card_button.click()
            self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                                       cvv_2=tests.settings.master_card_cvv, expiry_date=self.card_date)
            expected_deposit_message = 'Your deposit of 20.00 EUR has been successful'
            actual_deposit_message = self.site.deposit_transaction_details.successful_message
            self.assertEqual(actual_deposit_message, expected_deposit_message,
                             msg=f'Actual message: "{actual_deposit_message}" is not same as Expected: "{expected_deposit_message}"')
            self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name=vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_content_state_changed(timeout=30)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')

    def test_001_log_in_with_user_nr_1_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user nr 1 and go through the path from preconditions
        """
        # Covered in step_000

    def test_002_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        self.assertFalse(self.site.account_closure.continue_button.is_enabled(),
                         msg='"CONTINUE" button is not disabled by default')
        options = self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        options.click()
        self.assertTrue(self.site.account_closure.continue_button.is_displayed(),
                        msg='"CONTINUE" button is not displayed')
        self.assertTrue(self.site.account_closure.cancel_button.is_displayed(),
                        msg='"CANCEL" button is not displayed')

    def test_003_verify__continue__button(self):
        """
        DESCRIPTION: Verify [ Continue ] button
        EXPECTED: [ Continue ] button is disabled by default
        """
        # Covered in step_002

    def test_004_verify__cancel__button(self):
        """
        DESCRIPTION: Verify [ Cancel ] button
        EXPECTED: [ Cancel ] button is enabled by default
        """
        self.assertTrue(self.site.account_closure.cancel_button.is_enabled(),
                        msg='"CANCEL" button is not enabled by default')

    def test_005_clicktap__cancel__button(self):
        """
        DESCRIPTION: Click/Tap [ Cancel ] button
        EXPECTED: User is navigated to 'Gambling Controls' page
        """
        self.site.account_closure.cancel_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=40)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"Gambling Controls" page is not found. Page url is "{page_url}" instead of "{expected_url}"')

    def test_006_log_in_with_user_nr_2_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user nr 2 and go through the path from preconditions
        """
        self.product_closing()

    def test_007_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        self.navigate_to_page(name='en/mobileportal/gamblingcontrols')
        self.site.wait_content_state_changed(timeout=20)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        self.test_002_click_the__choose__button()
        self.test_004_verify__cancel__button()

    def test_008_log_in_with_user_3_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 3 and go through the path from preconditions
        """
        self.product_closing(close_all=True)

    def test_009_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        self.test_007_click_the__choose__button()

    def test_010_log_in_with_user_4_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 4 and go through the path from preconditions
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.site.logout()
        self.test_000_preconditions(uk=False)

    def test_011_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        self.test_002_click_the__choose__button()
        self.test_004_verify__cancel__button()
        self.test_005_clicktap__cancel__button()

    def test_012_log_in_with_user_5_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 5 and go through the path from preconditions
        """
        self.product_closing()

    def test_013_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to close my account or sections of it'
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        self.test_007_click_the__choose__button()

    def test_014_log_in_with_user_6_and_go_through_the_path_from_preconditions(self):
        """
        DESCRIPTION: Log in with user 6 and go through the path from preconditions
        """
        self.product_closing(close_all=True)

    def test_015_click_the__choose__button(self):
        """
        DESCRIPTION: Click the [ Choose ] button
        EXPECTED: Account closure page appears with content:
        EXPECTED: - **Account Closure & Reopening** header
        EXPECTED: - 'Please choose one of the options below.' line with radio button options underneath:
        EXPECTED: -- 'I want to reopen my account or sections of it'
        EXPECTED: -- 'I'd like to take an irreversible time-out or exclude myself from gaming'
        EXPECTED: - [ Continue ] button
        EXPECTED: - [ Cancel ] button
        """
        self.test_007_click_the__choose__button()
