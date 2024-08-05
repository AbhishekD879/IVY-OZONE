import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C28238_Verify_User_Session_Support(Common):
    """
    TR_ID: C28238
    NAME: Verify User Session Support
    DESCRIPTION: This test case verifies how user session is supported in Invictus application
    DESCRIPTION: *To Update:* With Vanilla session behaviour has changed, also according to https://jira.egalacoral.com/browse/BMA-46278 no more 'session timed out' popups
    PRECONDITIONS: Private mode is switched off on device browser
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Invictus in one browser tab
    PRECONDITIONS: *   Login to Invictus in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    PRECONDITIONS: Partly automated - AUTOTEST [C9698303]
    PRECONDITIONS: -------
    PRECONDITIONS: In order to close user session -> Navigate to IMS -> Player Info -> Click on Close Sessions button.
    PRECONDITIONS: In Openapi WebSocket connection messaged with ID: 33004 (sessionToken:{token}) is received when session is ended.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on 'Log In' button
        EXPECTED: 'Log in' form is opened
        """
        pass

    def test_003_enter_valid_credentials___tap_on_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials -> tap on 'Log In' button
        EXPECTED: User is logged in successfully. Appropriate page is displayed:
        EXPECTED: *   Page from which user made log in if he has positive balance
        EXPECTED: *   Quick Deposit page if user's balance is less or equal 0
        """
        pass

    def test_004_navigate_through_the_application(self):
        """
        DESCRIPTION: Navigate through the application
        EXPECTED: User stays logged in
        """
        pass

    def test_005_reload_app_via_browser_refresh_button(self):
        """
        DESCRIPTION: Reload app via browser refresh button
        EXPECTED: User stays logged in
        """
        pass

    def test_006_kill_app_on_the_device_browser_but_make_sure_app_tab_was_opened_in_the_moment_of_closing_browser__close_browser(self):
        """
        DESCRIPTION: Kill app on the device browser (but make sure app tab was opened in the moment of closing browser) / close browser
        EXPECTED: Application is closed
        """
        pass

    def test_007_open_browser(self):
        """
        DESCRIPTION: Open browser
        EXPECTED: User stays logged in
        """
        pass

    def test_008_press_home_button_on_the_device(self):
        """
        DESCRIPTION: Press 'Home' button on the device
        EXPECTED: App goes to the background
        """
        pass

    def test_009_app_is_in_background___wait_for_a_fewminuteshours(self):
        """
        DESCRIPTION: App is in background -> wait for a few minutes/hours
        EXPECTED: 
        """
        pass

    def test_010_open_app(self):
        """
        DESCRIPTION: Open app
        EXPECTED: User is logged in
        """
        pass

    def test_011_leave_an_app_in_background_until_user_session_is_timed_out(self):
        """
        DESCRIPTION: Leave an app in background until user session is timed out
        EXPECTED: 
        """
        pass

    def test_012_open_app_refresh_it(self):
        """
        DESCRIPTION: Open app, refresh it
        EXPECTED: Ladbrokes:
        EXPECTED: 1.  *User is logged out*
        EXPECTED: 2.  *Shouldn't appear any Messages*
        EXPECTED: Coral:
        EXPECTED: 1. User is logged out
        EXPECTED: 2. Message appears 'Your session is over. Please log in again'
        """
        pass

    def test_013_log_in_to_app___go_to_background(self):
        """
        DESCRIPTION: Log in to app -> Go to background
        EXPECTED: 
        """
        pass

    def test_014_lock_device(self):
        """
        DESCRIPTION: Lock device
        EXPECTED: 
        """
        pass

    def test_015_unlock_device___open_app(self):
        """
        DESCRIPTION: Unlock device -> open app
        EXPECTED: User is logged in
        """
        pass

    def test_016_repeat_steps__14___16_but_is_step_15_wait_until_device_is_locked_automatically(self):
        """
        DESCRIPTION: Repeat steps # 14 - 16 but is step 15 wait until device is locked automatically
        EXPECTED: 
        """
        pass

    def test_017_app_is_in_foreground___do_not_do_any_actions_for_a_fewminutes__hours(self):
        """
        DESCRIPTION: App is in foreground - >do not do any actions for a few minutes / hours
        EXPECTED: 
        """
        pass

    def test_018_interact_the_app(self):
        """
        DESCRIPTION: Interact the app
        EXPECTED: User is logged in
        """
        pass

    def test_019_app_is_in_foreground__wait_untill_user_session_is_timed_out(self):
        """
        DESCRIPTION: App is in foreground-> wait untill user session is timed out
        EXPECTED: User is logged out
        """
        pass

    def test_020_open_app_refresh_it(self):
        """
        DESCRIPTION: Open app, refresh it
        EXPECTED: Ladbrokes
        EXPECTED: 1.  *User is logged out*
        EXPECTED: 2.  *Shouldn't appear any Messages*
        EXPECTED: Coral:
        EXPECTED: 1. User is logged out
        EXPECTED: 2. Message appears 'Your session is over. Please log in again
        """
        pass

    def test_021_login_to_app___app_is_in_foreground_mode(self):
        """
        DESCRIPTION: Login to app -> app is in foreground mode
        EXPECTED: 
        """
        pass

    def test_022_lock_device(self):
        """
        DESCRIPTION: Lock device
        EXPECTED: 
        """
        pass

    def test_023_unlock_device___interact_app(self):
        """
        DESCRIPTION: Unlock device -> interact app
        EXPECTED: User is logged in
        """
        pass

    def test_024_repeat_steps__24_26_but_in_step_5_wait_until_device_is_locked_automatically(self):
        """
        DESCRIPTION: Repeat steps # 24-26 but in step #5 wait until device is locked automatically
        EXPECTED: 
        """
        pass

    def test_025_log_in_to_the_app___close_browser_tab(self):
        """
        DESCRIPTION: Log in to the app -> close browser tab
        EXPECTED: 
        """
        pass

    def test_026_open_new_tab___enter_url_for_app(self):
        """
        DESCRIPTION: Open new tab -> enter URL for app
        EXPECTED: User is logged in
        """
        pass

    def test_027_log_in_in_different_tabs___log_out_from_one_tab(self):
        """
        DESCRIPTION: Log in in different tabs -> log out from one tab
        EXPECTED: 
        """
        pass

    def test_028_go_to_another_tab___reload_page(self):
        """
        DESCRIPTION: Go to another tab ->  reload page
        EXPECTED: 1.  User is logged out
        EXPECTED: 2.  Server logs out user from all tabs
        """
        pass
