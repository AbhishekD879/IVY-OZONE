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
class Test_C9315122_Verify_deposit_using_expired_card_when_users_balance_is_100_and_expired_card_is_default_Quick_Deposit_stand_alone(Common):
    """
    TR_ID: C9315122
    NAME: Verify deposit using expired card when user's balance is > 100 and expired card is default ('Quick Deposit' stand alone)
    DESCRIPTION: This test case verifies Deposit functionality with expired card via 'Quick Deposit' stand alone when user's balance is > 100 and expired card is default payment method
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has a card that expired
    PRECONDITIONS: 3. User balance is > 100 and expired card is a default payment method
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_enter_valid_values_into_cvv__amount_fields(self):
        """
        DESCRIPTION: Enter valid values into 'CVV' & 'Amount' fields
        EXPECTED: - 'CVV' & 'Amount' fields are populated with entered values
        EXPECTED: - Expired card is selected by default
        EXPECTED: - Deposit' button becomes grayed out
        EXPECTED: - "Sorry, but your credit/debit card is expired. Please go to Account Settings to resolve the issue." message displayed.
        EXPECTED: ![](index.php?/attachments/get/36354)
        EXPECTED: ---
        EXPECTED: WHERE *Account Settings* is a tappable/clickable link-label, that redirects user to 'https://accountone.ladbrokes.com/deposit?clientType=sportsbook&back_url=https%3A%2F%2Fmsports.ladbrokes.com%2F' page, closing 'Quick Deposit' section once tapped/clicked.
        """
        pass
