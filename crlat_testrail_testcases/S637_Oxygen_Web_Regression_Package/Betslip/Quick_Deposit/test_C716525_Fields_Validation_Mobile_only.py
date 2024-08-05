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
class Test_C716525_Fields_Validation_Mobile_only(Common):
    """
    TR_ID: C716525
    NAME: Fields Validation (Mobile only)
    DESCRIPTION: This test case verifies all elements present within Quick Deposit section and Fields Validation
    PRECONDITIONS: * Load app and log in with a user that has at least two credit cards tied to his/her account
    PRECONDITIONS: * Add selection to Betslip
    """
    keep_browser_open = True

    def test_001_enter_stake_amount_that_exceeds_the_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount that exceeds the user`s balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately
        """
        pass

    def test_002_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * 'Quick Deposit' section is expanded and displayed at the bottom of the Bet Slip
        EXPECTED: * 'MAKE A DEPOSIT'  changed to  'DEPOSIT & PLACE BET' button and is not clickable
        """
        pass

    def test_003_switch_to_a_stakepreviously_entered_in_betslip_and_edit_its_value_using_numeric_keyboard(self):
        """
        DESCRIPTION: Switch to a Stake(previously entered in Betslip) and edit its value using numeric keyboard
        EXPECTED: - Amount needed on 'Please deposit a min..' message is changed according to new stake value
        EXPECTED: - 'QUICK DEPOSIT' section remains expanded
        EXPECTED: - 'Deposit Amount' field contains prepopulated value XX.XX
        EXPECTED: where XX.XX - the amount needed to be additionally deposited to complete bet placement (entered Stake minus Current Balance)
        EXPECTED: - Numeric keyboard with 'quick stakes' buttons are shown within 'QUICK DEPOSIT' section
        """
        pass

    def test_004_edit_stake_valuein_betslip_to_a_point_when_it_will_still_be_more_than_users_balance_but_deposit_amount_would_be_less_than_minimum_allowed_deposit_min_amount_are__5_gbp_eur_usd_or_50_sek(self):
        """
        DESCRIPTION: Edit Stake value(in Betslip) to a point when it will still be more than user's balance, but deposit amount would be less than minimum allowed (deposit min amount are : 5 GBP, EUR, USD or 50 SEK)
        EXPECTED: - Amount needed on 'Please deposit a min..' message is changed according to new stake value
        EXPECTED: - Quick Deposit Section remains expanded
        EXPECTED: -  'Deposit Amount' Field now contains a '<currency symbol> 5/50 Min' greyed out placeholder
        """
        pass

    def test_005_edit_deposit_amount_field_in_quick_deposit_section_type_more_than_7_digits_and_2_decimals_000_001_499_49(self):
        """
        DESCRIPTION: Edit 'Deposit Amount' Field in Quick Deposit section
        DESCRIPTION: * type <more than 7 digits and 2 decimals>
        DESCRIPTION: * 0.00, 0.01, 4.99, 49
        EXPECTED: -   Max number of digits is 7 and 2 decimal (e.g. "XXXXXXX.XX")
        """
        pass

    def test_006_press___plus_buttons(self):
        """
        DESCRIPTION: Press '-'/ '+' buttons
        EXPECTED: The amount is decreased/increased by 10
        EXPECTED: If the amount is less than 15 all the amount will be cleared when pressing minus button.
        """
        pass

    def test_007_select_card_by_card_dropdown(self):
        """
        DESCRIPTION: Select card by card dropdown
        EXPECTED: -  Card icon corresponds to card type (check response)
        EXPECTED: -   Green tick is displayed above selected card
        EXPECTED: -   It is possible to choose any of registered cards to deposit from
        """
        pass

    def test_008_edit_cvv_field_12_00_9_0_9_type_more_than_3_digits(self):
        """
        DESCRIPTION: Edit 'CVV' field
        DESCRIPTION: * 12, 00, 9, 0, 9
        DESCRIPTION: * type <more than 3 digits>
        EXPECTED: -   It is not allowed to enter more than 3 digits
        EXPECTED: -   '.' button is disabled on numeric keyboard when focus on 'CVV' field
        """
        pass

    def test_009_enter_at_least_1_symbol_in_cvv_and_amount__fieldsand_click_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter at least 1 symbol in 'CVV*' and 'Amount *' fields
        DESCRIPTION: and Click 'DEPOSIT & PLACE BET' button
        EXPECTED: - 'DEPOSIT & PLACE BET' button becomes enabled when at least 1 symbol is entered into 'CVV' and 'Deposit Amount' fields
        EXPECTED: - As value in 'Deposit Amount' field is less than 5/50 an error message appears below 'Deposit Amount' field: "The minimum deposit amount is <currency symbol>5/SEK 50."
        EXPECTED: - As value in 'CVV' is incorrect an error appears below 'CVV' field: "Your CV2 is incorrect."
        """
        pass
