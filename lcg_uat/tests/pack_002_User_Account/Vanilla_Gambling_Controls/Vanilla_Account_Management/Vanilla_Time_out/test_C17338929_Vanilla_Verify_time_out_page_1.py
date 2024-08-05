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
class Test_C17338929_Vanilla_Verify_time_out_page_1(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C17338929
    NAME: [Vanilla] Verify time-out page 1
    DESCRIPTION:
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls
    """
    keep_browser_open = True
    deposit_amount = 20.00

    def test_000_pre_conditions(self):
        """"
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls
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

    def test_001_select_account_closure__reopening_option_and_click_the_choose_button(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening' option and click the **CHOOSE** button
        EXPECTED: 'Account Closure & Reopening' page is open
        """
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

    def test_002_select_id_like_to_take_an_irreversible_time_out_or_exclude_myself_from_gaming_option_and_click_continue_button(self):
        """
        DESCRIPTION: Select 'I'd like to take an irreversible time-out or exclude myself from gaming' option and click 'CONTINUE' button
        EXPECTED: **Take a short time-out** page is displayed:
        EXPECTED: - the duration for time-out is displayed with weeks, months & until options, **TO EDIT** No months option is available
        EXPECTED: - the options to select reason are provided,
        EXPECTED: - link to **Self exclusion** is provided at the bottom of the page,
        EXPECTED: - **Continue** button is provided to proceed with Time out,
        EXPECTED: - **Cancel** button is provided which will cancel the action and take the user back to the Gambling controls page with Deposit Limits option highlighted by default
        """
        options = self.site.account_closure.items
        self.assertTrue(options, msg=f'"{options}" are not available')
        options[1].click()
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(), msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.account_closure.continue_button.click()

        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg='"Take a short time-out" page is not found')

        reason_list = []

        for reason in self.site.self_exclusion.reason_options_list:
            reason_list.append(reason.text)

        self.assertListEqual(sorted(reason_list), sorted(list(vec.account.REASON_FOR_TAKING_BREAK)),
                             msg=f'Actual duration list  "{sorted(reason_list)}" is not matching with exepected list "{sorted(list(vec.account.REASON_FOR_TAKING_BREAK))}"')

        duration_options_list = []

        for duration in self.site.self_exclusion.duration_options:
            duration_options_list.append(duration.text)

        self.assertListEqual(sorted(duration_options_list), sorted(list(vec.account.DURATION_TIMEOUT)),
                             msg=f'Actual duration list  "{sorted(duration_options_list)}" is not matching with exepected list "{sorted(list(vec.account.DURATION_TIMEOUT))}"')

        self.assertTrue(self.site.self_exclusion.self_exclusion_link.is_displayed(), msg='Self exclusion link is not present in Take a short time-out page')
        self.assertTrue(self.site.self_exclusion.continue_button.is_displayed(), msg='Continue button is not present in Take a short time-out page')
        self.assertTrue(self.site.self_exclusion.cancel_button.is_displayed(), msg='Cancel button is not present in Take a short time-out page')

    def test_003_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the **CANCEL** button
        EXPECTED: Time-out action is cancelled.
        EXPECTED: The user is redirected back to the **Gambling Controls** page with **Deposit Limits** option highlighted by default.
        """
        self.site.self_exclusion.cancel_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=40)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url,
                         msg=f'"Gambling Controls" page is not found. Page url is "{page_url}" instead of "{expected_url}"')
