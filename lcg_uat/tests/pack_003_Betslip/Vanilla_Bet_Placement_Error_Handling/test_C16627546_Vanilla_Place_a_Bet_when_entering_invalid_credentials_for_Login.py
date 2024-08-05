import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebet on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C16627546_Vanilla_Place_a_Bet_when_entering_invalid_credentials_for_Login(BaseBetSlipTest):
    """
    TR_ID: C16627546
    NAME: [Vanilla] Place a Bet when entering invalid credentials for Login
    DESCRIPTION: This test case verifies Bet Placement when entering invalid credentials for Login.
    PRECONDITIONS: Make sure that user is logged out.
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: event landing page
    PRECONDITIONS: event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: 'Next 4' module
    PRECONDITIONS: event details page
    PRECONDITIONS: Extra Info:
    PRECONDITIONS: Bet placement process will be automatically started JUST after session token will be set for user.
    PRECONDITIONS: Behavior of pop-ups is not changed by this functionality e.g. if 'Terms and Conditions' pop-up appears - user will need to accept new terms to be able to place bets.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        if tests.settings.backend_env != 'prod':
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        else:
            self.__class__.selection_ids = self.get_active_event_selections_for_category()

        self.__class__.username = tests.settings.betplacement_user

        # to avoid situation when dialogs affect test steps
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.logout()

    def test_001_open_application(self):
        """
        DESCRIPTION: Open application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_add_any_market_for_betting(self):
        """
        DESCRIPTION: Add any market for betting
        EXPECTED: Quick Bet is opened:
        EXPECTED: * 'ADD TO BETSLIP' is active
        EXPECTED: * 'LOGIN & PLACE BET' button is not active
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_003_enter_at_least_one_stake_for_any_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any selection
        EXPECTED: Stake is entered and displayed correctly
        EXPECTED: * 'ADD TO BETSLIP' is active
        EXPECTED: * 'LOGIN & PLACE BET' button is active
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)

    def test_004_tap_on_login__place_bet_button(self):
        """
        DESCRIPTION: Tap on 'LOGIN & PLACE BET' button
        EXPECTED: * Logged out user is not able to place a bet
        EXPECTED: * 'Log In' pop-up opens
        EXPECTED: * Username and Password fields are available
        """
        self.get_betslip_content().bet_now_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='Login dialog is not present on page')
        self.dialog.username = self.username  # verifies that username field is present
        self.dialog.password = 'incorrect'  # verifies that password field is present

    def test_005_enter_invalid_credentials_of_users_account___tap_on_log_in_button(self):
        """
        DESCRIPTION: Enter *invalid* credentials of user's account -> Tap on 'LOG IN' button
        EXPECTED: There is error message: 'The credentials entered are incorrect'
        """
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(), msg=f'Error message is not displayed')
        self.assertTrue(self.get_betslip_content().is_displayed(), msg='Betslip is closed')

    def test_006_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_no_pop_ups_are_expected_after_login___tap_log_in(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and *NO* pop-ups are expected after login -> Tap 'LOG IN'
        EXPECTED: * User is logged in
        EXPECTED: * User can't do any modification for bet that is ongoing
        EXPECTED: * Bets are placed successfully (NOTE: if at least one pop-up is expected after login, Bet is NOT placed automatically)
        EXPECTED: * Bet Receipt page appears after successful bet placement
        """
        self.dialog.username = self.username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=15)
        self.assertTrue(dialog_closed, msg='User is not logged in as Login Dialog was not closed')
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=3)
        if dialog:
            dialog.close_dialog()
            self.assertFalse(self.site.is_bet_receipt_displayed(expected_result=False), msg='Bet Receipt is displayed')
        else:
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.close_button.click()

    def test_007_repeat_steps_1__4(self):
        """
        DESCRIPTION: Repeat steps 1- 4
        """
        self.site.logout()

        self.__class__.expected_betslip_counter_value = 0

        self.test_001_open_application()
        self.test_002_add_any_market_for_betting()
        self.test_003_enter_at_least_one_stake_for_any_selection()
        self.test_004_tap_on_login__place_bet_button()

    def test_008_enter_valid_credentials_of_users_account_for_which_balance_is_positive_and_at_least_one_pop_up_is_expected_after_login___tap_log_in__place_bet_button(self):
        """
        DESCRIPTION: Enter valid credentials of user's account for which balance is positive and at least one pop-up is expected after login -> Tap 'Log In & Place Bet' button
        EXPECTED: * User is logged in and expected pop-ups appear
        EXPECTED: * Betslip is NOT closed
        EXPECTED: * Bet is NOT placed automatically
        EXPECTED: * After user will deal with pop-ups then *'Bet Now' button* will be enabled within Betslip
        """
        self.ob_config.grant_freebet(username=self.username)

        self.dialog.username = self.username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=15)
        self.assertTrue(dialog_closed, msg='User is not logged in as Login Dialog was not closed')
        self.site.close_all_dialogs(async_close=False)
        self.assertTrue(self.site.wait_logged_in(timeout=5), msg='User is not logged in')
        self.assertTrue(self.get_betslip_content().is_displayed(), msg='Betslip is closed')
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(), msg='Bet now button is not enabled')

    def test_009_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
