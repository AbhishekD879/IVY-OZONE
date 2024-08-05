import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.other
@vtest
class Test_C44870164_Check_user_sees_message_as_Please_log_in_to_see_your_Open_Bets_when_not_logged_in_to_system_and_on_Betslip__Openebst_section_Log_in_button_is_available(Common):
    """
    TR_ID: C44870164
    NAME: Check user sees message as 'Please log in to see your Open Bets.' when not logged in to system and on Betslip -> Openebst section. Log in button is available
    DESCRIPTION: Check user sees message as 'Please log in to see your Open Bets.' when not logged in to system and on Betslip -> Openebst section. Log in button is available
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_navigate_to_my_bets_section____open_bets_tab(self):
        """
        DESCRIPTION:For Desktop: Navigate to My Bets section --> Open Bets tab
        DESCRIPTION:For mobile/tablet: Navigate to 'My Bets'->'Open bets' via 'Cashout' from the Footer menu
        EXPECTED: User navigated to Open Bets tab
        """
        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
        else:
            if self.brand == 'bma':
                self.site.navigation_menu.items_as_ordered_dict.get(vec.bet_history.CASH_OUT_TAB_NAME).click()
                self.site.cashout.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
            else:
                self.navigate_to_page(name='open-bets')
                self.site.wait_content_state(state_name='OpenBets')

    def test_003_verify_please_login_to_see_your_open_bets_message_once_user_navigated_to_cashout_tab(self):
        """
        DESCRIPTION: Verify 'Please login to see your Open bets message once user navigated to cash out tab
        EXPECTED: Message is displayed
        """
        self.__class__.open_bet = self.site.open_bets.tab_content
        actual_text = self.open_bet.please_login_text
        self.assertEqual(actual_text, vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual text: {actual_text} is not same as'
                             f'Expected text: {vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE}')

    def test_004_verify_login_button_available_and_users_can_log_in_to_view_open_bets_tab(self):
        """
        DESCRIPTION: Verify Login button available and users can log in to view Open Bets tab
        EXPECTED: User logs in to Open bets tab and can see all available open bets
        """
        if self.brand == 'bma':
            self.assertTrue(self.open_bet.has_login_button(), msg='Login button not displayed.')
            self.open_bet.login_button.click()
            self.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
            self.dialog.username = tests.settings.betplacement_user
            self.dialog.password = tests.settings.default_password
            self.dialog.click_login()
        else:
            self.site.login()
        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
            current_tab = self.site.open_bets.grouping_buttons.current
        else:
            current_tab = self.site.open_bets.tabs_menu.current
        self.assertEqual(current_tab, vec.bet_history.OPEN_BETS_TAB_NAME,
                         msg=f'Actual text: "{current_tab}" is not as'
                             f'Expected text: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
        open_bets_item = self.open_bet.accordions_list.items_as_ordered_dict
        if len(open_bets_item) > 0:
            self.assertTrue(open_bets_item, msg='OPEN BETS tab has no bets to display.')
        else:
            no_open_bets_text = self.open_bet.accordions_list.no_bets_text
            self.assertEqual(no_open_bets_text, vec.bet_history.NO_OPEN_BETS,
                             msg=f'Actual text: "{no_open_bets_text}" is not equal with the'
                                 f'Expected text: "{vec.bet_history.NO_OPEN_BETS}"')
