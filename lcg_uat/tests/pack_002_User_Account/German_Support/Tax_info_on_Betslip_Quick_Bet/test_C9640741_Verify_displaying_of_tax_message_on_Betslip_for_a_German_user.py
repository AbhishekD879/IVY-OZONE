import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.lad_tst2    # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9640741_Verify_displaying_of_tax_message_on_Betslip_for_a_German_user(BaseBetSlipTest):
    """
    TR_ID: C9640741
    NAME: Verify displaying of tax message on 'Betslip' for a German user
    DESCRIPTION: This test case verifies displaying of a tax message on 'Betslip' for a German user
    PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
    PRECONDITIONS: 2. A user is logged out
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
    PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: - Please delete cookies and caches before test steps
    """
    keep_browser_open = True
    currency = '€'
    stake = None
    betslip_selection = None
    singles_section = None
    min_deposit = '5.00'

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
        DESCRIPTION: 2. A user is logged out
        DESCRIPTION: NOTE:
        DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
        DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
        DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
        DESCRIPTION: - Please delete cookies and caches before test steps
        """
        self.__class__.username = tests.settings.german_betplacement_user
        self.site.login(username=self.username, async_close_dialogs=False)
        self.__class__.user_balance = self.site.header.user_balance
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')
        self.delete_cookies()

        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self._logger.info(f'*** Found Football outcomes "{self.selection_ids}"')
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_ids = event.selection_ids
            self.__class__.team1 = event.team1

    def test_001_add_selections_to_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to 'Betslip' > Open 'Betslip'
        EXPECTED: - 'Betslip' is opened
        EXPECTED: - Added selection(s) is(are) displayed within 'Betslip'
        EXPECTED: - Tax message is NOT displayed
        """
        selection_ids = list(self.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.team1, self.singles_section,
                      msg=f'Betslip opened with not expected selections, actual: '
                      f'"{self.singles_section.keys()}", expected: "{self.team1}"')
        self.__class__.betslip_selection = self.singles_section[self.team1]
        self.assertTrue(self.betslip_selection, msg='Betslip Singles section is not displayed.')
        self.assertFalse(self.get_betslip_content().has_german_tax_message(expected_result=False),
                         msg=f'"{vec.betslip.TAX_5}" is displayed')

    def test_002_enter_stake_that_exceeds_german_users_balance_and_tap_login_place_bet_button(self):
        """
        DESCRIPTION: Enter 'Stake' that exceeds German user's balance > Tap 'Login & Place Bet'
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        EXPECTED: - Bet is not placed
        EXPECTED: - 'Betslip' stays on with an error: "Funds needed..."
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        addition_amount = 0.01
        bet_amount_exceeds = self.user_balance + addition_amount
        for stake_name, stake in self.singles_section.items():
            stake.amount_form.input.value = bet_amount_exceeds
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertEqual(bet_now_button.name, vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION,
                         msg=f'Found button name,"{bet_now_button.name}" '
                             f'is not same as "{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}"')
        bet_now_button.click()
        self.site.login(username=self.username, password=tests.settings.default_password, timeout_wait_for_dialog=2,
                        async_close_dialogs=False)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')
        actual_message = self.get_betslip_content().bet_amount_warning_message
        expected_message = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(float(self.min_deposit)).replace('£', self.currency)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message}"')

        betslip_page = self.get_betslip_content()
        self.assertTrue(betslip_page.has_german_tax_message(), msg='German Tax Message fee is not displayed')
        self.assertEqual(betslip_page.german_tax_message_text, vec.betslip.TAX_5,
                         msg=f'Mismatch in Actual "{betslip_page.german_tax_message_text}" '
                             f'and Expected "{vec.betslip.TAX_5}"')

    def test_003_re_enter_stake_that_is_covered_by_users_balance_and_tap_bet_now(self):
        """
        DESCRIPTION: Re-enter 'Stake' that is covered by user's balance > Tap 'Bet Now'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Bet Receipt' is displayed
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns' on 'Bet Receipt'
        """
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            stake.amount_form.input.clear()
            stake.amount_form.input.value = self.bet_amount
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt.has_german_tax_message(), msg='German Tax Message fee is not displayed')
        self.assertEqual(bet_receipt.german_tax_message_text, vec.betslip.TAX_5,
                         msg=f'Mismatch in Actual "{bet_receipt.german_tax_message_text}" '
                             f'and Expected "{vec.betslip.TAX_5}"')

    def test_004_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'Reuse Selection'
        EXPECTED: 'Betslip' is displayed with selection(s)
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        self.assertIn(self.team1, self.singles_section,
                      msg=f'Betslip opened with not expected selections, '
                          f'actual: "{self.singles_section.keys()}", expected: "{self.team1}"')

    def test_005_close_betslip_and_log_out(self):
        """
        DESCRIPTION: Close 'Betslip' > Log out
        EXPECTED: - User is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.close_betslip()
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is {key_value}')

    def test_006_open_betslip_and_verify_availability_of_a_tax_message(self):
        """
        DESCRIPTION: Open Betslip > Verify availability of a tax message
        EXPECTED: Message: "A fee of 5% is applicable on winnings" remains displayed below 'Stake' & 'Est. Returns' on 'Betslip'
        """
        self.site.open_betslip()
        betslip_page = self.get_betslip_content()
        self.assertTrue(betslip_page.has_german_tax_message(), msg=f'German Tax Message fee is not displayed')
        self.assertEqual(betslip_page.german_tax_message_text, vec.betslip.TAX_5,
                         msg=f'Mismatch in Actual "{betslip_page.german_tax_message_text}" '
                             f'and Expected "{vec.betslip.TAX_5}"')
