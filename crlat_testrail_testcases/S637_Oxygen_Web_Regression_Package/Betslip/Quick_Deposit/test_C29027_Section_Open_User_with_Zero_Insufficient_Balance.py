import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29027_Section_Open_User_with_Zero_Insufficient_Balance(Common):
    """
    TR_ID: C29027
    NAME: Section Open User with Zero/ Insufficient Balance
    DESCRIPTION: This test case verifies 'Quick Deposit' section on the Betslip for the User with 0 or Insufficient balance
    PRECONDITIONS: 1.  User account with **0 balance and at least one registered Credit Card** (Additional pop-up Quick Deposit)
    PRECONDITIONS: 2.  User account with **positive balance and at least one registered Credit Card**
    """
    keep_browser_open = True

    def test_001_load_application_and_log_in_with_account_1(self):
        """
        DESCRIPTION: Load application and Log in with account 1
        EXPECTED: - User is logged in
        """
        pass

    def test_002_open_the_betslip_pagewidget_with_an_added_selection(self):
        """
        DESCRIPTION: Open the Betslip page/widget with an added selection
        EXPECTED: - Made selection is displayed correctly within Betslip content area
        EXPECTED: **Coral**
        EXPECTED: - 'QUICK DEPOSIT' section is displayed on the bottom of the Bet Slip
        EXPECTED: - 'Please deposit a min of <currency>5.00/50 for SEK to continue placing your bet' default message is shown within Quick Deposit
        EXPECTED: - 'DEPOSIT' button is shown at the bottom of the section
        EXPECTED: **Ladbrokes**
        EXPECTED: - There is NO 'Quick Deposit' section or error message displayed on the Bet Slip
        """
        pass

    def test_003_coralclicktap_x_close_icon(self):
        """
        DESCRIPTION: **Coral**
        DESCRIPTION: Click/Tap 'X' (Close) icon
        EXPECTED: **Coral**
        EXPECTED: - 'QUICK DEPOSIT' section is closed
        EXPECTED: - 'DEPOSIT' button changes to 'PLACE BET'
        """
        pass

    def test_004_enter_value_less_than_5_in_the_stake_field(self):
        """
        DESCRIPTION: Enter value less than 5 in the 'Stake' field
        EXPECTED: - 'Please deposit a min of <currency>5.00/50 for SEK to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: - 'PLACE BET' button becomes 'MAKE A DEPOSIT'
        """
        pass

    def test_005_enter_value_equal_or_more_than_5_in_the_stake_field(self):
        """
        DESCRIPTION: Enter value equal or more than 5 in the 'Stake' field
        EXPECTED: - 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: - 'PLACE BET' button becomes 'MAKE A DEPOSIT'
        """
        pass

    def test_006_clicktap_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is present
        EXPECTED: - 'Please deposit a min of <currency>XX.XX to continue placing your bet' error message is shown within 'QUICK DEPOSIT' section
        EXPECTED: -  The 'Deposit Amount' field must be in real time auto-populated with the calculated funds needed to cover the User’s bet
        EXPECTED: - 'DEPOSIT &/AND PLACE BET' button is shown at the bottom of the section
        """
        pass

    def test_007_clicktap_x_close_icon(self):
        """
        DESCRIPTION: Click/Tap 'X' (Close) icon
        EXPECTED: - 'QUICK DEPOSIT' section is closed
        EXPECTED: - 'DEPOSIT &/AND PLACE BET' button becomes 'MAKE A DEPOSIT'
        """
        pass

    def test_008_change_value_in_stake_field_and_open_quick_deposit_section(self):
        """
        DESCRIPTION: Change value in 'Stake' field and Open 'QUICK DEPOSIT' section
        EXPECTED: - Value is recalculated in 'Please deposit a min..' message and 'Deposit Amount' field to cover the User's bet in real time
        """
        pass

    def test_009_add_a_few_more_selections_to_the_bet_slip_open_the_bet_slip_and_enter_stake_for_added_selections(self):
        """
        DESCRIPTION: Add a few more selections to the Bet Slip, open the Bet Slip and enter 'Stake' for added selections
        EXPECTED: - Value is recalculated in 'Please deposit a min..' message and 'Deposit Amount' field to cover the User's bet in real time
        """
        pass

    def test_010_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - User is  logged out
        EXPECTED: - There is NO 'Quick Deposit' section or error message displayed on the Bet Slip
        """
        pass

    def test_011_log_in_with_account_2(self):
        """
        DESCRIPTION: Log in with account 2
        EXPECTED: - User is logged in
        """
        pass

    def test_012_open_the_betslip_pagewidget(self):
        """
        DESCRIPTION: Open the Betslip page/widget
        EXPECTED: - Made selection is displayed within Betslip content area
        EXPECTED: - There is NO 'QUICK DEPOSIT' section or error message displayed on the Bet Slip
        EXPECTED: - Numeric keyboard with 'Quick stakes' buttons are displayed (if one selection has been added, mobile only)
        """
        pass

    def test_013_enter_stake_amount_greater_than_current_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount greater than current user's balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_014_repeat_steps_6_10(self):
        """
        DESCRIPTION: Repeat steps 6-10
        EXPECTED: 
        """
        pass
