import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C58694681_Login_Logout_flow_for_two_different_users_during_overask(BaseBetSlipTest):
    """
    TR_ID: C58694681
    NAME: Login/Logout flow for two different users  during overask
    DESCRIPTION: This test case verifies Overask process when different users logged in/logged out
    PRECONDITIONS: Overask functionality is enabled for Event Type and User:
    PRECONDITIONS: Confluence Instruction - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: User #1 - has Overask enabled
    PRECONDITIONS: User #2 - has Overask enabled
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in to application with User #1
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.username_1 = tests.settings.betplacement_user
        self.__class__.username_2 = tests.settings.betplacement_user
        self.site.login(username=self.username_1)

    def test_001_add_selection_available_for_overask_to_betslip(self):
        """
        DESCRIPTION: Add selection available for Overask to Betslip
        EXPECTED: - Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_open_betslip___enter_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Open Betslip -> Enter stake value which is higher than maximum bet limit for added selection
        EXPECTED: - Betslip is opened
        EXPECTED: - Stake value is entered
        """
        self.__class__.bet_amount = self.max_bet + 1

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -> BI Requests)
        """
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_log_out_with_user_1for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out with User #1:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User #1 is logged out
        EXPECTED: - Added selection from step#1 is cleared
        EXPECTED: - Betslip is empty
        """
        if self.device_type == 'mobile':
            self.device.refresh_page()
            self.site.wait_splash_to_hide(timeout=10)
        self.site.wait_content_state_changed()
        self.site.logout(timeout=20)
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.wait_logged_out(), msg='User is still logged in')
        self.site.close_all_dialogs(timeout=3)
        self.site.wait_content_state('Homepage')
        self.site.open_betslip()
        self.assertTrue(self.get_betslip_content().no_selections_title,
                        msg='Selections added in preconditions are still present in betslip')
        self.site.close_betslip()

    def test_005_log_in_with_user_2_to_application(self):
        """
        DESCRIPTION: Log in with User #2 to application
        EXPECTED: - User #2 is logged in
        """
        self.site.login(username=self.username_2)

    def test_006_repeat_steps_1_3(self):
        """
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: - Overask review process is started for User #2
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -> BI Requests)
        """
        self.test_001_add_selection_available_for_overask_to_betslip()
        self.test_002_open_betslip___enter_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection()
        self.test_003_tap_place_bet_button()

    def test_007_log_out_with_user_2for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out with User #2:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User #2 is logged out
        EXPECTED: - Overask selection from step#8 is cleared
        EXPECTED: - Betslip is empty
        """
        self.test_004_log_out_with_user_1for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app()

    def test_008_login_to_application_with_user_1_again_and_go_to_the_betslip(self):
        """
        DESCRIPTION: Login to application with User #1 again and go to the Betslip
        EXPECTED: - Betslip is empty
        """
        self.site.login(username=self.username_1)
        self.site.open_betslip()
        self.assertTrue(self.get_betslip_content().no_selections_title,
                        msg='Selections added in preconditions are still present in betslip')
        self.site.close_betslip()
