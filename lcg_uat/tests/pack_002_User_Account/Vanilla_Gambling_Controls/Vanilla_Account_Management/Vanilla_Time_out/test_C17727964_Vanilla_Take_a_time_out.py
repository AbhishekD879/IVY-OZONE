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
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C17727964_Vanilla_Take_a_time_out(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C17727964
    NAME: [Vanilla] Take a time-out
    DESCRIPTION:
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
    """
    keep_browser_open = True
    deposit_amount = 20.00

    def test_000_pre_conditions(self):
        """"
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        if tests.settings.backend_env != 'prod':
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
        self.site.wait_splash_to_hide()
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.assertTrue(self.site.gambling_controls_page.choose_button.is_displayed(),
                        msg=f'"{self.site.gambling_controls.choose_button.name}" button is not displayed')
        self.site.gambling_controls_page.choose_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/accountclosure'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=40)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url,
                         msg=f'"Account Closure" page is not found. Page url is "{page_url}" instead of "{expected_url}"')
        self.site.wait_splash_to_hide(7)
        self.assertFalse(self.site.account_closure.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is not disabled')

    def test_001_select_the_id_like_to_take_an_irreversible_time_out_or_exclude_myself_from_gaming_option(self):
        """
        DESCRIPTION: Select the 'I’d like to take an irreversible time-out or exclude myself from gaming' option
        EXPECTED: The time-out page is displayed with time-out duration options and reasons.
        """
        options = self.site.account_closure.items
        self.assertTrue(options, msg=f'"{options}" are not available')
        options[1].click()
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.account_closure.continue_button.click()

        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg='Take a short time-out page is not found')
        self.assertTrue(self.site.self_exclusion.duration_options, msg='duration option are not displayed')
        self.assertTrue(self.site.self_exclusion.reason_options_list, msg='reason option are not displayed')

    def test_002_select_time_out_duration(self):
        """
        DESCRIPTION: Select time-out duration
        EXPECTED: Duration gets selected.
        """
        self.site.self_exclusion.duration_options[0].click()
        self.assertTrue(self.site.self_exclusion.duration_options_btn[0].is_selected(),
                        msg='Duration check-box is not selected')

    def test_003_select_time_out_reason(self):
        """
        DESCRIPTION: Select time-out reason
        EXPECTED: Reason gets selected.
        """
        self.site.self_exclusion.reason_options_list[0].click()
        self.assertTrue(self.site.self_exclusion.reason_options[0].is_selected(),
                        msg='Reason check-box is not selected')

    def test_004_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: The confirmation screen of time-out is displayed.
        """
        self.site.self_exclusion.continue_button.click()
        self.assertTrue(self.site.self_exclusion.is_displayed(), msg=f'"Confirmation screen is not displayed')

    def test_005_click_the_take_a_short_time_out_button(self):
        """
        DESCRIPTION: Click the **Take a short time-out** button
        EXPECTED: User account is timed-out for the selected duration.
        EXPECTED: A confirmation message is displayed on the time-out page.
        EXPECTED: Under the confirmation, the consequences of a time-out are displayed with a link to customer service.
        EXPECTED: ![](index.php?/attachments/get/36533)
        """
        self.site.self_exclusion.take_short_time_out.click()
        wait_for_result(lambda: self.site.self_exclusion.consequences_info_message is True, timeout=30)

        short_timed_out_info_message = self.site.self_exclusion.consequences_info_message.text
        self.assertEqual(short_timed_out_info_message, vec.account.CONSEQUENCES_INFO_MESSAGE,
                         msg=f'Incorrect consequences info message is displayed, actual message is "{short_timed_out_info_message}" and '
                             f'expected message is "{vec.account.CONSEQUENCES_INFO_MESSAGE}"')

        self.assertTrue(self.site.self_exclusion.customer_service_team_link,
                        msg='link to customer service is missing under the confirmation')
        actual_consequences_description = self.site.self_exclusion.consequences_desription.text.split('\n')
        expected_consequences_description = list(vec.account.CONSEQUENCE_DESCRIPTION)

        if self.brand == 'bma':
            expected_consequences_description = [
                i.replace(expected_consequences_description[0], expected_consequences_description[0].upper()) for i in
                expected_consequences_description]
        self.assertEqual(sorted(list(actual_consequences_description)), sorted(list(expected_consequences_description)),
                         msg=f'CONSEQUENCE DESCRIPTION is incorrect, actual message is "{actual_consequences_description}" expected is "{sorted(list(expected_consequences_description))}"')
