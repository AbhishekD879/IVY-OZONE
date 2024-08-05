import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from selenium.webdriver.support.select import Select
from voltron.environments import constants as vec
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C17727961_Vanilla_Verify_Self_exclusion_page_1(Common):
    """
     TR_ID: C17727961
     NAME: [Vanilla] Verify Self-exclusion page 1
     PRECONDITIONS: App is loaded
     PRECONDITIONS: User is logged in
     PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
     PRECONDITIONS: User selects the 'I'd like to take an irreversible time-out or exclude myself from gaming' option
     """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
         PRECONDITIONS: App is loaded
         PRECONDITIONS: User is logged in
         PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
         PRECONDITIONS: User selects the 'I'd like to take an irreversible time-out or exclude myself from gaming' option
         """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_splash_to_hide(10)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        self.site.account_closure.continue_button.click()

    def test_001_click_the_self_exclusion_link_bottom_of_the_page(self):
        """
         DESCRIPTION: Click the 'Self-exclusion' link (bottom of the page)
         EXPECTED: Gambling Controls page opens.
         EXPECTED: (Self exclusion option selected by default)
         """
        self.site.self_exclusion.self_exclusion_link.scroll_to()
        self.site.self_exclusion.self_exclusion_link.click()
        self.site.wait_splash_to_hide(3)
        self.__class__.images = self.site.self_exclusion_selection.image
        self.assertTrue(self.images, msg='"Self-exclusion & Gamstop options" are not available')

    def test_002_click_the_choose_button(self):
        """
         DESCRIPTION: Click the 'Choose' button
         EXPECTED: User is redirected to the Self-Exclusion page:
         EXPECTED: - title is Self Exclusion,
         EXPECTED: - different self-exclusion periods are provided,
         EXPECTED: - brand selection is provided,
         EXPECTED: - reasons of self exclusion are provided
         EXPECTED: - 'Continue' button is available,
         EXPECTED: - 'Cancel' button is available
         """
        self.images[0].click()
        self.site.self_exclusion_selection.choose_button.click()
        self.__class__.duration = self.site.self_exclusion_options.duration_options
        self.assertTrue(self.duration, msg='"Duration options" are not available')
        self.__class__.reason = self.site.self_exclusion_options.reason_options
        self.assertTrue(self.duration, msg='"Reason options" are not available')
        self.__class__.brands = Select(self.site.self_exclusion_options.brand)
        self.assertTrue(self.brands, msg='"Brand" is not available')

    def test_003_verify_continue_button(self):
        """
         DESCRIPTION: Verify 'Continue' button
         EXPECTED: 'Continue' button is disabled
         """
        self.assertFalse(self.site.self_exclusion_options.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is enabled')

    def test_004_select_the_self_exclusion_duration(self):
        """
         DESCRIPTION: Select the self-exclusion duration
         EXPECTED: Duration gets selected.
         EXPECTED: 'Continue' button is disabled.
         """
        self.site.contents.scroll_to_top()
        self.duration[-1].click()
        self.assertFalse(self.site.self_exclusion_options.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is not enabled')

    def test_005_select_the_reason(self):
        """
         DESCRIPTION: Select the reason
         EXPECTED: 'Continue' button is enabled.
         """
        click(self.reason[0])
        self.assertTrue(self.site.self_exclusion_options.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')

    def test_006_click_the_cancel_button(self):
        """
         DESCRIPTION: Click the 'Cancel' button
         EXPECTED: User is redirected to Gambling Controls main page with Deposit Limits option selected by default.
         """
        self.assertTrue(self.site.account_closure.cancel_button.is_enabled(),
                        msg=f'"{vec.account.CANCEL}" button is not active')
        self.site.account_closure.cancel_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"{vec.bma.GAMBLING_CONTROLS}" page is not found')
