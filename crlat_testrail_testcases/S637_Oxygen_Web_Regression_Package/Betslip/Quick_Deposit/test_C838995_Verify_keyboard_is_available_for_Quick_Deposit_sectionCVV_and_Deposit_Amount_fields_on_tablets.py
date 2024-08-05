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
class Test_C838995_Verify_keyboard_is_available_for_Quick_Deposit_sectionCVV_and_Deposit_Amount_fields_on_tablets(Common):
    """
    TR_ID: C838995
    NAME: Verify keyboard is available for Quick Deposit section('CVV' and 'Deposit Amount' fields) on tablets
    DESCRIPTION: Verify keyboard is available for Quick Deposit section('CVV' and 'Deposit Amount' fields) on tablets
    PRECONDITIONS: User has added at least one Debit/Credit card
    """
    keep_browser_open = True

    def test_001_log_in_to_the_oxygen_app_on_ipad(self):
        """
        DESCRIPTION: Log in to the Oxygen app on iPad;
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_a_selection_to_betslip(self):
        """
        DESCRIPTION: Add a selection to betslip
        EXPECTED: Selection is displayed in Betslip widget
        """
        pass

    def test_003_enter_a_stake_higher_than_the_current_balance_of_a_user(self):
        """
        DESCRIPTION: Enter a stake higher than the current balance of a user
        EXPECTED: 'PLACE BET' button changes to 'MAKE A DEPOSIT'
        EXPECTED: 'Message about deposit amount needed in order to place bet is shown'
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button'
        EXPECTED: 
        """
        pass

    def test_005_tap_at_cvv_field(self):
        """
        DESCRIPTION: Tap at CVV field
        EXPECTED: - Cursor is focused in CVV field
        EXPECTED: - Device Keyboard appears
        """
        pass

    def test_006_tap_at_deposit_amount_field(self):
        """
        DESCRIPTION: Tap at 'Deposit Amount' field
        EXPECTED: - Cursor is focused in Amount field
        EXPECTED: - Device Keyboard appears
        """
        pass

    def test_007_fill_in_all_required_fields_and_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Fill in all required fields and tap "DEPOSIT & PLACE BET" button
        EXPECTED: Deposit and Bet is done successfully
        """
        pass
