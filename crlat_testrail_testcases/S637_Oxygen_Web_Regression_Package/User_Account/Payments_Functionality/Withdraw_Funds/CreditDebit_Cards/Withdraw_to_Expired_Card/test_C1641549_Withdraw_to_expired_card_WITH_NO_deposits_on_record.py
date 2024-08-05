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
class Test_C1641549_Withdraw_to_expired_card_WITH_NO_deposits_on_record(Common):
    """
    TR_ID: C1641549
    NAME: Withdraw to expired card WITH NO deposits on record
    DESCRIPTION: This test case verifies ability to withdraw to an expired card and user didn't deposit from this card.
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has a card that expired
    PRECONDITIONS: User has not deposited from this card
    PRECONDITIONS: User balance is < 100
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon__withdraw(self):
        """
        DESCRIPTION: Tap Right menu icon > Withdraw
        EXPECTED: 'Withdraw' page is opened
        EXPECTED: Default payment method selected in dropdown
        """
        pass

    def test_002_in_payments_dropdown_select_a_card_from_preconditions(self):
        """
        DESCRIPTION: In payments dropdown select a card from preconditions
        EXPECTED: Withdraw button becomes grayed out.
        EXPECTED: User is prompted with a message:
        EXPECTED: "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card"
        EXPECTED: 'Click here' is hyperlinked
        EXPECTED: 'Edit expiry date' is hyperlinked and leads to Deposit page > My Payments.
        """
        pass

    def test_003_click_on_click_here(self):
        """
        DESCRIPTION: Click on "Click here"
        EXPECTED: User redirected to Add new credit/debit card page.
        """
        pass

    def test_004_go_back_to_withdraw_page__and_select_the_card_from_preconditions_click_edit_expiry_date(self):
        """
        DESCRIPTION: Go back to Withdraw page  and select the card from preconditions. Click Edit expiry date
        EXPECTED: User redirected to Deposit > My payments page.
        """
        pass

    def test_005_edit_expiry_date_for_this_card(self):
        """
        DESCRIPTION: Edit expiry date for this card
        EXPECTED: Expiry date is changed.
        """
        pass

    def test_006_go_back_to_withdraw_page_and_select_same_card_in_payments_method_dropdown(self):
        """
        DESCRIPTION: Go back to Withdraw page and select same card in payments method dropdown
        EXPECTED: There is no message: "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card"
        EXPECTED: Withdraw button becomes enabled.
        """
        pass
