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
class Test_C26832987_Back_button_is_shown_if_user_navigates_from_Homepage(Common):
    """
    TR_ID: C26832987
    NAME: Back button is shown if user navigates from Homepage
    DESCRIPTION: TC verifies if back button is shown for user while navigating through the app
    PRECONDITIONS: App is installed.
    PRECONDITIONS: Some user exist in system.
    """
    keep_browser_open = True

    def test_001_start_the_app(self):
        """
        DESCRIPTION: Start the app
        EXPECTED: App main screen appears
        """
        pass

    def test_002_navigate_trough_the_app_go_to_some_sporteg_englend___some_league_eg_premiere_league___some_event___open_some_market_switch(self):
        """
        DESCRIPTION: Navigate trough the app Go to some sport(e.g. Englend) -> some league (e.g. Premiere League) -> some event -> open some market switch
        EXPECTED: Back button is shown
        """
        pass

    def test_003_press_back_button(self):
        """
        DESCRIPTION: Press back button
        EXPECTED: User get beck to previous screen and still shown
        """
        pass

    def test_004_press_back_button_till_user_get_to_home_screen(self):
        """
        DESCRIPTION: Press back button till user get to home screen
        EXPECTED: Home screen appears. Back button disappears
        """
        pass

    def test_005_login_with_user(self):
        """
        DESCRIPTION: Login with user
        EXPECTED: User logged in
        """
        pass

    def test_006_repeat_steps_1_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-5 for logged in user
        EXPECTED: Header bar behaves the same.
        """
        pass
