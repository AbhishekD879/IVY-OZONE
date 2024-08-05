import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C1503378_Verify_Deposit_is_Unavailable_Using_Expired_Card(Common):
    """
    TR_ID: C1503378
    NAME: Verify Deposit is Unavailable Using Expired Card
    DESCRIPTION: This test case verifies Deposit functionality with expired card.
    DESCRIPTION: AUTOTEST MOBILE [C2493291]
    DESCRIPTION: AUTOTEST DESKTOP [C2536468]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has credit/debit card with expiration date > current date
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_002_in_payments_dropdown_select_an_expired_card(self):
        """
        DESCRIPTION: In payments dropdown select an expired card
        EXPECTED: - Deposit button becomes greyed out.
        EXPECTED: - User is prompted with a message:
        EXPECTED: "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card"
        EXPECTED: - 'Click here' is hyperlinked
        """
        pass

    def test_003_click_click_here(self):
        """
        DESCRIPTION: Click 'Click here'
        EXPECTED: User redirected to Add credit/debit card tab
        """
        pass

    def test_004_go_back_to_my_payments_tab(self):
        """
        DESCRIPTION: Go back to My Payments tab
        EXPECTED: 
        """
        pass

    def test_005_in_payments_dropdown_select_card_with_expiration_date__current_date(self):
        """
        DESCRIPTION: In payments dropdown select card with expiration date > current date
        EXPECTED: - Deposit button becomes enabled.
        EXPECTED: - There is no message "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card" .
        EXPECTED: - User is able to deposit
        """
        pass

    def test_006_repeat_steps_2_3_on_quick_deposit_on_betslip(self):
        """
        DESCRIPTION: Repeat steps 2-3 on Quick Deposit on Betslip
        EXPECTED: note: "Edit expiry date" should be hyperlinked and clicking it takes user to deposit page.
        """
        pass

    def test_007_repeat_steps_2_3_on_quick_deposit_on_quick_bet(self):
        """
        DESCRIPTION: Repeat steps 2-3 on Quick Deposit on Quick Bet
        EXPECTED: 
        """
        pass
