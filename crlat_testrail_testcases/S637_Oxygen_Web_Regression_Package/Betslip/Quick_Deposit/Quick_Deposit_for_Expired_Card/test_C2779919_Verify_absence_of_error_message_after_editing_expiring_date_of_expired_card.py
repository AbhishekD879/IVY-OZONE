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
class Test_C2779919_Verify_absence_of_error_message_after_editing_expiring_date_of_expired_card(Common):
    """
    TR_ID: C2779919
    NAME: Verify absence of error message after editing expiring date of expired card
    DESCRIPTION: This test case verifies that no error message is present on Quick Deposit on Betslip after changing expired date of expired card.
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has an expired card without deposits on record.
    """
    keep_browser_open = True

    def test_001_add_any_selection_to_the_bet_slip_and_open_bet_slip_page__widget(self):
        """
        DESCRIPTION: Add any selection to the Bet Slip and open Bet Slip page / widget
        EXPECTED: The selection is displayed within Bet Slip content area
        """
        pass

    def test_002_enter_stake_amount_that_exceeds_the_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount that exceeds the user`s balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_003_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET'
        """
        pass

    def test_004_on_quick_deposit_section_select_an_expired_card_with_no_deposits_on_record(self):
        """
        DESCRIPTION: On Quick Deposit section select an expired card with no deposits on record
        EXPECTED: 'DEPOSIT & PLACE BET'  button becomes grayed out.
        EXPECTED: User is prompted with a message "Sorry but your credit/debit card is expired. Please edit expiry date or click here to register a new card"
        """
        pass

    def test_005_navigate_to_deposit__my_payments_and_select_an_expired_card_with_no_deposits_on_record_in_payments_dropdown(self):
        """
        DESCRIPTION: Navigate to Deposit > My Payments and select an expired card with no deposits on record in payments dropdown
        EXPECTED: 
        """
        pass

    def test_006_edit_expiry_date_for_this_card(self):
        """
        DESCRIPTION: Edit expiry date for this card
        EXPECTED: Expiry date changes
        """
        pass

    def test_007_open_again_betslip__quick_bet_section_and_select_the_card_from_step_6(self):
        """
        DESCRIPTION: Open again Betslip > Quick bet section and select the card from step 6
        EXPECTED: 'DEPOSIT & PLACE BET' button is enabled.
        EXPECTED: No error messages.
        """
        pass

    def test_008_click_deposit__place_bet(self):
        """
        DESCRIPTION: Click 'DEPOSIT & PLACE BET'
        EXPECTED: The deposit is successful
        EXPECTED: The bet is placed successfully.
        """
        pass