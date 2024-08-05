import datetime
import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17752131_Vanilla_Self_exclude_yourself(BaseBetSlipTest):
    """
    TR_ID: C17752131
    NAME: [Vanilla] Self-exclude yourself
    DESCRIPTION: This test case verifies self-exclusion feature
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
        PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount,
                                                                 card_number=tests.settings.master_card,
                                                                 card_type='mastercard', expiry_month=self.expiry_month,
                                                                 expiry_year=self.expiry_year,
                                                                 cvv=tests.settings.master_card_cvv)
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=20)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        self.site.account_closure.continue_button.click()

    def test_001_navigate_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Navigate to the bottom of the page
        """
        self.site.self_exclusion.self_exclusion_link.scroll_to()
        self.__class__.self_exclusion_link = self.site.self_exclusion.self_exclusion_link
        self.assertTrue(self.self_exclusion_link.is_displayed(), msg=f'"Self Exclusion" link is not displayed')

    def test_002_click_the_self_exclusion_link(self):
        """
        DESCRIPTION: Click the 'Self-exclusion' link
        EXPECTED: User is redirected to Gambling controls page with 'Self Exclusion' option selected by default.
        """
        self.self_exclusion_link.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion/selection'.replace('beta2', 'beta')
        result = wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        self.assertTrue(result, msg=f'User is not redirected to Gambling controls page and Actual URL is '
                                    f'"{self.device.get_current_url()}" & the Expected URL is: "{expected_url}"')
        images = self.site.self_exclusion_selection.image
        self.assertTrue(images[0].is_enabled(), msg='"Self-exclusion" option is not selected by default')

    def test_003_click_the_choose_button(self):
        """
        DESCRIPTION: Click the 'Choose' button
        EXPECTED: User is redirected to 'Self-Exclusion' page with self-exclusion duration and reason selection.
        """
        self.site.self_exclusion_selection.choose_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion/options'.replace('beta2', 'beta')
        result = wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        self.assertTrue(result, msg=f'User is not redirected to Self-Exclusion page and Actual URL is '
                                    f'"{self.device.get_current_url()}" & the Expected URL is: "{expected_url}"')
        self.__class__.self_exclusion_options = self.site.self_exclusion_options
        self.__class__.duration = self.self_exclusion_options.duration_options
        self.assertTrue(self.duration, msg='"Duration options" are not available')
        self.__class__.reason = self.self_exclusion_options.reason_options
        self.assertTrue(self.duration, msg='"Reason options" are not available')

    def test_004_select_self_exclusion_duration(self):
        """
        DESCRIPTION: Select self-exclusion duration
        EXPECTED: Duration successfully selected
        """
        self.duration[0].click()
        click(self.reason[0])
        self.assertTrue(self.self_exclusion_options.continue_button.is_enabled(),
                        msg=f'Continue button:"{vec.account.CONTINUE}" is not enabled')
        self._logger.info('"Duration" and "Reason" options are selected as continue button is enabled')

    def test_005_select_the_reason(self):
        """
        DESCRIPTION: Select the reason
        EXPECTED: Reason successfully selected
        """
        # Covered in the step test_004

    def test_006_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: User is redirected to Self-Exclusion password confirmation page.
        """
        self.self_exclusion_options.continue_button.click()
        self.__class__.self_exclusion_options = self.site.self_exclusion_options
        self.assertTrue(self.self_exclusion_options.password_field.is_displayed(),
                        msg='User is not redirected to Self-Exclusion password confirmation page')

    def test_007_enter_correct_password(self):
        """
        DESCRIPTION: Enter correct password
        EXPECTED: Password is successfully entered
        """
        self.self_exclusion_options.password_input(tests.settings.default_password)
        self.assertTrue(self.self_exclusion_options.self_exclude_button.is_enabled(),
                        msg='Password was not entered as Self exclude button was not enabled')

    def test_008_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Click the 'Self Exclude' button
        EXPECTED: Self-exclusion confirmation page appears.
        """
        self.self_exclusion_options.self_exclude_button.click()
        self.assertTrue(self.site.self_exclusion_options.info_message.is_displayed(),
                        msg='Self-exclusion confirmation page was not appeared')
        actual_text = self.site.self_exclusion_options.info_message.text
        self.assertEqual(actual_text, vec.bma.SELF_EXCLUDED_INFO_MESSAGE,
                         msg=f'Actual self-excluded message: "{actual_text}" is not same as Expected self-excluded message: "{vec.bma.SELF_EXCLUDED_INFO_MESSAGE}"')

    def test_009_tick_both_tickboxes(self):
        """
        DESCRIPTION: Tick both tickboxes
        EXPECTED: Tickboxes successfully ticked
        """
        # step to be removed

    def test_010_click_the_yes_button(self):
        """
        DESCRIPTION: Click the 'YES' button
        EXPECTED: User is self-excluded.
        EXPECTED: Self-exclusion confirmation page appears.
        """
        # step to be removed
