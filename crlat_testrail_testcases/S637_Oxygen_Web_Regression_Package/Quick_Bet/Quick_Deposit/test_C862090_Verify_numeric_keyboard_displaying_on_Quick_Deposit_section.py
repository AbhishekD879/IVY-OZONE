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
class Test_C862090_Verify_numeric_keyboard_displaying_on_Quick_Deposit_section(Common):
    """
    TR_ID: C862090
    NAME: Verify numeric keyboard displaying on 'Quick Deposit' section
    DESCRIPTION: This test case verifies numeric keyboard displaying with Quick Deposit section on Quick Bet
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * User account with zero balance and supported card types added
    PRECONDITIONS: * User account with positive balance and supported card types added
    """
    keep_browser_open = True

    def test_001_log_in_as_user_with_zero_balance(self):
        """
        DESCRIPTION: Log in as user with zero balance
        EXPECTED: User is logged in
        """
        pass

    def test_002_quick_deposit_popup_window_should_be_displayed_outside_of_quickbet(self):
        """
        DESCRIPTION: Quick Deposit popup window should be displayed (outside of quickbet)
        EXPECTED: Verify that Quick Deposit popup window is displayed
        """
        pass

    def test_003_tap_on_x_of_popup_window(self):
        """
        DESCRIPTION: Tap on 'x' of popup window
        EXPECTED: Quick Deposit popup window should be closed
        """
        pass

    def test_004_add_one_selectionfill_valid_stake_and_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Add one selection
        DESCRIPTION: Fill valid 'Stake" and tap on 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is shown within Quick Bet
        EXPECTED: - 'Quick stakes' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_005_set_focus_over_deposit_amount_or_cvv_field_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Deposit Amount' or 'CVV' field in 'Quick Deposit' section
        EXPECTED: * Numeric keyboard appears
        EXPECTED: * 'Quick stakes' buttons are NOT present on Numeric keyboard
        """
        pass

    def test_006_tap_on_quick_deposit_section_headerx_button_in_quick_deposit_sectionquick_deposit_link_in_the_quick_bet_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header/'X' button in 'Quick Deposit' section/'Quick Deposit' link in the Quick Bet header
        EXPECTED: - Numeric Keyboard disappears
        EXPECTED: - 'Quick Deposit' section is collapsed
        """
        pass

    def test_007_enter_value_into_stake_field(self):
        """
        DESCRIPTION: Enter value into 'Stake' field
        EXPECTED: - 'Quick Deposit' section remains collapsed
        """
        pass

    def test_008_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is opened
        """
        pass

    def test_009_set_focus_over_deposit_amount_or_cvv_fields_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Deposit Amount' or 'CVV' fields in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard appear below 'CVV' and 'Deposit Amount' fields
        """
        pass

    def test_010_log_out_and_log_in_as_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log out and Log in as user account with positive balance
        EXPECTED: User is logged in
        """
        pass

    def test_011_select_one_selection_to_quick_bet_and_enter_higher_stake_than_user_balance(self):
        """
        DESCRIPTION: Select one selection to Quick Bet and enter higher stake than user balance
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: - Numeric keyboard remains shown
        """
        pass

    def test_012_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is displayed
        EXPECTED: - Numeric keyboard is hidden
        EXPECTED: - 'Quick stakes' buttons are displayed
        """
        pass

    def test_013_set_focus_over_deposit_amount_orand_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Deposit Amount' or/and 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard appear below 'CVV' and 'Deposit Amount' fields
        EXPECTED: - 'Quick stakes' buttons are NOT present on Numeric keyboard
        """
        pass

    def test_014_tap_on_quick_deposit_section_headerx_button_in_quick_deposit_sectionquick_deposit_link_in_the_betslip_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header/'X' button in 'Quick Deposit' section/'Quick Deposit' link in the Betslip header
        EXPECTED: - 'Quick Deposit' section disappears
        EXPECTED: - Numeric keyboard is no longer available
        """
        pass
