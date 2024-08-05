import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C28091_Auto_Login_to_Casino_for_Desktop(Common):
    """
    TR_ID: C28091
    NAME: Auto Login to Casino for Desktop
    DESCRIPTION: This test case verifies auto login from Oxygen Desktop application to Third-Party integrations
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-8276 Auto Login - Oxygen to Casino/Games (Portal)
    PRECONDITIONS: Check for the existence of the following cookies:
    PRECONDITIONS: *   **sportsbookToken** - the temp token received from PAS API’s login response
    PRECONDITIONS: *   **sportsbookUsername** - the username of logged in user
    PRECONDITIONS: *   **userLoginTime** - the login successful timestamp (in UNIX)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen application on Desktop
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_without_remeber_me_option(self):
        """
        DESCRIPTION: Log in without 'Remeber me' option
        EXPECTED: User is logged in successfully
        """
        pass

    def test_003_click_casino_tab_on_main_navigation_menu(self):
        """
        DESCRIPTION: Click 'Casino' tab on Main Navigation Menu
        EXPECTED: *   User is navigated to Casino app under global domain - **coral.co.uk;**
        EXPECTED: *   User is logged in automatically with credentials entered on step #2.
        """
        pass

    def test_004_log_outand_navigate_to_oxygen_application(self):
        """
        DESCRIPTION: Log out and Navigate to Oxygen application
        EXPECTED: * Homepage is opened
        EXPECTED: * User is logged out
        """
        pass

    def test_005_login_with_remember_me_option_and_repeat_steps_3_4(self):
        """
        DESCRIPTION: Login with 'Remember me' option and repeat steps #3-4
        EXPECTED: * Homepage is opened
        EXPECTED: * User is logged in
        """
        pass

    def test_006_repeat_steps__1_5_but_click_games_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'Games' tab on step #3
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps__1_5_but_click_live_casino_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'Live Casino' tab on step #3
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps__1_5_but_click_slots_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'Slots' tab on step #3
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps__1_5_but_click_bingo_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'Bingo' tab on step #3
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps__1_5_but_click_poker_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'Poker' tab on step #3
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps__1_5_but_click_mobile_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'Mobile' tab on step #3
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps__1_5_but_click_vip_tab_on_step_3(self):
        """
        DESCRIPTION: Repeat steps # 1-5 but click 'VIP' tab on step #3
        EXPECTED: 
        """
        pass

    def test_013_navigate_between_tabs(self):
        """
        DESCRIPTION: Navigate between tabs
        EXPECTED: User stays logged in
        """
        pass
