import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C17354958_Vanilla_Mini_Games_Handle_Request_Response(Common):
    """
    TR_ID: C17354958
    NAME: [Vanilla]  Mini Games: Handle Request/Response
    DESCRIPTION: This test case verifies handle the request/response between iFrame and Games content
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS
    PRECONDITIONS: 3. Developer Tools is opened - "Verbose" mode is ON, postMessages debugger is installed (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
    PRECONDITIONS: 4. User is logged out
    """
    keep_browser_open = True

    def test_001_load_desktop_appverify_desktop_mini_games_iframe(self):
        """
        DESCRIPTION: Load Desktop App
        DESCRIPTION: Verify Desktop Mini Games iFrame
        EXPECTED: Spinner is displayed while MiniGames iFrame is loading
        EXPECTED: Desktop Mini Games iFrame is displayed in Right Column right under Betslip widget
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        pass

    def test_002_tap_on_anywhere_inside_mini_games_iframe(self):
        """
        DESCRIPTION: Tap on anywhere inside Mini Games iFrame
        EXPECTED: Log in popup appears
        EXPECTED: PostMessage {type: 'SHOW_LOGIN'} notification is visible in Console
        """
        pass

    def test_003_enter_username_and_passwordtap_on_log_in_button(self):
        """
        DESCRIPTION: Enter Username and Password
        DESCRIPTION: Tap on Log in button
        EXPECTED: User is logged in
        """
        pass

    def test_004_observe_mini_games_iframe(self):
        """
        DESCRIPTION: Observe Mini Games iFrame
        EXPECTED: Spinner is displayed while MiniGames iFrame is loading
        EXPECTED: Mini Games view items appeared inside Mini Games iFrame
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        pass

    def test_005_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: Mini Games iFrame with Play Now button appears
        """
        pass

    def test_006_tap_on_login_button_from_the_headerenter_username_and_passwordtap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on Login button from the Header
        DESCRIPTION: Enter Username and Password
        DESCRIPTION: Tap on Log in button
        EXPECTED: User is logged in
        """
        pass

    def test_007_observe_mini_games_iframe(self):
        """
        DESCRIPTION: Observe Mini Games iFrame
        EXPECTED: Spinner is displayed while MiniGames iFrame is loading
        EXPECTED: Mini Games view items appeared inside Mini Games iFrame
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        pass
