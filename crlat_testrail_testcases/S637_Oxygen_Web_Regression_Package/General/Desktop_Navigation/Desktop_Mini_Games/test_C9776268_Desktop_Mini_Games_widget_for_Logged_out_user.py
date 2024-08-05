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
class Test_C9776268_Desktop_Mini_Games_widget_for_Logged_out_user(Common):
    """
    TR_ID: C9776268
    NAME: Desktop Mini Games widget for Logged out user
    DESCRIPTION: This test case verifies Desktop Mini games functionality for logged out user.
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS.
    """
    keep_browser_open = True

    def test_001_load_app_on_desktop_as_a_logged_out_user_and_verify_mini_games_widget(self):
        """
        DESCRIPTION: Load app on Desktop as a logged out user and verify Mini Games widget
        EXPECTED: * Mini Games widget is displayed under Betslip widget.
        EXPECTED: * A Mini Games iframe displayed inside of widget with Play Now button
        """
        pass

    def test_002_click_play_now_button_inside_iframe(self):
        """
        DESCRIPTION: Click Play Now button inside iframe
        EXPECTED: Login pop up opens
        """
        pass

    def test_003_close_login_pop_up(self):
        """
        DESCRIPTION: Close login pop up
        EXPECTED: 'Please log in to play' message displayed inside iframe.
        """
        pass

    def test_004_click_please_log_in_to_play_message(self):
        """
        DESCRIPTION: Click 'Please log in to play' message
        EXPECTED: * Login pop up opens
        """
        pass

    def test_005_login_to_app_with_oxygen_user(self):
        """
        DESCRIPTION: Login to app with oxygen user
        EXPECTED: * User is logged in
        EXPECTED: * Login pop up closes and user is able to play mini games.
        """
        pass
