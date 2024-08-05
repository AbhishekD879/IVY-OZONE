import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


# @pytest.mark.lad_tst2   # VANO-1483, BMA-52554
# @pytest.mark.lad_hl
# @pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.bet_placement
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9690301_Verify_tax_message_not_displaying_to_a_non_german_user_on_Quick_Bet(BaseSportTest):
    """
    TR_ID: C9690301
    VOL_ID: C16768819
    NAME: Verify tax message not displaying to a non german user on 'Quick Bet'
    DESCRIPTION: This test case verifies tax message not displaying to a non german user on 'Quick Bet'
    PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 2. A non-german user is registered
    """
    keep_browser_open = True
    added_value_amount = 1.00
    min_deposit_amount = 5.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: Log in as a non german user > Log out
        EXPECTED: - Non German user is logged out
        EXPECTED: - retrieve the user balance to place a bet
        """
        category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=category_id)[0]
            market_name = normalize_name(event['event']['children'][0].get('market').get('name'))
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.event_id = event['event']['id']
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.event_id = event_params.team1, event_params.event_id
            market_name = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        self.__class__.username = tests.settings.betplacement_user
        self.__class__.german_user = tests.settings.german_betplacement_user
        self.site.login(self.username)
        self.site.wait_content_state('Homepage')
        self.__class__.user_balance = self.site.header.user_balance
        self.site.logout(timeout=0.5)

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(self.german_user)
        self.site.logout(timeout=0.5)
        self.site.wait_content_state('Homepage')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_002_add_a_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add a selection to 'Quick Bet'
        EXPECTED: - 'Quick Bet' appears with an added selection
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        self.assertTrue(self.site.quick_bet_panel.has_german_tax_message(), msg=f'"{vec.quickbet.TAX_5}" is not displayed')
        self.assertEqual(self.site.quick_bet_panel.german_tax_message_text, vec.quickbet.TAX_5,
                         msg=f'Mismatch in Actual: "{self.site.quick_bet_panel.german_tax_message_text}" and Expected: "{vec.quickbet.TAX_5}"')

    def test_003___enter_stake_that_will_exceed_non_german_user_balance__tap_log_in__bet__log_in_with_non_german_user(self):
        """
        DESCRIPTION: - Enter 'Stake' that will exceed non german user balance
        DESCRIPTION: - Tap 'Log in & Bet'
        DESCRIPTION: - Log in with non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        EXPECTED: - 'Quick Bet' stays on with an error: "Funds needed..."
        EXPECTED: - Tax message is not displayed
        """
        self.__class__.bet_amount = self.user_balance + float(self.added_value_amount)
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.quick_bet.selection.content.amount_form.input.value = self.bet_amount
        self.assertEqual(self.quick_bet.place_bet.name, vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET,
                         msg=f'Found button name, "{self.quick_bet.place_bet.name}" is not same as "{vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET}"')
        self.quick_bet.place_bet.click()
        self.site.login(self.username)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')
        actual_message = self.quick_bet.bet_amount_warning_message
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.min_deposit_amount)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.has_german_tax_message(expected_result=False), msg=f'"{vec.quickbet.TAX_5}" is displayed')

    def test_004_re_enter_stake_that_is_covered_by_users_balance__tap_place_bet(self):
        """
        DESCRIPTION: Re-enter 'Stake' that is covered by user's balance > Tap 'Place Bet'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Bet Receipt' is displayed
        EXPECTED: - Tax message is not displayed
        """
        self.quick_bet.selection.content.amount_form.input.clear()
        self.quick_bet.selection.content.amount_form.input.value = self.added_value_amount
        self.quick_bet.place_bet.click()
        self.quick_bet.wait_for_bet_receipt_displayed()
        self.assertFalse(self.site.quick_bet_panel.has_german_tax_message(expected_result=False), msg=f'"{vec.quickbet.TAX_5}" is displayed')

    def test_005_close_quick_bet__log_out(self):
        """
        DESCRIPTION: Close 'Quick Bet' > Log out
        EXPECTED: - User is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.logout(timeout=0.5)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_006___add_a_selection_to_quick_bet__verify_availability_of_tax_message_on_quick_deposit(self):
        """
        DESCRIPTION: - Add a selection to 'Quick Bet'
        DESCRIPTION: - Verify availability of tax message on 'Quick Deposit'
        EXPECTED: Tax message is not displayed
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market, selection_name=self.team1)
        self.assertFalse(self.site.quick_bet_panel.has_german_tax_message(expected_result=False),
                         msg=f'"{vec.quickbet.TAX_5}" is displayed')
