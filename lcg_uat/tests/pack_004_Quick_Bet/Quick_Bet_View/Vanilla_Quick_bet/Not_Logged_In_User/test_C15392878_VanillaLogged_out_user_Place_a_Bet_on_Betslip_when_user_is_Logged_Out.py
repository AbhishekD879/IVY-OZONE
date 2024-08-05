import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot suspend event in prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C15392878_VanillaLogged_out_user_Place_a_Bet_on_Betslip_when_user_is_Logged_Out(BaseBetSlipTest):
    """
    TR_ID: C15392878
    NAME: [Vanilla][Logged out user] Place a Bet on Betslip when user is Logged Out
    DESCRIPTION: This test case verifies bet placement when the user is Logged Out
    PRECONDITIONS: Make sure that user is logged out.
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next races' module
    PRECONDITIONS: - event details page
    PRECONDITIONS: **Extra Info:**
    PRECONDITIONS: *   Bet placement process will be automatically started JUST after session token will be set for the user.
    PRECONDITIONS: *   Behavior of pop-ups is not changed by this functionality e.g. if 'Terms and Conditions' pop-up appears - user will need to accept new terms to be able to place bets.
    """
    keep_browser_open = True
    username = tests.settings.betplacement_user

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        selection_id = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.team1 = list(selection_id.keys())[0]
        self.__class__.selection_id1 = list(selection_id.values())[0]
        selection_ids2 = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.selection_id2 = list(selection_ids2.values())[0]

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("Home")

    def test_002_add_selections_to_the_betslip(self, multiples=False):
        """
        DESCRIPTION: Add selections to the Betslip
        EXPECTED: Betslip counter is increased
        """
        self.__class__.expected_betslip_counter_value = 0
        if multiples:
            self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id2])
        else:
            self.open_betslip_with_selections(selection_ids=self.selection_id1)

    def test_003_go_to_the_betslip_singles_section(self, multiples=False):
        """
        DESCRIPTION: Go to the Betslip->'Singles' section
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added single selections are present
        EXPECTED: 3. 'Login & Place Bet' button is disabled
        """
        if multiples:
            section = self.get_betslip_sections(multiples=True)
            singles_section, multiple_section = section.Singles, section.Multiples
            self.assertTrue(multiple_section, msg='*** No Multiple stakes found')
        else:
            singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertEqual(self.stake_name, self.team1,
                         msg=f'Selection "{self.team1}" should be present in betslip, got "{self.stake_name}"')
        betslip = self.get_betslip_content()
        self.assertEqual(betslip.bet_now_button.name,
                         vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Bet button caption should be "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        self.assertFalse(betslip.bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not enabled')

    def test_004_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: 1. Stake is entered and displayed correctly
        EXPECTED: 2. 'Login & Place Bet' button becomes enabled
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(timeout=5),
                        msg='Bet now button is not enabled')

    def test_005_tap_login__place_bet_button(self):
        """
        DESCRIPTION: Tap 'Login & Place Bet' button
        EXPECTED: 1.  Logged out user is not able to place a bet
        EXPECTED: 2.  'Log In' pop-up opens
        EXPECTED: 3.  Username and Password fields are available
        EXPECTED: 4.  "Log in" button is disabled by default
        """
        self.get_betslip_content().bet_now_button.click()
        self.__class__.login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.login_dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not shown')

    def test_006_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login___tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **at least one** pop-up is expected after login -> Tap 'Log in' button
        EXPECTED: 1.  User is logged in and expected pop-ups appear
        EXPECTED: 2.  Betslip is NOT refreshed
        EXPECTED: 3.  Bet is NOT placed automatically
        EXPECTED: 4.  After user will deal with pop-ups then** 'Place Bet' button** will be enabled within Betslip
        """
        self.login_dialog.username = self.username
        self.login_dialog.password = tests.settings.default_password
        self.login_dialog.click_login()
        dialog_closed = self.login_dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')
        freebet_dialog_displayed = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION)
        if freebet_dialog_displayed:
            freebet_dialog_displayed.close_dialog()
        dialog_displayed = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.assertTrue(dialog_displayed, msg='Login dialog is not present on page')
        self.site.close_all_dialogs(timeout=5, async_close=False)
        betslip = self.get_betslip_content()
        self.assertTrue(betslip.betslip_sections_list, msg='*** No bets found in BetSlip')
        self.assertTrue(betslip.bet_now_button.is_enabled(), msg='Bet Now button is not enabled')

    def test_007_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        self.device.refresh_page()

    def test_008_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User is logged out successfully
        """
        self.site.logout()

    def test_009_repeat_steps_1_5(self, multiples=False):
        """
        DESCRIPTION: Repeat steps #1-5
        """
        self.test_001_load_oxygen_application()
        self.test_002_add_selections_to_the_betslip(multiples=multiples)
        self.test_003_go_to_the_betslip_singles_section(multiples=multiples)
        self.test_004_enter_at_least_one_stake_for_any_selection()
        self.test_005_tap_login__place_bet_button()

    def test_010_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_no_pop_ups_are_expected_after_login___tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO **pop-ups are expected after login -> Tap 'Log in' button
        EXPECTED: 1.  User is logged in
        EXPECTED: 2.  Betslip is NOT refreshed
        EXPECTED: 3.  Bets are placed successfully
        EXPECTED: 4.  User is redirected to Bet Receipt page
        """
        self.login_dialog.username = tests.settings.user_positive_balance_without_card
        self.login_dialog.password = tests.settings.default_password
        self.login_dialog.click_login()
        dialog_closed = self.login_dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')
        self.check_bet_receipt_is_displayed()

    def test_011_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User is logged out successfully
        """
        self.site.close_betreceipt()
        self.device.refresh_page()
        self.test_008_log_out_from_the_application()

    def test_012_repeat_steps_1_5(self, multiples=False):
        """
        DESCRIPTION: Repeat steps #1-5
        """
        self.test_001_load_oxygen_application()
        self.test_002_add_selections_to_the_betslip(multiples=multiples)
        self.test_003_go_to_the_betslip_singles_section(multiples=multiples)
        self.test_004_enter_at_least_one_stake_for_any_selection()
        self.test_005_tap_login__place_bet_button()

    def test_013_enter_valid_credentials_of_users_account_for_which_balance_is_positive_andnopop_ups_are_expected_after_login__tap_log_in_button_and_right_after_that_trigger_error_occurance_eg_suspension_price_change(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and **NO **pop-ups are expected after login ->Tap 'Log in' button and right after that trigger error occurance (e.g. suspension, price change)
        EXPECTED: 1.  Bet placement process starts automatically after login, hovewer it is interrupted by corresponding message about error
        EXPECTED: 2.  Betslip is NOT refreshed
        EXPECTED: 3.  Bet is not placed
        EXPECTED: 4.  User needs to make changes in the Betslip to be able to place a bet
        EXPECTED: 5.  After user will deal with error then** 'Place Bet' button** will be enabled within Betslip
        """
        self.login_dialog.username = tests.settings.user_positive_balance_without_card
        self.login_dialog.password = tests.settings.default_password
        self.login_dialog.click_login(spinner_wait=False)
        self.login_dialog.wait_dialog_closed()
        self.ob_config.change_selection_state(selection_id=self.selection_id1, displayed=True, active=False)
        self.site.close_all_dialogs(async_close=False)

        page_title = self.get_betslip_content().betslip_title.upper()
        expected_bet_slip_page_title = self.expected_bet_slip_page_title.title().upper()
        self.assertEqual(page_title, expected_bet_slip_page_title,
                         msg=f'Page title "{page_title}" doesn\'t match expected text "{expected_bet_slip_page_title}"')
        betslip_sections = self.get_betslip_content().betslip_sections_list
        self.assertTrue(betslip_sections, msg='*** No bets found in BetSlip')
        btn_enabled = self.get_betslip_content().bet_now_button.is_enabled(expected_result=False)
        self.assertFalse(btn_enabled, msg='Bet Now button is not disabled')

        stake = self.get_betslip_sections().Singles.values()[0]
        self.assertTrue(stake.is_suspended(), msg='Stake is not suspended')
        self.ob_config.change_selection_state(selection_id=self.selection_id1, displayed=True, active=True)
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        btn_enabled = self.get_betslip_content().bet_now_button.is_enabled(timeout=20)
        self.assertTrue(btn_enabled, msg='Bet Now button is not enabled')

    def test_014_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        self.test_007_tap_place_bet_button()

    def test_015_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: User is logged out successfully
        """
        self.test_008_log_out_from_the_application()

    def test_016_add_several_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        self.test_001_load_oxygen_application()
        self.test_002_add_selections_to_the_betslip(multiples=True)

    def test_017_go_to_the_betslip___multiples_section(self):
        """
        DESCRIPTION: Go to the Betslip -> 'Multiples' section
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added multiple selections are present
        """
        self.test_003_go_to_the_betslip_singles_section(multiples=True)

    def test_018_repeat_steps_4_15(self):
        """
        DESCRIPTION: Repeat steps #4-15
        """
        self.test_004_enter_at_least_one_stake_for_any_selection()
        self.test_005_tap_login__place_bet_button()
        self.test_006_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login___tap_log_in_button()
        self.test_007_tap_place_bet_button()
        self.test_008_log_out_from_the_application()
        self.test_009_repeat_steps_1_5(multiples=True)
        self.test_010_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_no_pop_ups_are_expected_after_login___tap_log_in_button()
        self.test_011_log_out_from_the_application()
        self.test_012_repeat_steps_1_5()
        self.test_013_enter_valid_credentials_of_users_account_for_which_balance_is_positive_andnopop_ups_are_expected_after_login__tap_log_in_button_and_right_after_that_trigger_error_occurance_eg_suspension_price_change()
        self.test_014_tap_place_bet_button()
        self.test_015_log_out_from_the_application()
