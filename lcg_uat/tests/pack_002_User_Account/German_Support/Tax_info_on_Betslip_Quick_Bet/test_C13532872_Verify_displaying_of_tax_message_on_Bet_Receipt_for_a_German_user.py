import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import tests
import voltron.environments.constants as vec


# @pytest.mark.lad_tst2    # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# # @pytest.mark.lad_hl
# # @pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C13532872_Verify_displaying_of_tax_message_on_Bet_Receipt_for_a_German_user(BaseBetSlipTest):
    """
    TR_ID: C13532872
    NAME: Verify displaying of tax message on Bet Receipt for a German user
    DESCRIPTION: This test case verifies displaying of a tax message on Bet Receipt for a German user
    """
    keep_browser_open = True
    stake = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Log in with German user (testtest3/qwerty123)
        PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
        PRECONDITIONS: 4. Make bet placement for single selection
        PRECONDITIONS: 5. Make sure Bet is placed successfully
        PRECONDITIONS: **NOTE:**
        PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user). Verify in Application > Local Storage > OX.countryCode. For german user 'DE' value is set.
        """
        self.site.login(username=tests.settings.german_betplacement_user, password=tests.settings.default_password)
        self.__class__.user_balance = self.site.header.user_balance
        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_ids = list(event.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection_ids)
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            stake.amount_form.input.clear()
            stake.amount_form.input.value = self.bet_amount
        stake.amount_form.input.clear()
        stake.amount_form.input.value = self.bet_amount
        self.get_betslip_content().bet_now_button.click()

        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount)

    def test_002_verify_availability_of_a_tax_message_on_bet_receipt(self):
        """
        DESCRIPTION: Verify availability of a tax message on Bet Receipt
        EXPECTED: Message: "A fee of 5% is applicable on winnings" is displayed below 'Total Stake' & 'Potential Returns' fields on Bet Receipt
        """
        bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt.has_german_tax_message(), msg='German Tax Message fee is not displayed')
        self.assertEqual(bet_receipt.german_tax_message_text, vec.betslip.TAX_5,
                         msg=f'Mismatch in Actual:"{bet_receipt.german_tax_message_text}" and Expected:"{vec.betslip.TAX_5}"')
