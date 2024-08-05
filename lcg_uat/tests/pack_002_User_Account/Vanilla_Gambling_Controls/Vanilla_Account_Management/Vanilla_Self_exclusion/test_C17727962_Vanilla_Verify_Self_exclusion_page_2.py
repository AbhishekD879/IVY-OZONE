import pytest
import tests
from tests.base_test import vtest
from datetime import datetime
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import click


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17727962_Vanilla_Verify_Self_exclusion_page_2(BaseUserAccountTest):
    """
    TR_ID: C17727962
    NAME: [Vanilla] Verify Self-exclusion page 2
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure&Reopening
    PRECONDITIONS: User selects 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
    PRECONDITIONS: User selects the self-exclusion duration and the reason
    """
    keep_browser_open = True
    wrong_password = "Ivy@1234"

    def test_000_preconditions(self):
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_content_state_changed(10)
        self.site.wait_splash_to_hide(10)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        self.site.account_closure.continue_button.click()
        self.site.self_exclusion.self_exclusion_link.scroll_to()
        self.site.self_exclusion.self_exclusion_link.click()
        self.site.wait_splash_to_hide(3)
        images = self.site.self_exclusion_selection.image
        self.assertTrue(images, msg='"Self-exclusion & Gamstop options" are not available')
        images[0].click()
        self.site.self_exclusion_selection.choose_button.click()
        duration = self.site.self_exclusion_options.duration_options
        reason = self.site.self_exclusion_options.reason_options
        self.site.contents.scroll_to_top()
        duration[-1].click()
        click(reason[0])

    def test_001_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: Self-Exclusion page appears:
        EXPECTED: - title is 'Self-Exclusion'
        EXPECTED: - date and time of the end of self-exclusion is provided,
        EXPECTED: - password confirmation field is displayed,
        EXPECTED: - consequences of self-exclusion are provided,
        EXPECTED: - after confirmation info is provided,
        EXPECTED: - 'Self exclude' button is present,
        EXPECTED: - 'Cancel' button is present
        """
        self.site.account_closure.continue_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion/options'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"SELF EXCLUSION" page is not found')
        if self.device_type == 'mobile':
            expected_title = vec.bma.SELF_EXCLUSION_PAGE2_HEADER if self.brand == 'ladbrokes' else vec.bma.SELF_EXCLUSION_PAGE2_HEADER.upper()
            page_title = self.site.self_exclusion_options.header.text
            self.assertEqual(page_title, expected_title,
                             msg=f'Page title "{page_title}" is not same as "{expected_title}"')
        self.assertTrue(self.site.self_exclusion_options.date_time.is_displayed(),
                        msg='Date & time of the self exclusion is not provided')
        self.assertTrue(self.site.self_exclusion_options.password_input_field.is_displayed(),
                        msg='Password confirmation field is not provided')
        consequences = self.site.self_exclusion_options.consequences.text
        expected_consequences = vec.bma.SELF_EXCLUSION_CONSEQUENCES if self.brand == 'ladbrokes' else vec.bma.SELF_EXCLUSION_CONSEQUENCES.upper()
        self.assertEqual(consequences, expected_consequences,
                         msg=f'Consequences "{consequences}" of self-exclusion is not same as "{expected_consequences}"')
        after_confirmation = self.site.self_exclusion_options.after_confirmation.text
        expected_after_confirmation = vec.bma.SELF_EXCLUSION_AFTER_CONFIRMATION if self.brand == 'ladbrokes' else vec.bma.SELF_EXCLUSION_AFTER_CONFIRMATION.upper()
        self.assertEqual(after_confirmation, expected_after_confirmation,
                         msg=f'After Confirmation "{after_confirmation}" of self-exclusion is not same as "{expected_after_confirmation}"')
        self.assertTrue(self.site.self_exclusion_options.self_exclude_button.is_displayed(),
                        msg=f'"SELF EXCLUDE" button is not present')
        self.assertTrue(self.site.self_exclusion_options.cancel_btn.is_displayed(),
                        msg=f'"Cancel" button is not present')

    def test_002_verify_self_exclusion_date(self):
        """
        DESCRIPTION: Verify
        self exclusion date
        EXPECTED: Date is the same as the one selected as duration
        """
        ui_date = self.site.self_exclusion_options.date_time.text
        self.assertTrue(ui_date, msg=f'Date "{ui_date}" is available')
        ui_year = (ui_date.split(',')[0]).split('/')[2]
        now = datetime.now()
        exclude_year = str(now.year + 5)
        self.assertEqual(ui_year, exclude_year, msg=f'"{ui_year}" is not same as selected as duration "{exclude_year}"')

    def test_003_verify_self_exclude_button(self):
        """
        DESCRIPTION: Verify 'Self exclude' button
        EXPECTED: 'Self exclude' button is disabled
        """
        self.assertFalse(self.site.self_exclusion_options.self_exclude_button.is_enabled(expected_result=False),
                         msg='"Self-exclude" button is enabled')

    def test_004_enter_incorrect_password(self):
        """
        DESCRIPTION: Enter incorrect password
        EXPECTED: 'Self exclude' button is enabled
        """
        self.site.self_exclusion_options.password_input(self.wrong_password)

    def test_005_click_the_self_exclude_button(self):
        """
        DESCRIPTION: Click the 'Self exclude' button
        EXPECTED: 'Incorrect password' message appears
        """
        self.site.self_exclusion_options.self_exclude_button.click()
        self.assertTrue(self.site.self_exclusion_options.info_message.is_displayed(),
                        msg='"Incorrect Password" info message is not displayed')

    def test_006_enter_correct_password(self):
        """
        DESCRIPTION: Enter correct password
        EXPECTED: 'Self exclude' button is enabled
        """
        self.site.self_exclusion_options.password_input(tests.settings.default_password)
        self.assertTrue(self.site.self_exclusion_options.self_exclude_button.is_enabled(),
                        msg=f'"SELF EXCLUDE" button is not enabled')
        self.site.account_closure.cancel_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"{vec.bma.GAMBLING_CONTROLS}" page is not found')
