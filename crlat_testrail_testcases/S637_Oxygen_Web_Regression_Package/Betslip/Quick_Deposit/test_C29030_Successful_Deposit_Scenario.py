import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C29030_Successful_Deposit_Scenario(Common):
    """
    TR_ID: C29030
    NAME: Successful Deposit Scenario
    DESCRIPTION: This test case verifies Successful Depositing and Placing Bet functionality on the Bet Slip page via credit/debit cards.
    DESCRIPTION: Jira tickets:
    DESCRIPTION: * BMA-3455   (Quick Deposit on Betslip)
    DESCRIPTION: * BMA-10220 (Quick Deposit: User has Zero Funds in Account)
    DESCRIPTION: * BMA-10449 (Quick Deposit: Calculation of funds required)
    DESCRIPTION: * BMA-20368 (Betslip design - Quick deposit section)
    DESCRIPTION: * BMA-20463 New betslip - Nummeric keyboard (mobile only)
    PRECONDITIONS: 1. Load the app and log in with a user that has at list TWO credit cards added
    PRECONDITIONS: 2. Add selection to Betslip
    """
    keep_browser_open = True

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_002_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET' immediately
        """
        pass

    def test_003_press___plus_buttons(self):
        """
        DESCRIPTION: Press '-'/ '+' buttons
        EXPECTED: * The amount is decreased/increased by "N" (where N is a sum configured on GVC side) every time user clicks them (works both for keyboard and quick deposit buttons)
        EXPECTED: * If the input field is empty the '+' button populates it with the amount of "N"
        """
        pass

    def test_004_enter_valid_cvv_into_cvv_field_andtap_deposit_a_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV' field and
        DESCRIPTION: Tap 'DEPOSIT A BET' button
        EXPECTED: - Numeric keyboard without 'Quick stakes' buttons is displayed
        EXPECTED: - User 'Balance' doesn't change
        EXPECTED: - Bet is placed
        EXPECTED: - Bet Slip is replaced with a Bet Receipt view
        EXPECTED: - Successful message: **"Your deposit was successful and your bet has been placed"** is displayed at the bottom of Bet Receipt area (above 'Reuse Selection' and 'Done' buttons)
        """
        pass

    def test_005_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION'
        EXPECTED: - Same selection is displayed within Betslip content area
        EXPECTED: - Numeric keyboard is displayed (mobile only)
        """
        pass

    def test_006_repeat_step_1_2(self):
        """
        DESCRIPTION: Repeat step #1-2
        EXPECTED: All good
        """
        pass

    def test_007_choose_card_to_deposit_from_not_default_one(self):
        """
        DESCRIPTION: Choose card to deposit from (not default one)
        EXPECTED: - Card is selected
        """
        pass

    def test_008_enter_deposit_amount_larger_than_needed_to_cover_the_bet_additionally_needed_for_bet_placementbut_lower_than_deposit_limit(self):
        """
        DESCRIPTION: Enter deposit amount larger than needed to cover the bet (additionally needed for bet placement)
        DESCRIPTION: but lower than deposit limit
        EXPECTED: - Amount is displayed in 'Deposit Amount' edit field
        """
        pass

    def test_009_enter_valid_cvv_into_cvv_field_andtap_deposit_a_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV' field and
        DESCRIPTION: Tap 'DEPOSIT A BET' button
        EXPECTED: - The rest of deposited amount that was not needed to cover placed bet is funded to the user account
        EXPECTED: - Bet is placed
        EXPECTED: - User 'Balance' is changed accordingly
        EXPECTED: - No Message about exceeding Deposit Limits
        EXPECTED: - Bet Slip is replaced with a Bet Receipt view
        EXPECTED: - Successful message: **"Your deposit was successful and your bet has been placed"** is displayed at the bottom of Bet Receipt area (above 'Reuse Selection' and 'Done' buttons)
        """
        pass

    def test_010_tap_reuse_selection(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION'
        EXPECTED: - Same selection is displayed within Betslip content area
        EXPECTED: - Numeric keyboard is displayed (mobile only)
        """
        pass

    def test_011_enter_deposit_amount_smaller_than_needed_to_cover_the_bet_additionally_needed_for_bet_placementbut_lower_than_deposit_limit(self):
        """
        DESCRIPTION: Enter deposit amount smaller than needed to cover the bet (additionally needed for bet placement)
        DESCRIPTION: but lower than deposit limit
        EXPECTED: Amount is displayed in 'Deposit Amount' edit field
        """
        pass

    def test_012_tap_deposit_a_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT A BET' button
        EXPECTED: -   Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"** is displayed on the green background in the top of betslip content area (for a few seconds)
        EXPECTED: -   Bet is NOT placed
        EXPECTED: -   Deposit of entered amount is done
        EXPECTED: -   User 'Balance' is changed accordingly
        EXPECTED: -   No Message about exceeding Deposit Limits
        EXPECTED: -   ''Please deposit a min of "<currency symbol>XX.XX to continue placing your bet''  message is updated with the new value that is still needed
        EXPECTED: -   'Deposit Amount' field is updated with the missing funds value
        """
        pass
