import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2  # Never works on tst2 endpoints
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C17354958_Vanilla__Mini_Games_Handle_Request_Response(BaseUserAccountTest):
    """
    TR_ID: C17354958
    VOL_ID: C28946360
    NAME: [Vanilla]  Mini Games: Handle Request/Response
    DESCRIPTION: This test case verifies handle the request/response between iFrame and Games content
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS
    PRECONDITIONS: 3. Developer Tools is opened - "Verbose" mode is ON, postMessages debugger is installed
    (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
    PRECONDITIONS: 4. User is logged out
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_load_desktop_appverify_desktop_mini_games_iframe(self):
        """
        DESCRIPTION: Load Desktop App
        DESCRIPTION: Verify Desktop Mini Games iFrame
        EXPECTED: Spinner is displayed while MiniGames iFrame is loading
        EXPECTED: Desktop Mini Games iFrame is displayed in Right Column right under Betslip widget
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        self.__class__.name = self.get_filtered_widget_name(self.cms_config.constants.MINI_GAMES_TYPE_NAME)
        self.site.wait_content_state(state_name='Homepage')
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')

    def test_002_tap_on_anywhere_inside_mini_games_iframe(self):
        """
        DESCRIPTION: Tap on anywhere inside Mini Games iFrame
        EXPECTED: Log in popup appears
        EXPECTED: PostMessage {type: 'SHOW_LOGIN'} notification is visible in Console
        """
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        wait_for_result(lambda : mini_games.expand(), timeout=10)
        self.assertTrue(mini_games.is_expanded(), msg='"Mini Games" widget is not expanded')
        mini_games.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')

    def test_003_enter_username_and_passwordtap_on_log_in_button(self):
        """
        DESCRIPTION: Enter Username and Password
        DESCRIPTION: Tap on Log in button
        EXPECTED: User is logged in
        """
        self.__class__.user = tests.settings.betplacement_user
        self.dialog.username = self.user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        try:
            if self.site.root_app.has_fanzone_cb_overlay(timeout=5, expected_result=True):
                self.site.fanzone_cb_overlay.close_button_click()
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            self._logger.warning(e)
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_004_observe_mini_games_iframe(self):
        """
        DESCRIPTION: Observe Mini Games iFrame
        EXPECTED: Spinner is displayed while MiniGames iFrame is loading
        EXPECTED: Mini Games view items appeared inside Mini Games iFrame
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')

    def test_005_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: Mini Games iFrame with Play Now button appears
        """
        self.site.logout()
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')

    def test_006_tap_on_login_button_from_the_headerenter_username_and_passwordtap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on Login button from the Header
        DESCRIPTION: Enter Username and Password
        DESCRIPTION: Tap on Log in button
        EXPECTED: User is logged in
        """
        self.site.login(username=self.user)

    def test_007_observe_mini_games_iframe(self):
        """
        DESCRIPTION: Observe Mini Games iFrame
        EXPECTED: Spinner is displayed while MiniGames iFrame is loading
        EXPECTED: Mini Games view items appeared inside Mini Games iFrame
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')
