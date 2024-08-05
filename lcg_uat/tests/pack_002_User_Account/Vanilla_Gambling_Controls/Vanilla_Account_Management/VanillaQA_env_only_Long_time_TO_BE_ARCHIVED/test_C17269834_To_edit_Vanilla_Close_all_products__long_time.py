import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


# @pytest.mark.stg2
# @pytest.mark.tst2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C17269834_To_edit_Vanilla_Close_all_products__long_time(BaseUserAccountTest):
    """
    TR_ID: C17269834
    NAME: {To edit} [Vanilla] Close all products - long time
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in and DON'T have any closed products
        PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
        PRECONDITIONS: User selects 'I'd like to close my account' option and clicks the Continue button
        """
        user_data = self.gvc_wallet_user_client.register_new_user()
        self.username = user_data.username
        self.password = user_data.password
        self.add_card_and_deposit(username=self.username,
                                  card_number='5137651100600001',
                                  amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.username)

        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(timeout=3),
                        msg='User menu is not opened')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.gambling_controls_title)
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=10),
                        msg=f'"Gambling Controls" page is not opened')
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')

        account_closure_data = self.gvc_wallet_user_client.get_account_closure_data(username=self.username,
                                                                                    password=self.password)
        self.account_options = [i['title'] for i in account_closure_data['items']]
        account_closure_options = self.site.account_closure.items_as_ordered_dict
        self.assertTrue(account_closure_options, msg='List of options isn\'t displayed on the page')
        list_products_names = [x for x in list(account_closure_options.keys()) if x]
        self.assertListEqual(self.account_options, list_products_names,
                             msg=f'Account closure options from response: \n"{self.account_options}" are not '
                             f'the same as on UI: \n"{list_products_names}"')

        self.site.account_closure.select_option(option_name=self.account_options[0])

        continue_button = self.site.account_closure.continue_button

        self.assertTrue(continue_button.is_displayed(), msg=f'"Continue" button is not displayed')
        self.assertTrue(continue_button.is_enabled(timeout=5), msg=f'"Continue" button is not enabled')
        continue_button.click()

    def test_001_click_the_close_all_button(self):
        """
        DESCRIPTION: Click the 'Close all' button
        EXPECTED: The confirmation screen of Service closure is displayed with closure duration and reason selections.
        """
        self.site.service_closure.close_all_button.click()

        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')

        self.assertListEqual(self.site.service_closure.reason_options.items_names, list(vec.account.CLOSURE_REASONS),
                             msg=f'Actual reasons "{self.site.service_closure.reason_options.items_names}" is not matching with exepected reasons "{list(vec.account.CLOSURE_REASONS)}"')

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'Continue' button
        EXPECTED: 'Continue' button is disabled
        """
        self.assertFalse(self.site.account_closure.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is enabled')

    def test_003_select_account_closure_duration_time(self):
        """
        DESCRIPTION: Select account closure duration time
        EXPECTED: 'Continue' button is disabled
        """
        duration_options = self.site.service_closure.duration_options.items_as_ordered_dict
        self.assertTrue(duration_options, msg='Duration radio buttons aren\'t displayed')
        duration_name, duration = list(duration_options.items())[0]
        duration.click()
        self.assertFalse(self.site.service_closure.continue_button.is_enabled(),
                         msg=f'"{vec.account.CONTINUE}" button is enabled')
        self.assertTrue(duration.is_checked(), msg=f'Duration "{duration_name}" is not selected')

    def test_004_select_closure_reason(self):
        """
        DESCRIPTION: Select closure reason
        EXPECTED: 'Continue' button is enabled
        """
        reason_options = self.site.service_closure.reason_options.items_as_ordered_dict
        self.assertTrue(reason_options, msg='Reason radio buttons aren\'t displayed')
        reason_name, reason = list(reason_options.items())[0]
        reason.click()
        self.assertTrue(self.site.service_closure.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.assertTrue(reason.is_checked(), msg=f'Reason "{reason_name}" is not selected')

    def test_005_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: Another confirmation screen of Service closure is displayed.
        """
        self.site.service_closure.continue_button.click()
        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')

    def test_006_click_the_close_my_account_button(self):
        """
        DESCRIPTION: Click the 'Close my account' button
        EXPECTED: All products are closed for the selected period of time.
        EXPECTED: A confirmation message:
        EXPECTED: 'Successfully closed: <prod1>, ...,<prodn>'
        EXPECTED: is displayed on the Service Closure page.
        """
        self.site.service_closure.close_button.click()
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT,
                         msg=f'Actual text: "{actual_info_text}" is not same as 'f'Expected text: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT}"')
