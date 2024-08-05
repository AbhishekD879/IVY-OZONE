import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C852695_Verify_unsuccessful_deposit_via_Quick_Deposit(Common):
    """
    TR_ID: C852695
    NAME: Verify unsuccessful deposit via Quick Deposit
    DESCRIPTION: This test case verifies unsuccessful deposit via Quick Deposit within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: 4. Users have the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    PRECONDITIONS: 5. In order to check response open Dev Tools -> select Network -> WS -> Frames section
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * 'QUICK DEPOSIT' section is displayed within Quick Bet
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        """
        pass

    def test_005_select_visa_card(self):
        """
        DESCRIPTION: Select **Visa** card
        EXPECTED: **Visa** card is selected
        """
        pass

    def test_006_enter_cvv_in_cvv_field_amount_in_deposit_amount_field_if_needed(self):
        """
        DESCRIPTION: Enter CVV in 'CVV' field, amount in 'Deposit Amount' field (if needed)
        EXPECTED: * 'Deposit Amount' and 'CVV' fields are populated with values
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes enabled
        """
        pass

    def test_007_tap_plus_button_near_the_deposit_amount_input_field_then___button(self):
        """
        DESCRIPTION: Tap '+' button near the deposit amount input field then '-' button
        EXPECTED: The deposit amount is increased/decreased by 10 (user currency)
        """
        pass

    def test_008_tap_deposit__place_bet_buttonnote_incorrect_cvv_can_be_used_for_triggering_error(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        DESCRIPTION: **NOTE** incorrect CVV can be used for triggering error
        EXPECTED: * Error message is displayed on red background below 'QUICK  DEPOSIT' header
        EXPECTED: * User balance is NOT changed
        EXPECTED: * 'CVV' field is cleared
        EXPECTED: * 'Amount' field is not cleared
        """
        pass

    def test_009_verify_error_message(self):
        """
        DESCRIPTION: Verify error message
        EXPECTED: * Error message is received in **data.error.errorMessage** value from 33014 response in WS
        """
        pass

    def test_010_select_visa_electron_card_and_repeat_steps_6_8(self):
        """
        DESCRIPTION: Select **Visa Electron** card and repeat steps #6-8
        EXPECTED: 
        """
        pass

    def test_011_select_master_card_card_and_repeat_steps_6_8(self):
        """
        DESCRIPTION: Select **Master Card** card and repeat steps #6-8
        EXPECTED: 
        """
        pass

    def test_012_select_maestro_card_and_repeat_steps_6_8(self):
        """
        DESCRIPTION: Select **Maestro** card and repeat steps #6-8
        EXPECTED: 
        """
        pass

    def test_013_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is logged out
        """
        pass

    def test_014__log_in_with_user_that_has_0_balance_and_credit_cards_added_to_his_account_repeat_steps_2_11(self):
        """
        DESCRIPTION: * Log in with user that has 0 balance and credit cards added to his account
        DESCRIPTION: * Repeat steps #2-11
        EXPECTED: 
        """
        pass
