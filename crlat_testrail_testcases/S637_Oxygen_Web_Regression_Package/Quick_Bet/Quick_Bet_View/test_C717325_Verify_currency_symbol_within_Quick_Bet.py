import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C717325_Verify_currency_symbol_within_Quick_Bet(Common):
    """
    TR_ID: C717325
    NAME: Verify currency symbol within Quick Bet
    DESCRIPTION: This test case verifies currency symbol within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. Make sure you have users with next currency:
    PRECONDITIONS: * 'GBP': symbol = **£**;
    PRECONDITIONS: * 'USD': symbol = **$**;
    PRECONDITIONS: * 'EUR': symbol = **€**;
    PRECONDITIONS: 4. Application is loaded
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_has_gbp_currency(self):
        """
        DESCRIPTION: Log in with user that has 'GBP' currency
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_one_selection_to_quickbet(self):
        """
        DESCRIPTION: Add one selection to QuickBet
        EXPECTED: Quick Bet is displayed at the bottom of page
        """
        pass

    def test_003_verify_currency_set_within_quick_bet_section(self):
        """
        DESCRIPTION: Verify currency set within Quick Bet section
        EXPECTED: 'GBP' currency is displayed next to:
        EXPECTED: * 'Quick Stake' buttons
        EXPECTED: * 'Total Stake' and 'Estimated Returns' **CORAL** / 'Potential Returns' **Ladbrokes** labels
        """
        pass

    def test_004_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: * No currency symbol within 'Stake' field
        EXPECTED: * "Stake" text is displayed within 'Stake' field
        """
        pass

    def test_005_close_quick_bet_section_via_x_button(self):
        """
        DESCRIPTION: Close Quick Bet section via 'X' button
        EXPECTED: Quick Bet section is not displayed
        EXPECTED: After release of BMA-54870 Expected result will be:
        EXPECTED: * Quick Bet is closed automatically
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is the same as was added by Quick bet
        EXPECTED: * 'Stake' field contains added value from Quick bet
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_007_log_in_with_user_that_has_usd_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in with user that has 'USD' currency and repeat steps #2-6
        EXPECTED: 
        """
        pass

    def test_008_log_in_with_user_that_has_eur_currency_and_repeat_steps_2_6(self):
        """
        DESCRIPTION: Log in with user that has 'EUR' currency and repeat steps #2-6
        EXPECTED: 
        """
        pass
