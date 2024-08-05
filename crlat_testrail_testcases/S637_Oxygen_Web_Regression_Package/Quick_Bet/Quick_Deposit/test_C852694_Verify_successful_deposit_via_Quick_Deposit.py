import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C852694_Verify_successful_deposit_via_Quick_Deposit(Common):
    """
    TR_ID: C852694
    NAME: Verify successful deposit via Quick Deposit
    DESCRIPTION: This test case verifies successful deposit via Quick Deposit section within Quick Bet
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
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * 'Quick Deposit' section is displayed instead of Quick Bet
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        EXPECTED: * 'Deposit Amount' field is pre-populated automatically with the difference between entered stake value and users balance
        EXPECTED: * '-' and '+' buttons are displayed on both sides of deposit amount input field
        """
        pass

    def test_005_select_visa_card(self):
        """
        DESCRIPTION: Select **Visa** card
        EXPECTED: **Visa** card is selected
        """
        pass

    def test_006_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: * 'CVV' field is populated with value with the entered value
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes enabled
        """
        pass

    def test_007_tap_plus__buttons_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '+'/'-' buttons near the deposit amount input field
        EXPECTED: * The amount is decreased/increased by 10 every time user clicks them (works both for key board and quick deposit buttons)
        EXPECTED: * If the amount is less than 15 all the amount will be cleared when pressing minus button
        EXPECTED: * If the input field is empty the '+' button populates it with amount of 10
        """
        pass

    def test_008_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: * User balance is changed on deposited amount
        EXPECTED: * Bet is placed automatically
        EXPECTED: * Bet Receipt is displayed
        EXPECTED: * 'Your Deposit was successful and your bet has been placed' message is displayed on green background below 'BET RECEIPT' header
        """
        pass

    def test_009_close_quick_bet_via_x_button(self):
        """
        DESCRIPTION: Close Quick Bet via 'X' button
        EXPECTED: Quick Bet is closed
        """
        pass

    def test_010_repeat_steps_2_8_but_on_step_6_enter_bigger_amount_than_needed_to_place_a_bet_step_3_in_stake_field(self):
        """
        DESCRIPTION: Repeat steps #2-8 but on step #6 enter bigger amount than needed to place a bet (step 3) in 'Stake' field
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_6_but_on_step_6_enter_lesser_amount_than_needed_to_place_a_bet_step_3_in_stake_field(self):
        """
        DESCRIPTION: Repeat steps #2-6 but on step #6 enter lesser amount than needed to place a bet (step 3) in 'Stake' field
        EXPECTED: 
        """
        pass

    def test_012_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: * User balance is changed on deposited amount
        EXPECTED: * Bet is NOT placed
        EXPECTED: * Value in 'Deposit Amount' field is re-calculated according to new difference between entered stake value and users balance
        EXPECTED: * 'CVV' field is cleared
        """
        pass

    def test_013_select_visa_electron_card_and_repeat_steps_6_11(self):
        """
        DESCRIPTION: Select **Visa Electron** card and repeat steps #6-11
        EXPECTED: 
        """
        pass

    def test_014_select_master_card_card_and_repeat_steps_6_11(self):
        """
        DESCRIPTION: Select **Master Card** card and repeat steps #6-11
        EXPECTED: 
        """
        pass

    def test_015_select_maestro_card_and_repeat_steps_6_11(self):
        """
        DESCRIPTION: Select **Maestro** card and repeat steps #6-11
        EXPECTED: 
        """
        pass

    def test_016_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is logged out
        """
        pass

    def test_017__log_in_with_user_that_has_0_balance_and_credits_card_added_to_his_account_repeat_steps_2_15(self):
        """
        DESCRIPTION: * Log in with user that has 0 balance and credits card added to his account
        DESCRIPTION: * Repeat steps #2-15
        EXPECTED: Upon Login a "Quick Deposit" popup window is expected to be displayed (due to 0 balance)
        """
        pass
