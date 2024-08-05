import pytest
import tests
import voltron.environments.constants as vec
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
class Test_C58694810_Verify_Betslip_behavior_for_user_with_without_Overask_available(BaseBetSlipTest):
    """
    TR_ID: C58694810
    NAME: Verify Betslip behavior for user with/without  Overask available
    DESCRIPTION: This test case verifies Betslip behavior for user with/without  Overask available
    PRECONDITIONS: Overask functionality is enabled for Event Type and User:
    PRECONDITIONS: Confluence Instruction - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: User #1 - Overask enabled for user
    PRECONDITIONS: User #2 - Overask disabled for user
    PRECONDITIONS: 1. Open the app
    PRECONDITIONS: 2. Log in to application with User #1
    PRECONDITIONS: 3. Add selection available for Overask to Betslip
    PRECONDITIONS: 4. Enter stake value which is higher than maximum bet limit for added selection
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.site.login(username=tests.settings.overask_enabled_user)
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -> BI Requests)
        """
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_log_out_from_the_application_with_user_1for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self, flag=True):
        """
        DESCRIPTION: Log Out from the application with User #1:
        DESCRIPTION: For Desktop: Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: For Web Mobile: Refresh the page
        DESCRIPTION: For Wrappers: Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Betslip is Empty
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
        if flag:
            self.assertTrue(self.get_betslip_content().no_selections_title,
                            msg='Selections added in preconditions are still present in betslip')
            self.site.close_betslip()

    def test_003_log_in_to_application_with_user_2_wo_overask_available(self):
        """
        DESCRIPTION: Log in to application with User #2 (w/o Overask available)
        EXPECTED: - User is logged in
        """
        self.site.login(username=tests.settings.disabled_overask_user)

    def test_004_add_the_selection_from_preconditions_to_betslip_with_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Add the selection from preconditions to Betslip with stake value which is higher than maximum bet limit for added selection
        EXPECTED: - Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet()

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - 'Maximum stake of <currency><amount>' ( **Coral** ) /'Sorry, the maximum stake for this bet is <currency><amount>' ( **Ladbrokes** ) error message is displayed above stake section
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake_name, stake = list(singles_section.items())[0]
        error_message = stake.wait_for_error_message()
        int_num = [int(x) for x in error_message.split() if x.isdigit()]
        error_message = error_message.replace(str(int_num[0]), "{:.2f}".format(int_num[0]))
        expected_max_bet_msg = vec.betslip.MAX_STAKE.format(self.max_bet)
        self.assertEqual(error_message, expected_max_bet_msg,
                         msg=f'Actual message: "{error_message}"'
                             f'is not as expected: "{expected_max_bet_msg}"')

    def test_006_log_out_from_the_application_with_user_2for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application with User #2:
        DESCRIPTION: For Desktop: Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: For Web Mobile: Refresh the page
        DESCRIPTION: For Wrappers: Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Selection is shown in Betslip
        """
        self.test_002_log_out_from_the_application_with_user_1for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(flag=False)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
