import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.overask
@vtest
class Test_C58694728_Verify_Betslip_is_cleared_after_logged_out_during_Overask_and_trader_accepts_bet(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C58694728
    NAME: Verify Betslip is cleared after logged out during Overask and trader accepts bet
    DESCRIPTION: This test case verifies that Betslip is cleared after tapping logging out during OA and accepted bet is shown in My Bets and balance is updated appropriately
    PRECONDITIONS: Overask is enabled for User1 and for event which will be added to Betslip (see doc: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    PRECONDITIONS: Login with User1 (without 'Remember Me' option) and add selection available for Overask to Betslip
    PRECONDITIONS: Add Stake bigger than MaxAllowed
    PRECONDITIONS: Check parameters in Local Storage:
    PRECONDITIONS: OX.BetSelections
    PRECONDITIONS: OX.overaskPlaceBetsData
    PRECONDITIONS: OX.overaskIsInProgress
    PRECONDITIONS: OX.overaskUsername
    PRECONDITIONS: ![](index.php?/attachments/get/106948247)
    """
    keep_browser_open = True
    max_bet = 0.05

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.eventID = event_params.event_id
        local_start_time = self.convert_time_to_local(date_time_str=event_params.event_date_time)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2} {local_start_time}'
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.__class__.user_balance_before = self.site.header.user_balance

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - OA bet trigger is sent to TI (Bet>BI Request)
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

    def test_002_trigger_log_out_from_appon_desktop_tap_logout_button_in_account_menuon_web_mobile_refresh_page_or_close_and_reopen_tab_and_then_taplogout_button_in_the_account_menuon_wrappers_kill_and_reopen_the_app(
            self):
        """
        DESCRIPTION: Trigger log out from app:
        DESCRIPTION: **On Desktop:** Tap 'Logout' button in account menu
        DESCRIPTION: **On Web mobile:** Refresh page or close and reopen tab and then Tap'Logout' button in the account menu
        DESCRIPTION: **On wrappers:** Kill and reopen the app
        EXPECTED: - User is logged out
        EXPECTED: - Homepage is shown (for mobile web and wrappers)
        """
        if self.device_type == 'mobile':
            self.device.refresh_page()
            self.site.wait_splash_to_hide(timeout=10)
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

    def test_003_in_ti_accept_bet_betbi_request(self):
        """
        DESCRIPTION: In TI ACCEPT bet (Bet>BI Request)
        EXPECTED:
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

    def test_004_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: Selection added in preconditions is NOT shown in Betslip
        """
        self.site.open_betslip()
        self.assertTrue(self.get_betslip_content().no_selections_title,
                        msg='Selections added in preconditions are still present in betslip')

    def test_005_check_local_storage(self):
        """
        DESCRIPTION: Check Local Storage:
        EXPECTED: - OX.overaskPlaceBetsData, OX.overaskIsInProgress, OX.overaskUsername are cleared
        EXPECTED: - OX.BetSelections is empty
        """
        key_value1 = self.get_local_storage_cookie_value_as_dict('OX.overaskPlaceBetsData')
        self.assertTrue(key_value1 is None, msg=f'Value of cookie "OX.overaskPlaceBetsData" is blank')
        key_value2 = self.get_local_storage_cookie_value_as_dict('OX.overaskIsInProcess')
        self.assertTrue(key_value2 is None, msg=f'Value of cookie "OX.overaskIsInProcess" is not True')
        key_value3 = self.get_local_storage_cookie_value_as_dict('OX.overaskUsername')
        self.assertTrue(key_value3 is None, msg=f'Value of cookie "OX.overaskUsername" is not cleared')
        key_value4 = self.get_local_storage_cookie_value_as_dict('OX.betSelections')
        self.assertTrue(len(key_value4) == 0, msg=f'cookie "OX.betSelections" is NOT blank')

    def test_006_tap_login_buttonlogin_with_user1_from_preconditions(self):
        """
        DESCRIPTION: Tap 'Login' button
        DESCRIPTION: Login with user1 from preconditions
        EXPECTED: - User is logged in
        EXPECTED: - Selection added in preconditions is NOT shown in Betslip
        EXPECTED: - User balance is updated according to the Stake from preconditions
        """
        self.site.close_betslip()
        self.site.login(username=self.username)
        self.site.open_betslip()
        self.assertTrue(self.get_betslip_content().no_selections_title,
                        msg='Selections added in preconditions are still present in betslip')
        user_balance_after = self.site.header.user_balance
        self.assertGreater(self.user_balance_before, user_balance_after, msg='Balance not updated successfully')

    def test_007_go_to_my_bets(self):
        """
        DESCRIPTION: Go to My Bets
        EXPECTED: Bet which was accepted by trader is shown in My Bets
        """
        self.site.close_betslip()
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        self.assertTrue(bet, msg=f'Bet for the event "{self.event_name}" is not shown in My Bets')
