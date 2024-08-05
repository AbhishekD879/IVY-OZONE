import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C883820_C15500642_Verify_Quick_Bet_for_not_Logged_In(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C883820
    TR_ID: C15500642
    VOL_ID: C9698257
    NAME: Verify Quick Bet for not Logged In
    DESCRIPTION: This test case verifies Quick Bet for not Logged in
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: User should be logged out
    PRECONDITIONS: For Step #8 and Step #10
    PRECONDITIONS: User should not have any popup windows appear after starting session
    PRECONDITIONS: For Step #11
    PRECONDITIONS: User should have one or more popup windows appear after starting session:
    PRECONDITIONS: Terms and Conditions
    PRECONDITIONS: Verify Your Account (Netverify)
    PRECONDITIONS: Deposit Limits
    PRECONDITIONS: Quick Deposit
    PRECONDITIONS: Free Bet
    PRECONDITIONS: Casino bonuses
    """
    keep_browser_open = True
    quick_bet = None
    odds = None
    total_est_return = None
    market_name = None
    outcome_name = None
    bet_amount = 1.00
    additional_amount = 11.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login and Logout
        """
        self.__class__.username = tests.settings.betplacement_user
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.expected_market = next((market.get('market').get('name') for market in event['event']['children']
                                                   if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        else:
            self.__class__.eventID = self.ob_config.add_football_event_to_england_championship().event_id
            expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
            self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.logout()

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Open created event
        DESCRIPTION: Select one <Sport> selection
        EXPECTED: Quick Bet is opened
        EXPECTED: Added selection is displayed
        EXPECTED: Numeric keyboard is collapsed by default
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

    def test_002_verify_login_place_bet_button(self):
        """
        DESCRIPTION: Verify 'LOGIN & PLACE BET' button
        EXPECTED: 'LOGIN & PLACE BET' button is disabled by default
        """
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='Place Bet button is not disabled')

    def test_003_enter_valid_value_on_stake_field(self):
        """
        DESCRIPTION: Enter valid value on 'Stake' field
        EXPECTED: 'LOGIN & PLACE BET' button becomes enabled
        """
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                        msg='Place Bet button is not enabled')

        self.__class__.odds = self.quick_bet.content.odds
        self.__class__.total_stake = self.quick_bet.bet_summary.total_stake
        self.__class__.total_est_return = self.quick_bet.bet_summary.total_estimate_returns
        self.__class__.outcome_name = self.quick_bet.content.outcome_name
        self.__class__.market_name = self.quick_bet.content.market_name
        self.__class__.event_name = self.quick_bet.content.event_name

    def test_004_tap_on_login_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'LOGIN & PLACE BET' button
        EXPECTED: An overlay Login window is displayed
        """
        self.site.quick_bet_panel.place_bet.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(dialog, msg='Login dialog is not present on page')

    def test_005_fill_valid_username_password_and_tap_on_login_place_bet_button(self):
        """
        DESCRIPTION: Fill valid username / password and tap on 'LOGIN & PLACE BET' button
        EXPECTED: User session is started and bet is placed according to selected <Sport>, 'Odds' and 'Stake'
        """
        self.site.login(timeout_wait_for_dialog=1, username=self.username, close_free_bets_notification=False)

    def test_006_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Local Time (if available) and Event is displayed;
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Unit Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        """
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

        bet_receipt = self.site.quick_bet_panel.bet_receipt
        self.assertEqual(bet_receipt.name, self.outcome_name,
                         msg=f'Actual Outcome name: "{bet_receipt.name}" '
                             f'does not match expected: "{self.outcome_name}"')
        self.assertEqual(bet_receipt.event_market, self.market_name,
                         msg=f'Actual Market name" "{bet_receipt.event_market}" '
                             f'does not match expected: "{self.market_name}"')
        self.assertEqual(bet_receipt.event_name, self.event_name,
                         msg=f'Actual Event name: "{bet_receipt.event_name}" '
                             f'does not match expected: "{self.event_name}"')
        self.assertTrue(bet_receipt.bet_id, msg='Bet ID is not shown')
        self.assertEqual(bet_receipt.odds, self.odds,
                         msg=f'Actual Odds: "{bet_receipt.odds}" '
                             f'does not match expected: "{self.odds}"')
        self.assertEqual(bet_receipt.total_stake, self.total_stake,
                         msg=f'Actual Total Stake: "{bet_receipt.total_stake}" '
                             f'does not match expected: "{self.total_stake}"')
        self.assertAlmostEqual(float(bet_receipt.estimate_returns), float(self.total_est_return), delta=0.01,
                               msg=f'Actual Est./Pot. Returns: "{float(bet_receipt.estimate_returns)}"'
                                   f'does not match expected: "{float(self.total_est_return)}" with delta 0.01')

    def test_007_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is logged out
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

        self.__class__.user_balance = self.site.header.user_balance
        self.site.logout()

    def test_008_repeat_steps_log_in_with_user_that_has_lower_balance_than_the_amount_entered_on_stake_and_credit_card_added(self):
        """
        DESCRIPTION: Repeat steps
        DESCRIPTION: Log in with user that has lower balance than the amount entered on 'Stake' and credit card added
        EXPECTED: Quick bet appears at the bottom of the page and should display:
        EXPECTED: 'Funds needed for bet "<currency symbol>XX.XX' error message is displayed below 'QUICK BET' header
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - entered stake value
        """
        self.test_001_select_one_sport_selection()
        self.test_002_verify_login_place_bet_button()

        self.__class__.bet_amount = self.user_balance + self.additional_amount

        self.test_003_enter_valid_value_on_stake_field()
        self.test_004_tap_on_login_place_bet_button()

        self.site.login(username=self.username,
                        timeout_wait_for_dialog=1, close_free_bets_notification=False,
                        async_close_dialogs=False)

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed(expected_result=False)
        self.assertFalse(bet_receipt_displayed, msg='Bet Receipt is shown')

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        result = self.site.quick_bet_panel.wait_for_quick_bet_info_panel() if self.brand == 'bma' \
            else self.site.quick_bet_panel.wait_for_deposit_info_panel()
        self.assertTrue(result, msg='Quick Bet Info Panel is not present')

        actual_message = self.site.quick_bet_panel.info_panels_text[0] if self.brand != 'ladbrokes' \
            else self.site.quick_bet_panel.bet_amount_warning_message
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message: "{actual_message}" '
                             f'does not match expected: "{expected_message}"')

    def test_009_repeat_steps_log_in_with_an_user_that_has_an_expected_popup_window_to_appear_for_any_case_below(self):
        """
        DESCRIPTION: Repeat Steps
        DESCRIPTION: Log in with an user that has an expected popup window to appear for any case below:
        DESCRIPTION: Terms and Conditions
        DESCRIPTION: Verify Your Account (Netverify)
        DESCRIPTION: Deposit Limits
        DESCRIPTION: Quick Deposit
        DESCRIPTION: Free Bet
        DESCRIPTION: Casino bonuses
        EXPECTED: Respective popup window should appear and bet is not placed
        """
        if tests.settings.backend_env != 'prod':

            self.test_007_log_out_from_app()
            counter_value = int(self.site.header.bet_slip_counter.counter_value)
            if counter_value > 0:
                self.site.header.bet_slip_counter.click()
                self.clear_betslip()
                self.device.go_back()

            odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
            if odds_boost is None:
                raise CmsClientException('Odds Boost config is disabled in CMS')
            if not odds_boost.get('enabled'):
                raise CmsClientException('Odds Boost is disabled in CMS')

            username = self.gvc_wallet_user_client.register_new_user().username
            self.add_card_and_deposit(username=username, amount=tests.settings.min_deposit_amount)

            # Adding OddsBoost token, need to login first
            self.site.login(username=username)
            self.ob_config.grant_odds_boost_token(username=username)
            self.site.logout()

            self.test_001_select_one_sport_selection()
            self.test_002_verify_login_place_bet_button()
            self.test_003_enter_valid_value_on_stake_field()
            self.test_004_tap_on_login_place_bet_button()

            self.site.login(username=username,
                            timeout_wait_for_dialog=1,
                            ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST,
                            close_free_bets_notification=False,
                            async_close_dialogs=False)

            expected_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
            self.assertTrue(expected_dialog, msg='Odds Boost dialog is not shown')
            expected_dialog.close_dialog()

            bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed(expected_result=False)
            self.assertFalse(bet_receipt_displayed, msg='Bet Receipt is shown')
        else:
            self._logger.info('*** Skipping last step for PROD environment as Odds Boost tokens cannot be granted')
