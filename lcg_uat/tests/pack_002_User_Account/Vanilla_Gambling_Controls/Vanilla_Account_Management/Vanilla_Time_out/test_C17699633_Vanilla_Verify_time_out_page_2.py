import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C17699633_Vanilla_Verify_time_out_page_2(BaseUserAccountTest):
    """
    TR_ID: C17699633
    NAME: [Vanilla] Verify time-out page 2
    DESCRIPTION: This test case verifies the 2nd page of time-out
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure & Reopening
    PRECONDITIONS: User selects the third option - 'I’d like to take an irreversible time-out or exclude myself from gaming', selects the time-out period and the reason of closure (**remember selected date**)
    """
    keep_browser_open = True
    card_number = '5137651100600001'

    def test_000_pre_conditions(self):
        """"
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls
        """
        user_data = self.gvc_wallet_user_client.register_new_user()
        self.username = user_data.username
        self.add_card_and_deposit(username=self.username,
                                  card_number=self.card_number,
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
        self.site.wait_splash_to_hide(6)
        options = self.site.account_closure.items
        self.assertTrue(options, msg=f'"{options}" are not available')
        options[1].click()

    def test_001_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: The confirmation screen of time-out is displayed:
        EXPECTED: - the title of the page is 'Take a short time-out',
        EXPECTED: - date and time of the end of time-out,
        EXPECTED: - consequences of a time-out,
        EXPECTED: - information what would happen after confirmation,
        EXPECTED: - "Take a short time-out" button,
        EXPECTED: - "Cancel" button
        """
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(), msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.account_closure.continue_button.click()

        reason_list = []

        for reason in self.site.self_exclusion.reason_options_list:
            reason_list.append(reason.text)

        self.assertListEqual(sorted(reason_list), sorted(list(vec.account.REASON_FOR_TAKING_BREAK)),
                             msg=f'Actual duration list  "{sorted(reason_list)}" is not matching with expected list "{sorted(list(vec.account.REASON_FOR_TAKING_BREAK))}"')

        duration_options_list = []

        for duration in self.site.self_exclusion.duration_options:
            duration_options_list.append(duration.text)

        self.site.self_exclusion.duration_options[0].click()
        self.assertTrue(self.site.self_exclusion.duration_options_btn[0].is_selected(),
                        msg='Duration check-box is not selected')
        self.site.self_exclusion.reason_options_list[0].click()
        self.assertTrue(self.site.self_exclusion.reason_options[0].is_selected(),
                        msg='Reason check-box is not selected')

        self.assertListEqual(sorted(duration_options_list), sorted(list(vec.account.DURATION_TIMEOUT)),
                             msg=f'Actual duration list  "{sorted(duration_options_list)}" is not matching with '
                                 f'expected list "{sorted(list(vec.account.DURATION_TIMEOUT))}"')

        self.assertTrue(self.site.self_exclusion.self_exclusion_link.is_displayed(),
                        msg='Self exclusion link is not present in Take a short time-out page')
        self.assertTrue(self.site.self_exclusion.continue_button.is_displayed(),
                        msg='Continue button is not present in Take a short time-out page')
        self.assertTrue(self.site.self_exclusion.cancel_button.is_displayed(),
                        msg='Cancel button is not present in Take a short time-out page')

    def test_002_validate_date_and_time_of_time_out(self):
        """
        DESCRIPTION: Validate date and time of time-out
        EXPECTED: Date and time is the same as the one selected as duration
        """
        self.site.self_exclusion.continue_button.click()
        self.assertTrue(self.site.self_exclusion.is_displayed(), msg=f'"Confirmation screen is not displayed')
        short_timed_out_info_message = self.site.self_exclusion.consequences_desription.text
        self.assertIn(list(vec.account.CONSEQUENCE_DESCRIPTION)[0].upper(), short_timed_out_info_message.upper(),
                      msg=f'Short time out message "{list(vec.account.CONSEQUENCE_DESCRIPTION)[0]}" is '
                          f'not in expected "{short_timed_out_info_message.upper()}"')
        self.assertIn(list(vec.account.CONSEQUENCE_DESCRIPTION)[1].upper(), short_timed_out_info_message.upper(),
                      msg=f'Short time out message "{list(vec.account.CONSEQUENCE_DESCRIPTION)[1]}" is '
                          f'not in expected "{short_timed_out_info_message.upper()}"')
        title_and_date = self.site.self_exclusion.date_time
        self.assertTrue(title_and_date, msg='Time and date is not displayed')
