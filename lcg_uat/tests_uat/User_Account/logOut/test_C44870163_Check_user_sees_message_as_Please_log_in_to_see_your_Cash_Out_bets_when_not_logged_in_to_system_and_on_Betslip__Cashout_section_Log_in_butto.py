import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.crl_uat
@pytest.mark.desktop
@vtest
class Test_C44870163_Check_user_sees_message_as_Please_log_in_to_see_your_Cash_Out_bets_when_not_logged_in_to_system_and_on_Betslip__Cashout_section_Log_in_button_is_available(Common):
    """
    TR_ID: C44870163
    NAME: Check user sees message as 'Please log in to see your Cash Out bets.' when not logged in to system and on Betslip -> Cashout section. Log in button is available
    DESCRIPTION: Check user sees message as 'Please log in to see your Cash Out bets.' when not logged in to system and on Betslip -> Cashout section. Log in button is available
    PRECONDITIONS: User not logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='homepage')

    def test_002_navigate_to_my_bets_section___cashout_tab(self):
        """
        DESCRIPTION: Navigate to My Bets section --> Cashout Tab
        EXPECTED: User navigated to Cashout tab
        """
        if self.device_type == 'desktop':
            self.site.open_my_bets_cashout()
        else:
            self.navigate_to_page(name='cashout', test_automation=False)
            self.site.wait_content_state(state_name='Cashout')

    def test_003_verify__please_login_to_see_your_cash_out_bets_message_once_user_navigated_to_cashout_tab(self):
        """
        DESCRIPTION: Verify  'Please login to see your Cash Out bets message once user navigated to cashout tab
        EXPECTED: Message is displayed
        """
        self.__class__.cashouts = self.site.cashout.tab_content
        actual_text = self.cashouts.please_login_text
        self.assertEqual(actual_text, vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual text: "{actual_text}" is not equal with the'
                             f'Expected text: "{vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE}"')

    def test_004_verify_login_button_available_and_use_can_log_in_to_view_cashout_tab(self):
        """
        DESCRIPTION: Verify Login button available and use can log in to view cashout tab
        EXPECTED: User logs in to cashout tab
        """
        self.assertTrue(self.cashouts.has_login_button(), msg='Login button not displayed.')
        self.cashouts.login_button.click()

        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        dialog.username = tests.settings.betplacement_user
        dialog.password = tests.settings.default_password
        dialog.click_login()
        if self.site.is_cookie_banner_shown():
            self.site.cookie_banner.ok_button.click()
        if self.device_type == "mobile":
            if self.site.root_app.has_timeline_overlay_tutorial(timeout=15, expected_result=True):
                self.site.timeline_tutorial_overlay.close_icon.click()
        if self.device_type == 'desktop':
            current_tab = self.cashouts.grouping_buttons.current
        else:
            current_tab = self.site.cashout.tabs_menu.current
        self.assertEqual(current_tab, vec.bet_history.CASH_OUT_TAB_NAME,
                         msg=f'Actual text: "{current_tab}" is not as'
                             f'Expected text: "{vec.bet_history.CASH_OUT_TAB_NAME}"')

        cash_out_bets = self.cashouts.accordions_list.items_as_ordered_dict
        if len(cash_out_bets) > 0:
            self.assertTrue(cash_out_bets, msg='Cashout tab has no bets to display.')
        else:
            cash_out_text = self.cashouts.accordions_list.no_bets_text
            self.assertEqual(cash_out_text, vec.bet_history.NO_CASHOUT_BETS,
                             msg=f'Actual text: "{cash_out_text}" is not equal with the'
                                 f'Expected text: "{vec.bet_history.NO_CASHOUT_BETS}"')
