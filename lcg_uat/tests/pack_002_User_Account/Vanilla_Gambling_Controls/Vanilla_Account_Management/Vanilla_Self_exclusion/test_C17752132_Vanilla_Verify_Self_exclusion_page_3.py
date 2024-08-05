import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
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
class Test_C17752132_Vanilla_Verify_Self_exclusion_page_3(Common):
    """
    TR_ID: C17752132
    NAME: [Vanilla] Verify Self-exclusion page 3
    DESCRIPTION: this test case verifies the 3rd self-exclusion page (self-exclusion confirmation)
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link (bottom of the page) and proceeds with self exclusion
    PRECONDITIONS: User selects the self-exclusion duration, the reason and proceeds to the next page
    PRECONDITIONS: User enters the correct password and clicks the 'Self Exclude' button
    PRECONDITIONS: User ticks both tickboxes on the self-exclusion confirmation pop-up
    """
    keep_browser_open = True

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

    def test_001_click_the_yes_button(self):
        """
        DESCRIPTION: Click the 'YES' button
        EXPECTED: Self-exclusion confirmation page appears:
        EXPECTED: - confirmation message is displayed,
        EXPECTED: - the consequences of Self-Exclusion are displayed,
        EXPECTED: - the links to help and contact pages are provided
        """
        self.site.account_closure.continue_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion/options'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"SELF EXCLUSION" page is not found')

        consequences = self.site.self_exclusion_options.consequences.text
        expected_consequences = vec.bma.SELF_EXCLUSION_CONSEQUENCES if self.brand == 'ladbrokes' else vec.bma.SELF_EXCLUSION_CONSEQUENCES.upper()
        self.assertEqual(consequences, expected_consequences,
                         msg=f'Consequences "{consequences}" of self-exclusion is not same as "{expected_consequences}"')
        self.site.self_exclusion_options.password_input(tests.settings.default_password)
        self.assertTrue(self.site.self_exclusion_options.self_exclude_button.is_enabled(),
                        msg=f'"SELF EXCLUDE" button is not enabled')
        self.site.self_exclusion_options.self_exclude_button.click()
        consequences = self.site.self_exclusion_options.consequences.text
        expected_consequences = vec.bma.SELF_EXCLUSION_CONSEQUENCES if self.brand == 'ladbrokes' else vec.bma.SELF_EXCLUSION_CONSEQUENCES.upper()
        self.assertEqual(consequences, expected_consequences,
                         msg=f'Consequences "{consequences}" of self-exclusion is not same as "{expected_consequences}"')
        self.assertTrue(self.site.self_exclusion.customer_service_team_link,
                        msg='link to customer service team is missing')
