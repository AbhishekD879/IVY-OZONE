import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29031_Unsuccessful_Deposit_Payments_Cancellation(Common):
    """
    TR_ID: C29031
    NAME: Unsuccessful Deposit Payments Cancellation
    DESCRIPTION: This test case verifies Unsuccessful Depositing functionality on the Bet Slip page via credit/debit cards and cancellation from payments system.
    PRECONDITIONS: * Load app and log in with a user that has at list one credit card added
    PRECONDITIONS: * Add selection to Betslip
    """
    keep_browser_open = True

    def test_001_enter_stake_amount_that_exceeds_the_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount that exceeds the user`s balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_002_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET'
        """
        pass

    def test_003_enter__valid_cvv_into_cvv_field__an_amount_that_is_more_than_the_selected_card_limitpayment_method_limit_into_deposit_amount_field(self):
        """
        DESCRIPTION: Enter:
        DESCRIPTION: - valid CVV into 'CVV' field
        DESCRIPTION: - an amount that is more than the Selected Card limit(payment method limit) into 'Deposit Amount' field
        EXPECTED: - No error messages appear
        """
        pass

    def test_004_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: -   User remains on the 'Bet Slip' page
        EXPECTED: -   User Balance is unchanged
        EXPECTED: -   'Deposit Amount' field remains unchanged
        EXPECTED: -  'CVV' field is cleared
        EXPECTED: -  [Coral]/[Ladbrokes] Error message appears within 'Quick Deposit' content area inside the 'i' information message
        EXPECTED: (e.g.
        EXPECTED: "Sorry, the maximum MC deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Sorry, the maximum VISA deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Sorry, the maximum MAESTRO deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Sorry, the maximum ELECTRON deposit amount is £100,000.00. Choose a smaller amount and try again."
        EXPECTED: "Canceled by the Payment Method System")
        EXPECTED: also check Error from in WebSockets. The "**message**" part of the error response is shown.  (e.g. "errorMessage":"Canceled by the Payment Method System".)
        EXPECTED: Note: If "message" part is absent, "errorMessage"/"description"/"errorDescription" part is shown (next available value in mentioned order)
        EXPECTED: WS/ Response ID: 33014
        """
        pass
