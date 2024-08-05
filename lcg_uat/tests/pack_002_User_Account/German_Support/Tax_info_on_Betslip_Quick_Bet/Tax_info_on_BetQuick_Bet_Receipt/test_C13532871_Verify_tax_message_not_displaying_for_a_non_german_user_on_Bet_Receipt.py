import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C13532871_Verify_tax_message_not_displaying_for_a_non_german_user_on_Bet_Receipt(BaseBetSlipTest):
    """
    TR_ID: C13532871
    NAME: Verify tax message not displaying for a non-german user on Bet Receipt
    DESCRIPTION: This test case verifies tax message not displaying to a non-german user on Bet Receipt
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Log in with the non-German user
        PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
        PRECONDITIONS: 4. Make bet placement for single selection
        PRECONDITIONS: 5. Make sure Bet is placed successfully
        PRECONDITIONS: NOTE:
        PRECONDITIONS: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user). Verify in Application > Local Storage > OX.countryCode. For german user 'DE' value is set.
        """
        self.site.login()
        self.site.wait_content_state('Homepage')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB".'
                             f'Actual value of "OX.countryCode" is "{key_value}"')
        self.__class__.balance = self.site.header.user_balance
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            selection_id = list(selection_ids.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = list(event.selection_ids.values())[0]

        self.open_betslip_with_selections(selection_ids=selection_id)
        self.__class__.bet_amount = 1
        self.place_single_bet()

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Betslip is replaced with a Bet Receipt view
        """
        self.check_bet_receipt_is_displayed(timeout=15)
        updated_balance = self.site.header.user_balance
        self.assertEqual(self.balance - 1, updated_balance,
                         msg=f'Balance before betplacement: "{self.balance}" was not decreased to expected balance '
                             f'after betplacement: "{updated_balance}"')

    def test_002_verify_availability_of_a_tax_message_on_bet_receipt(self):
        """
        DESCRIPTION: Verify availability of a tax message on Bet Receipt
        EXPECTED: Message: "A fee of 5% is applicable on winnings" is NOT displayed below 'Total Stake' & 'Potential Returns' fields on Bet Receipt
        """
        self.assertFalse(self.site.bet_receipt.footer.has_german_tax_message(),
                         msg='German Tax Message fee is displayed')
