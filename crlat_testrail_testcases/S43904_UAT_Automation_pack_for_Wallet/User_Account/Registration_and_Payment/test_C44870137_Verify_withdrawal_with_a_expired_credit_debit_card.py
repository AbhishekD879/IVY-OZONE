import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870137_Verify_withdrawal_with_a_expired_credit_debit_card(Common):
    """
    TR_ID: C44870137
    NAME: Verify withdrawal with a expired credit/debit card
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has at least 1 debit/credit card that expired card
    PRECONDITIONS: User has credit/debit card with expiration date > current date
    PRECONDITIONS: User has some money in the account.
    """
    keep_browser_open = True

    def test_001_open_withdraw_page(self):
        """
        DESCRIPTION: Open Withdraw page
        EXPECTED: 'Withdraw' page is opened
        """
        pass

    def test_002_in_payments_dropdown_select_an_expired_card(self):
        """
        DESCRIPTION: In payments dropdown select an expired card
        EXPECTED: Withdraw button becomes grayed out.
        EXPECTED: User is prompted with a message:
        EXPECTED: "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card"
        EXPECTED: 'Click here' is hyperlinked
        EXPECTED: 'Edit expiry date' is hyperlinked and leads to Deposit page > My Payments
        """
        pass

    def test_003_click_click_here(self):
        """
        DESCRIPTION: Click 'Click here'
        EXPECTED: User redirected to Add credit/debit card tab
        """
        pass

    def test_004_go_back_to_withdraw_page(self):
        """
        DESCRIPTION: Go back to Withdraw page
        EXPECTED: 
        """
        pass

    def test_005_in_payments_dropdown_select_card_with_expiration_date__current_date(self):
        """
        DESCRIPTION: In payments dropdown select card with expiration date > current date
        EXPECTED: Withdraw button becomes enabled.
        EXPECTED: There is no message "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card" . User is able to withdraw.
        """
        pass
