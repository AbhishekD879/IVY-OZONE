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
class Test_C852693_Verify_currency_symbol_within_Quick_Deposit_section(Common):
    """
    TR_ID: C852693
    NAME: Verify currency symbol within Quick Deposit section
    DESCRIPTION: This test case verifies currency symbol within Quick Deposit section
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. Make sure you have users with next currency:
    PRECONDITIONS: CORAL
    PRECONDITIONS: * 'GBP': symbol = **£**;
    PRECONDITIONS: * 'USD': symbol = **$**;
    PRECONDITIONS: * 'EUR': symbol = **€**;
    PRECONDITIONS: * 'SEK': symbol = **Kr**'
    PRECONDITIONS: LADBROKES:
    PRECONDITIONS: *   GBP currency
    PRECONDITIONS: *   AUD currency
    PRECONDITIONS: *   EUR currency
    PRECONDITIONS: *   NOK currency
    PRECONDITIONS: *   NZD currency
    PRECONDITIONS: *   CHF currency
    PRECONDITIONS: *   USD currency
    PRECONDITIONS: 4. Users have the cards added to its account
    PRECONDITIONS: 5. Application is loaded
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_has_gbp_currency(self):
        """
        DESCRIPTION: Log in with user that has 'GBP' currency
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_one_selection_to_betslip(self):
        """
        DESCRIPTION: Add one selection to Betslip
        EXPECTED: Quick Bet is displayed at the bottom of page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: 'GBP' currency is displayed within:
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed over of Quick Bet
        """
        pass

    def test_005_verify_currency_set_within_quick_deposit_section(self):
        """
        DESCRIPTION: Verify currency set within Quick Deposit section
        EXPECTED: 'GBP' currency is displayed within:
        EXPECTED: * 'Please deposit a min of £XX.XX to continue placing your bet' message
        EXPECTED: * 'Deposit Amount' field
        EXPECTED: where,
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        """
        pass

    def test_006_close_quick_deposit_and_quick_bet_sections_via_x_button_one_by_one(self):
        """
        DESCRIPTION: Close Quick Deposit and Quick Bet sections via 'X' button one by one
        EXPECTED: * 'Quick Deposit' and 'Quick Bet' sections are closed
        """
        pass

    def test_007_log_out_of_app(self):
        """
        DESCRIPTION: Log out of app
        EXPECTED: User is logged
        """
        pass

    def test_008_log_in_with_user_that_has_usd_currency_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Log in with user that has 'USD' currency and repeat steps #2-7
        EXPECTED: 
        """
        pass

    def test_009_log_in_with_user_that_has_eur_currency_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Log in with user that has 'EUR' currency and repeat steps #2-7
        EXPECTED: 
        """
        pass

    def test_010_log_in_with_user_that_has_sek_currency_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Log in with user that has 'SEK' currency and repeat steps #2-7
        EXPECTED: 
        """
        pass
