import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # overask cannot be triggered for prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C58694749_Verify_triggering_new_OA_bet_request_with_LOGIN_PLACE_BET(BaseBetSlipTest):
    """
    TR_ID: C58694749
    NAME: Verify triggering new OA bet request with 'LOGIN & PLACE BET'
    DESCRIPTION: This test case verifies Overask functionality when user adds a selection and uses 'LOGIN & PLACE BET' option.
    PRECONDITIONS: Overask functionality is enabled for Event Type and User:
    PRECONDITIONS: Confluence Instruction - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in to the application
    PRECONDITIONS: - Add selection available for Overask to Betslip
    PRECONDITIONS: - Enter stake value which is higher than maximum bet limit for added selection
    PRECONDITIONS: Check parameters in Local Storage:
    PRECONDITIONS: OX.BetSelections
    PRECONDITIONS: OX.overaskPlaceBetsData
    PRECONDITIONS: OX.overaskIsInProgress
    PRECONDITIONS: OX.overaskUsername
    PRECONDITIONS: ![](index.php?/attachments/get/106947951)
    """
    keep_browser_open = True
    max_bet = 0.05

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - Open the app
        PRECONDITIONS: - Log in to the application
        PRECONDITIONS: - Add selection available for Overask to Betslip
        PRECONDITIONS: - Enter stake value which is higher than maximum bet limit for added selection
        PRECONDITIONS: Check parameters in Local Storage:
        PRECONDITIONS: OX.BetSelections
        PRECONDITIONS: OX.overaskPlaceBetsData
        PRECONDITIONS: OX.overaskIsInProgress
        PRECONDITIONS: OX.overaskUsername
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.eventID, self.__class__.selection_id = event_params.event_id, list(event_params.selection_ids.values())[0]
        event_params1 = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.eventID1, self.__class__.selection_id1 = event_params1.event_id, list(event_params1.selection_ids.values())[0]
        self.__class__.username = tests.settings.freebet_user_with_value_0
        self.site.login(username=self.username)

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -> BI Requests)
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.05
        self.place_single_bet()
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')
        key_value1 = self.get_local_storage_cookie_value_as_dict('OX.overaskPlaceBetsData')
        self.assertTrue(key_value1, msg=f'Value of cookie "OX.overaskPlaceBetsData" is blank')
        key_value2 = self.get_local_storage_cookie_value_as_dict('OX.overaskIsInProcess')
        self.assertTrue(key_value2, msg=f'Value of cookie "OX.overaskIsInProcess" is not True')
        key_value3 = self.get_local_storage_cookie_value_as_dict('OX.overaskUsername')
        self.assertEqual(key_value3, self.username,
                         msg=f'Value of cookie "OX.overaskUsername" does not match with "{self.username}')
        key_value4 = self.get_local_storage_cookie_value_as_dict('OX.betSelections')
        self.assertTrue(len(key_value4) > 0, msg=f'cookie "OX.betSelections" is blank')

    def test_002_log_out_from_the_applicationfor_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
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
        self.assertTrue(self.get_betslip_content().no_selections_title,
                        msg='Selections added in preconditions are still present in betslip')

    def test_003_add_the_same_selection_from_preconditions_to_betslip_with_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Add the same selection from preconditions to Betslip with stake value which is higher than maximum bet limit for added selection
        EXPECTED: - The same selection is added to Beslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.05
        self.place_single_bet()
        self.site.login(username=self.username)

    def test_004_tap_login__place_betlogin_and_place_bet_buttoncoralladbrokes(self):
        """
        DESCRIPTION: Tap 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button
        DESCRIPTION: (Coral/Ladbrokes)
        EXPECTED: - New Overask review process is started
        EXPECTED: - New Bet trigger OA is displayed in TI (Bet -> BI Requests)
        EXPECTED: - New placeBet request is sent
        """
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

    def test_005_log_out_from_the_applicationfor_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Betslip is Empty
        """
        self.test_002_log_out_from_the_applicationfor_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app()

    def test_006_add_new_selection_another_than_was_used_in_preconditions_to_betslip_with_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Add new selection another than was used in preconditions to Betslip with stake value which is higher than maximum bet limit for added selection
        EXPECTED: - Selection is added to Beslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        self.__class__.bet_amount = self.max_bet + 0.05
        self.place_single_bet()
        self.site.login(username=self.username)

    def test_007_tap_login__place_betlogin_and_place_bet_buttoncoralladbrokes(self):
        """
        DESCRIPTION: Tap 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button
        DESCRIPTION: (Coral/Ladbrokes)
        EXPECTED: - New Overask review process is started
        EXPECTED: - New Bet trigger OA is displayed in TI (Bet -> BI Requests)
        EXPECTED: - New placeBet request is sent
        """
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')
