import datetime
import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.uat
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.p2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870143_Verify_account_closure_Verify_user_can_navigate_to_Responsible_Gambling_https_responsiblegamblingcoralcouk_Verify_details_for_Account_Closure_and_close_the_account_Verify_user_cant_login_to_sports_site_after_account_closure(BaseBetSlipTest):
    """
    TR_ID: C44870143
    NAME: "Verify account closure, Verify user can navigate to 'Responsible Gambling' https://responsiblegambling.coral.co.uk/ Verify details for 'Account Closure' and close the account. Verify user can't login to sports site after account closure."
    DESCRIPTION: "Verify account closure,
    DESCRIPTION: Verify user can navigate to 'Responsible Gambling' https://responsiblegambling.coral.co.uk/
    DESCRIPTION: Verify details for 'Account Closure' and close the account.
    DESCRIPTION: Verify user can't login to sports site after account closure."
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load app and log in
        PRECONDITIONS: Navigate to Right Menu -> select Gambling Controls
        PRECONDITIONS: Tap/click 'Account Closure & Reopening' twistee
        PRECONDITIONS: Tap on Choose
        PRECONDITIONS: User is taken to Account Closure & Reopening page
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
        sleep(10)
        page_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        self.assertEqual(page_url, expected_url,
                         msg=f'"Gambling Controls" page is not found. Page url is "{page_url}" instead of "{expected_url}"')
        images = self.site.gambling_controls_page.image
        self.assertTrue(images[2].is_displayed(),
                        msg=f'"{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION}" image is not diplayed')
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.assertTrue(self.site.gambling_controls_page.choose_button.is_displayed(),
                        msg=f'"{self.site.gambling_controls.choose_button.name}" button is not displayed')
        self.site.gambling_controls_page.choose_button.click()
        self.assertEqual(self.device.active_tab_title(), vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE,
                         msg=f'"{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION}" page title is incorrect. Page title is "{self.device.active_tab_title()}" instead of "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE}"')

    def test_001_on_account_closure__reopeningstep_1_page_is_opened_with_options_to_choose_and_continue_button_is_disabled(self):
        """
        DESCRIPTION: On 'Account Closure & Reopening'
        DESCRIPTION: Step 1 page is opened with options to choose and CONTINUE button is disabled
        EXPECTED: Option is selected and displayed within 'Closure Reason'
        EXPECTED: 'CONTINUE' button becomes enabled
        """
        self.site.wait_splash_to_hide(7)
        self.assertFalse(self.site.account_closure.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is not disabled')
        options = self.site.account_closure.items
        self.assertTrue(options, msg=f'"{options}" are not available')
        options[0].click()
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')

    def test_002_tap_continue(self):
        """
        DESCRIPTION: Tap CONTINUE
        EXPECTED: Options to CLOSE
        EXPECTED: Bingo/Casino/Poker & Sports are available.
        """
        self.site.account_closure.continue_button.click()
        self.assertEqual(self.device.active_tab_title(), vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE,
                         msg=f'"{vec.account.ACCOUNT_CLOSURE}" page title is incorrect. Page title is "{self.device.active_tab_title()}" instead of "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE}"')
        sections = list(self.site.service_closure.items_as_ordered_dict.keys())
        try:
            self.assertListEqual(sections, vec.bma.ACCOUNT_CLOSURE_SECTIONS,
                                 msg=f'Actual options list: "{sections}" is not same as Expected options list: "{vec.bma.ACCOUNT_CLOSURE_SECTIONS}"')
        except Exception:
            for i in range(len(sections)):
                self.assertIn(sections[i], vec.bma.ACCOUNT_CLOSURE_SECTIONS,
                              msg=f'Actual option: "{sections[i]}" is not present in the Expected options: "{vec.bma.ACCOUNT_CLOSURE_SECTIONS}"')

    def test_003_choose_any_options_or_close_all_the_accounts(self):
        """
        DESCRIPTION: Choose any options or Close All the accounts
        EXPECTED: Next page shows the user about the selection for the products to be closed with Consequences and Reopening along with options to choose DURATION & REASON FOR CLOSURE
        EXPECTED: with  CONTINUE button disabled.
        """
        self.site.service_closure.close_all_button.click()
        self.assertTrue(self.site.service_closure.duration_options.is_displayed(),
                        msg='"Duration" options are not available')
        self.assertTrue(self.site.service_closure.reason_options.is_displayed(),
                        msg='"Reason" options are not available')
        self.assertFalse(self.site.service_closure.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is not disabled')

    def test_004_chose_any_options_for_duration__reason_for_closure_and_then_click_continue_button_becomes_enabled(self):
        """
        DESCRIPTION: Chose any options for DURATION & REASON FOR CLOSURE and then click 'CONTINUE' (button becomes enabled)
        EXPECTED: Pop up displayed with the following message:
        EXPECTED: Successfully closed: Bingo,Casino,Poker & Sports message is shown
        EXPECTED: Note: The user can still navigate within the app but will not be able to place bets.
        """
        duration_options = self.site.service_closure.duration_options.items
        self.assertTrue(duration_options, msg=f'"{duration_options}" are not available')
        duration_options[0].click()
        self.assertFalse(self.site.service_closure.continue_button.is_enabled(expected_result=False), msg=f'"{vec.account.CONTINUE}" button is not enabled')
        reason_options = self.site.service_closure.reason_options.items
        self.assertTrue(reason_options, msg=f'"{reason_options}" are not available')
        reason_options[0].click()
        self.assertTrue(self.site.service_closure.continue_button.is_enabled(), msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.service_closure.continue_button.perform_click()
        self.site.service_closure.close_button.click()
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT,
                         msg=f'Actual text: "{actual_info_text}" is not same as '
                             f'Expected text: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_INFO_TEXT}"')
        self.navigate_to_page(name='sport/football')
        self.assertTrue(self.site.wait_content_state(vec.olympics.FOOTBALL),
                        msg='"User" is not able to navigate within the app')
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category()
        else:
            selection_ids = self.ob_config.add_autotest_premier_league_football_event(in_play_event=False).selection_ids
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        self.place_and_validate_single_bet()
        sleep(3)  # Getting attribute error due to synchronization issue
        actual_message = self.get_betslip_content().suspended_account_warning_message.text
        self.assertEqual(actual_message, vec.betslip.ACCOUNT_SUSPENDED,
                         msg=f'Actual suspension message: "{actual_message}" is not same as expected suspension message: "{vec.betslip.ACCOUNT_SUSPENDED}"')
