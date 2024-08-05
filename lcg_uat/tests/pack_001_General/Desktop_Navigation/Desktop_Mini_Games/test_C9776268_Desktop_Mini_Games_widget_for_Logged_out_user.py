import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.waiters import wait_for_haul


# @pytest.mark.tst2 # NA for tst env
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9776268_Desktop_Mini_Games_widget_for_Logged_out_user(BaseUserAccountTest):
    """
    TR_ID: C9776268
    NAME: Desktop Mini Games widget for Logged out user
    DESCRIPTION: This test case verifies Desktop Mini games functionality for logged out user.
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_load_app_on_desktop_as_a_logged_out_user_and_verify_mini_games_widget(self):
        """
        DESCRIPTION: Load app on Desktop as a logged out user and verify Mini Games widget
        EXPECTED: * Mini Games widget is displayed under Betslip widget.
        EXPECTED: * A Mini Games iframe displayed inside of widget with Play Now button
        """
        self.__class__.name = self.get_filtered_widget_name(self.cms_config.constants.MINI_GAMES_TYPE_NAME)
        self.site.wait_content_state(state_name='Homepage')
        self.__class__.mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(self.mini_games, msg='Mini Games widget is not displayed')

    def test_002_click_play_now_button_inside_iframe(self):
        """
        DESCRIPTION: Click Play Now button inside iframe
        EXPECTED: Login pop up opens
        """
        self.mini_games.expand()
        wait_for_haul(10)
        self.assertTrue(self.mini_games.is_expanded(), msg='"Mini Games" widget is not expanded')
        self.mini_games.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')

    def test_003_close_login_pop_up(self):
        """
        DESCRIPTION: Close login pop up
        EXPECTED: 'Please log in to play' message displayed inside iframe.
        """
        self.dialog.close_dialog()
        self.assertFalse(vec.dialogs.DIALOG_MANAGER_LOG_IN in self.site.dialog_manager.items_as_ordered_dict,
                         msg='"Log In" dialog should not be displayed on the screen')
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')
        mini_games.expand()
        self.assertTrue(mini_games.is_expanded(), msg='"Mini Games" widget is not expanded')
        mini_games.click()
        self.site.login()
        mini_games = self.site.right_column.items_as_ordered_dict.get(self.name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')

    def test_004_click_please_log_in_to_play_message(self):
        """
        DESCRIPTION: Click 'Please log in to play' message
        EXPECTED: * Login pop up opens
        """
        # Covered in step 3

    def test_005_login_to_app_with_oxygen_user(self):
        """
        DESCRIPTION: Login to app with oxygen user
        EXPECTED: * User is logged in
        EXPECTED: * Login pop up closes and user is able to play mini games.
        """
        # Covered in step 3
