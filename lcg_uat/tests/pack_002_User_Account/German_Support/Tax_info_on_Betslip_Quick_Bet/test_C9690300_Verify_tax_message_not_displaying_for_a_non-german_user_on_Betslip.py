import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.lad_tst2   # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# # @pytest.mark.lad_prod
# # @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9690300_Verify_tax_message_not_displaying_for_a_non_german_user_on_Betslip(BaseBetSlipTest):
    """
    TR_ID: C9690300
    NAME: Verify tax message not displaying for a non-german user on 'Betslip'
    DESCRIPTION: This test case verifies tax message not displaying to a non german user on 'Betslip'
    """
    keep_browser_open = True
    event = None

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
        PRECONDITIONS: 2. A non-german user is registered
        PRECONDITIONS: 3. A German user is logged in
        PRECONDITIONS: NOTE:
        PRECONDITIONS: - "signupCountryCode" is received in WS "openapi" response from IMS
        PRECONDITIONS: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
        PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(tests.settings.german_betplacement_user, tests.settings.default_password)
        self.site.logout(timeout=10)
        self.site.wait_content_state('Homepage')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_002_add_selections_to_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to 'Betslip' > Open Betslip
        EXPECTED: - Added selections are available within 'Betslip'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        selection_ids = list(self.event.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section, msg='Betslip Singles section is not displayed.')
        self.__class__.betslip = self.get_betslip_content()
        self.assertTrue(self.betslip.has_german_tax_message(), msg=f'"{vec.betslip.TAX_5}" is not displayed')
        self.assertEquals(self.betslip.german_tax_message_text, vec.betslip.TAX_5,
                          msg=f'How can we help message is not the same as expected. '
                          f'Actual: {self.betslip.german_tax_message_text}.'
                          f'Expected: "{vec.betslip.TAX_5}"')
        self.site.close_betslip()

    def test_003_log_in_as_non_german_user(self):
        """
        DESCRIPTION: Log in as non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.login()
        self.site.wait_content_state('Homepage')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_004___open_betslip__verify_availability_of_a_tax_message(self):
        """
        DESCRIPTION: - Open Betslip
        DESCRIPTION: - Verify availability of a tax message
        EXPECTED: Message: "A fee of 5% is applicable on winnings" is NOT displayed below 'Stake' & 'Est. Returns' on 'Betslip'
        """
        self.site.open_betslip()
        self.assertFalse(self.betslip.has_german_tax_message(expected_result=False),
                         msg=f'"{vec.betslip.TAX_5}" is displayed on betslip')

    def test_005_enter_valid_stake__tap_bet_now(self):
        """
        DESCRIPTION: Enter valid 'Stake' > Tap 'Bet Now'
        EXPECTED: - Bet Receipt is displayed
        EXPECTED: - No tax message is displayed
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed(timeout=15)
        self.assertFalse(self.betslip.has_german_tax_message(expected_result=False),
                         msg=f'"{vec.betslip.TAX_5}" is displayed on betslip')

    def test_006_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'Reuse Selection'
        EXPECTED: Betslip is displayed with selection(s)
        """
        self.site.bet_receipt.footer.reuse_selection_button.click()
        self.assertTrue(self.singles_section, msg='Betslip Singles section is not displayed.')

    def test_007_close_betslip__log_out(self):
        """
        DESCRIPTION: Close 'Betslip' > Log out
        EXPECTED: - User is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.close_betslip()
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_008_open_betslip__verify_availability_of_a_tax_message(self):
        """
        DESCRIPTION: Open Betslip > Verify availability of a tax message
        EXPECTED: No tax message is displayed
        """
        self.site.open_betslip()
        self.assertFalse(self.betslip.has_german_tax_message(expected_result=False),
                         msg=f'"{vec.betslip.TAX_5}" is displayed on betslip')
