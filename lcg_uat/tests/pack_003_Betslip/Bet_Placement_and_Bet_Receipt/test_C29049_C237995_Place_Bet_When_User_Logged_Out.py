import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29049_C237995_Place_Bet_When_User_Logged_Out(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29049
    TR_ID: C237995
    NAME: Verify Bet Placement when user is Logged Out and when user enter invalid credentials for Login
    """
    keep_browser_open = True
    expected_error_message = None
    selection_id = None
    dialog = None

    def check_error_message(self, expected_error_message):
        self.dialog.wait_error_message()
        error_message = self.dialog.error_message
        self.assertIn(error_message, expected_error_message,
                      msg=f'Error message "{error_message}" is not the same as expected "{expected_error_message}"')

    def test_001_create_test_event_get_error_message_from_ims(self):
        """
        DESCRIPTION: Creating test event
        DESCRIPTION: Login and logout
        EXPECTED: Get error message before test execution
        """
        self.__class__.username = tests.settings.betplacement_user
        self.__class__.expected_error_message = [vec.gvc.INCORRECT_CREDENTIALS, vec.gvc.INCORRECT_PASSWORD_ERROR]

        if tests.settings.backend_env != 'prod':
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        else:
            self.__class__.selection_ids = self.get_active_event_selections_for_category()

        # to avoid situation when dialogs affect test steps
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.logout()

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.__class__.selection_id = list(self.selection_ids.values())[0]
        # timeout needed here as it open betslip sometimes before UI loaded user logging out process
        self.open_betslip_with_selections(selection_ids=self.selection_id, timeout=3)
        self.place_single_bet()

    def test_003_verify_login_dialog_appears(self):
        """
        DESCRIPTION: Check if login dialog shows up
        EXPECTED: Check if you are still on BetSlip page
        """
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='No login dialog present on page')

    def test_004_verify_user_is_not_logged_in(self):
        """
        DESCRIPTION: Enter invalid credentials of user's account -> Tap on 'Log In and Place Bet' button
        EXPECTED: *   Error message is displayed on 'Log In' pop-up
        EXPECTED: *   User is NOT logged in and 'Log In' pop-up is still displaying
        EXPECTED: *   Betslip is NOT closed
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = 'incorrect'
        self.dialog.click_login()
        self.check_error_message(expected_error_message=self.expected_error_message)
        self.dialog.close_dialog()
        self.assertTrue(self.get_betslip_content().is_displayed(), msg='Betslip is closed')

    def test_005_use_betplacement_user_to_login(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO **pop-ups are expected after login -> Tap 'Log In and Place Bet'
        EXPECTED: User is logged in
        EXPECTED: Betslip is NOT refreshed
        EXPECTED: Bets are placed successfully
        EXPECTED: User is redirected to Bet Receipt page
        """
        self.get_betslip_content().bet_now_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='Login dialog is not present on page')
        dialog.username = self.username
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')
        try:
            dialog_displayed = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
            self.assertTrue(dialog_displayed, msg='Login dialog is not present on page')
            self.site.close_all_dialogs(timeout=5, async_close=False)
            betslip = self.get_betslip_content()
            self.assertTrue(betslip.betslip_sections_list, msg='*** No bets found in BetSlip')
            self.assertTrue(betslip.bet_now_button.is_enabled(), msg='Bet Now button is not enabled')
            betslip.bet_now_button.click()
        except Exception as e:
            self.site.close_all_dialogs(timeout=5, async_close=False)
        self.site.bet_receipt.is_displayed()
