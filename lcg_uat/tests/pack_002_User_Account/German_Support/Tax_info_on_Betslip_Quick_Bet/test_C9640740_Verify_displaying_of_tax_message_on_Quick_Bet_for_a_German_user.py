import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.lad_tst2   # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_hl
# @pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9640740_Verify_displaying_of_tax_message_on_Quick_Bet_for_a_German_user(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C9640740
    VOL_ID: C16706467
    NAME: Verify displaying of tax message on 'Quick Bet' for a German user
    DESCRIPTION: This test case verifies displaying of a tax message on 'Quick Bet' for a German user
    """
    keep_browser_open = True
    quick_bet = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. A German user is registered (with "signupCountryCode": "DE" - select Germany as a country during registration)
        PRECONDITIONS: 2. A German user is logged out
        PRECONDITIONS: NOTE:
        PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
        PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
        PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
        """
        self.__class__.username = tests.settings.german_betplacement_user
        self.site.login(username=self.username)
        self.__class__.user_balance = self.site.header.user_balance
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')
        self.delete_cookies()
        if tests.settings.backend_env == 'prod':
            self.__class__.event = self.get_active_events_for_category(
                category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = self.event['event']['id']
            market_name = next((market['market']['name'] for market in self.event['event']['children']
                                if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        else:
            self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = self.event.event_id
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|',
                                                                                                                    '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_a_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add a selection to 'Quick Bet'
        EXPECTED: - 'Quick Bet' appears with an added selection
        EXPECTED: - Tax message is NOT displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        actual_selection = self.site.quick_bet_panel.selection.content.outcome_name
        self.assertEqual(actual_selection, 'Draw',
                         msg=f'Actual selection name: "{actual_selection}" is not same as Expected: "Draw"')
        self.assertFalse(self.site.quick_bet_panel.has_german_tax_message(expected_result=False),
                         msg=f'"{vec.quickbet.TAX_5}" is displayed')

    def test_002_enter_stake_that_exceeds_german_users_balance_and_tap_login_place_bet_button(self):
        """
        DESCRIPTION: Enter 'Stake' that exceeds German user's balance > Tap 'Login & Place Bet'
        EXPECTED: - German user is logged in
        EXPECTED: - Bet is not placed
        EXPECTED: -  In Application > Local Storage > "OX.countryCode"="DE"
        EXPECTED: - 'Quick Bet' stays on with an error: "Please deposit a min of €{} to continue placing your bet"
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        addition_amount = 5.00
        bet_amount_exceeds = self.user_balance + addition_amount
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.quick_bet.selection.content.amount_form.input.value = bet_amount_exceeds
        quick_place_bet_name = self.quick_bet.place_bet.name
        self.assertEqual(quick_place_bet_name, vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET,
                         msg=f'Found button name, "{quick_place_bet_name}", '
                             f'is not same as "{vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET}"')
        self.quick_bet.place_bet.click()
        self.site.login(username=self.username, timeout_wait_for_dialog=2)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

        actual_message = self.quick_bet.bet_amount_warning_message
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(addition_amount)
        expected_message1 = expected_message.replace('£', '€')
        self.assertEqual(actual_message, expected_message1,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message1}"')
        self.assertTrue(self.quick_bet.has_german_tax_message(),
                        msg='German Tax Message fee is not displayed')
        self.assertEqual(self.quick_bet.german_tax_message_text, vec.quickbet.TAX_5,
                         msg=f'Mismatch in Actual: "{self.quick_bet.german_tax_message_text}" '
                             f'and Expected: "{vec.quickbet.TAX_5}"')

    def test_003_re_enter_stake_that_is_covered_by_users_balance_and_tap_place_bet(self):
        """
        DESCRIPTION: Re-enter 'Stake' that is covered by user's balance > Tap 'Place Bet'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Bet Receipt' is displayed
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns' on 'Bet Receipt'
        """
        self.quick_bet.selection.content.amount_form.input.clear()
        self.quick_bet.selection.content.amount_form.input.value = self.bet_amount
        self.quick_bet.place_bet.click()
        bet_receipt_displayed = self.quick_bet.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.assertTrue(self.quick_bet.has_german_tax_message(), msg='German Tax Message fee is not displayed')
        self.assertEqual(self.quick_bet.german_tax_message_text, vec.quickbet.TAX_5,
                         msg=f'Mismatch in Actual: "{self.quick_bet.german_tax_message_text}" '
                             f'and Expected: "{vec.quickbet.TAX_5}"')

    def test_004_close_quick_bet_and_log_out(self):
        """
        DESCRIPTION: Close 'Quick Bet' > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.quick_bet.header.close_button.click()
        self.site.logout(timeout=0.5)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_005_add_a_selection_to_quick_bet_and_verify_availability_of_tax_message_on_quick_deposit(self):
        """
        DESCRIPTION: Add a selection to 'Quick Bet'
        DESCRIPTION: Verify availability of tax message on 'Quick Deposit'
        EXPECTED: Message: "A fee of 5% is applicable on winnings" remains displayed below 'Stake' & 'Est. Returns' on 'Bet Receipt'
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        quick_bet = self.site.quick_bet_panel
        self.assertTrue(quick_bet.has_german_tax_message(),
                        msg='German Tax Message fee is not displayed')
        self.assertEqual(quick_bet.german_tax_message_text, vec.quickbet.TAX_5,
                         msg=f'Mismatch in Actual: "{quick_bet.german_tax_message_text}" '
                             f'and Expected: "{vec.quickbet.TAX_5}"')
