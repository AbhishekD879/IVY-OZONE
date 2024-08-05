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
class Test_C399867_TO_BE_ARCHIVED_Section_Display_User_with_Balance_Above_Below_100_PayPal_NETELLER(Common):
    """
    TR_ID: C399867
    NAME: [TO BE ARCHIVED] Section Display User with Balance Above/Below 100 & PayPal/NETELLER
    DESCRIPTION: This test case verifies  Payment methods display within Quick Deposit Section on Betslip area in case default payment method is PayPall/NETELLER and balance is above or below 100.
    DESCRIPTION: ** JIRA tickets:**
    DESCRIPTION: BMA-20368 Betslip design - Quick deposit section
    DESCRIPTION: BMA-20463 New betslip - Nummeric keyboard (mobile only)
    PRECONDITIONS: 1. User account with balance >=100 and more than one Credit Cards + other payment method PayPall/NETELLER (default)
    PRECONDITIONS: 2. User account with balance >=100 and more than one Credit Cards (1 card is default) + other payment method PayPall/NETELLER
    PRECONDITIONS: 3. User account with balance <100 and more than one Credit Card + other payment method PayPall/NETELLER (default)
    PRECONDITIONS: 4. User account with balance <100 and more than one Credit Cards (1 card is default) + other payment method PayPall/NETELLER
    PRECONDITIONS: Applies for **Mobile** and **Tablet**
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: - Homepage is shown
        """
        pass

    def test_002_login_with_account_1__2(self):
        """
        DESCRIPTION: Login with account 1) / 2)
        EXPECTED: - User is logged in
        """
        pass

    def test_003_add_a_selection_to_the_betslip_and_open_bet_slip_page___widget(self):
        """
        DESCRIPTION: Add a selection to the Betslip and open Bet Slip page  / widget
        EXPECTED: - Selection is displayed within Betslip content area
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons are displayed (if one selection has been added, mobile only)
        """
        pass

    def test_004_enter_stake_that_is_greater_than_users_balance(self):
        """
        DESCRIPTION: Enter Stake that is greater than User's Balance
        EXPECTED: - 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message appears on the red background, anchored to the footer of the Betslip, and in real time get the funds value calculated in order to cover the User’s bet
        """
        pass

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'Make a Deposit' button
        EXPECTED: - 'Quick Deposit' section is present
        EXPECTED: - PayPall/NETELLER are not Displayed in Quick Deposit Section at all even it is default method
        EXPECTED: - Only Last used credit card is displayed within Quick Deposit Section and marked with green tick icon
        """
        pass

    def test_006_enter_valid_cvv_into_cvv_field_andtap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV' field and
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: - User 'Balance' is changed accordingly
        EXPECTED: - Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"** is displayed on green background in the top of betslip content area (for a few seconds)
        EXPECTED: - Bet is placed
        EXPECTED: - Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_007_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION'
        EXPECTED: - Same selection is displayed within Betslip content area
        EXPECTED: - Numeric keyboard is displayed (mobile only)
        """
        pass

    def test_008_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - User is Logged out
        """
        pass

    def test_009_login_with_account_3__4(self):
        """
        DESCRIPTION: Login with account 3) / 4)
        EXPECTED: - User is  logged in
        """
        pass

    def test_010_open_bet_slip_page___widget(self):
        """
        DESCRIPTION: Open Bet Slip page  / widget
        EXPECTED: - Selection is displayed within Betslip content area
        """
        pass

    def test_011_enter_stake_that_is_greater_than_users_balance(self):
        """
        DESCRIPTION: Enter Stake that is greater than User's Balance
        EXPECTED: - 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message appears on the red background, anchored to the footer of the Betslip, and in real time get the funds value calculated in order to cover the User’s bet
        """
        pass

    def test_012_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'Make a Deposit' button
        EXPECTED: - 'Quick Deposit' section is present
        EXPECTED: - PayPall/NETELLER are not Displayed in Quick Deposit Section at all
        EXPECTED: - All User registered credit cards are displayed within Quick Deposit Section in Desc order and Last Used is marked with green tick icon
        """
        pass

    def test_013_enter_valid_cvv_into_cvv_field_andtap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV' field and
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: - User 'Balance' is changed accordingly
        EXPECTED: - Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"** is displayed on green background in the top of betslip content area (for a few seconds)
        EXPECTED: - Bet is placed
        EXPECTED: - Bet Slip is replaced with a Bet Receipt view
        """
        pass
