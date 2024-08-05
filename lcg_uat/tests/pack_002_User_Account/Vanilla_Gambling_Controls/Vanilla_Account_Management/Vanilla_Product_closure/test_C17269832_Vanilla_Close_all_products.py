import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17269832_Vanilla_Close_all_products(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C17269832
    NAME: [Vanilla] Close all products
    DESCRIPTION:
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and **DON'T** have any closed products
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I want to close my account or sections of it' option and clicks the Continue button
    """
    keep_browser_open = True
    deposit_amount = 20.00

    def test_000_pre_conditions(self):
        """"
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in and **DON'T** have any closed products
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure & Reopening
        PRECONDITIONS: User selects 'I want to close my account or sections of it' option and clicks the Continue button
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=user_name, amount=self.deposit_amount,
                                  card_number=tests.settings.quick_deposit_card)
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=40)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url,
                         msg=f'"Gambling Controls" page is not found. Page url is "{page_url}" instead of "{expected_url}"')
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.assertTrue(self.site.gambling_controls_page.choose_button.is_displayed(),
                        msg=f'"{self.site.gambling_controls.choose_button.name}" button is not displayed')
        self.site.gambling_controls_page.choose_button.click()
        self.assertEqual(self.device.active_tab_title(), vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE,
                         msg=f'"{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION}" page title is incorrect. Page title is "{self.device.active_tab_title()}" instead of "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE}"')
        self.site.wait_splash_to_hide(7)
        self.assertFalse(self.site.account_closure.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is not disabled')
        options = self.site.account_closure.items
        self.assertTrue(options, msg=f'"{options}" are not available')
        options[0].click()
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.account_closure.continue_button.click()
        self.assertEqual(self.device.active_tab_title(), vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE,
                         msg=f'"{vec.account.ACCOUNT_CLOSURE}" page title is incorrect. Page title is "{self.device.active_tab_title()}" instead of "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE}"')

    def test_001_click_the_close_all_button(self):
        """
        DESCRIPTION: Click the **Close all** button
        EXPECTED: The confirmation screen of product closure is displayed with closure duration and reason selections.
        """
        self.site.service_closure.close_all_button.click()

        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')

        self.assertListEqual(self.site.service_closure.reason_options.items_names, list(vec.account.CLOSURE_REASONS),
                             msg=f'Actual reasons "{self.site.service_closure.reason_options.items_names}" is not matching with exepected reasons "{list(vec.account.CLOSURE_REASONS)}"')

        duration_list = self.site.service_closure.duration_options.items_names
        final_duration_list = []
        for duration in duration_list:
            if vec.account.DURATION[4] in duration:
                final_duration_list.append(vec.account.DURATION[4])
            else:
                final_duration_list.append(duration)

        self.assertListEqual(sorted(final_duration_list), sorted(list(vec.account.DURATION)),
                             msg=f'Actual reasons "{final_duration_list}" is not matching with exepected reasons "{list(vec.account.DURATION)}"')

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify **Continue** button
        EXPECTED: **Continue** button is disabled
        """
        continue_btn_disabled = self.site.service_closure.continue_button.is_enabled()
        self.assertFalse(continue_btn_disabled, msg='Continue button is enabled, which it should be disabled')

    def test_003_select_account_closure_duration_time(self):
        """
        DESCRIPTION: Select account closure duration time
        EXPECTED: **Continue** button is disabled
        """
        self.site.service_closure.duration_options.items[0].click()
        continue_btn_disabled = self.site.service_closure.continue_button.is_enabled()
        self.assertFalse(continue_btn_disabled, msg='Continue button is enabled, which it should be disabled')

    def test_004_select_closure_reason(self):
        """
        DESCRIPTION: Select closure reason
        EXPECTED: **Continue** button becomes enabled
        """
        self.site.service_closure.reason_options.items[0].click()
        continue_btn_enabled = self.site.service_closure.continue_button.is_enabled()
        self.assertTrue(continue_btn_enabled, msg='Continue button is disabled, which it should be enabled')

    def test_005_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: Another confirmation screen of product closure is displayed.
        """
        self.site.service_closure.continue_button.perform_click()
        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')

    def test_006_click_the_close_my_account_button(self):
        """
        DESCRIPTION: Click the **Close my account** button
        EXPECTED: All products are closed for the selected period of time.
        EXPECTED: The confirmation message:
        EXPECTED: **Successfully closed: <prod1>, ..., <prodn>'**
        EXPECTED: is displayed on the ** Account Closure** confirmation page.
        EXPECTED: There shouldn't be any other text information under the confirmation message.
        """
        self.site.service_closure.close_button.click()
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT,
                         msg=f'Actual text: "{actual_info_text}" is not same as 'f'Expected text: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT}"')
