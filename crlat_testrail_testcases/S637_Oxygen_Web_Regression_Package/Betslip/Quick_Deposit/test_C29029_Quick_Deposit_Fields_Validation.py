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
class Test_C29029_Quick_Deposit_Fields_Validation(Common):
    """
    TR_ID: C29029
    NAME: Quick Deposit Fields Validation
    DESCRIPTION: This test case verifies all elements are present within Quick Deposit section and Fields Validation
    DESCRIPTION: AUTOTEST: [C2352380]
    PRECONDITIONS: 1. Load app and log in with a user that has at list one credit card added
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
        EXPECTED: *  'Quick Deposit' section is expanded and displayed at the bottom of the Betslip
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button and is disabled by default
        """
        pass

    def test_003_edit_stakeless_than_min_amount_5_gbp_eur_usd_or_50_sek(self):
        """
        DESCRIPTION: Edit 'Stake' (less than min amount: 5 GBP, EUR, USD or 50 SEK)
        EXPECTED: - 'Please deposit a min...' message is updated
        EXPECTED: - Quick Deposit Section remains expanded
        EXPECTED: - 'Deposit Amount' field contains a '<currency symbol> 5/50 Min' greyed out placeholder
        """
        pass

    def test_004_edit_deposit_amount_field_in_quick_deposit_section_type_more_than_7_digits_and_2_decimals_000_001_499__1__49__50a_z_a_z___plus_space(self):
        """
        DESCRIPTION: Edit 'Deposit Amount' Field in Quick Deposit section
        DESCRIPTION: * type <more than 7 digits and 2 decimals>
        DESCRIPTION: * 0.00, 0.01, 4.99, -1 / 49, -50
        DESCRIPTION: *<a-z, A-Z, ~!@#$%^&*()`__+={}|[]\:";'<>, <space>>"
        EXPECTED: -   Max number of digits is 7 and 2 decimal (e.g. "XXXXXXX.XX")
        EXPECTED: -   It is not allowed to enter letters or symbols
        """
        pass

    def test_005_select_card_by_using_the_card_dropdown(self):
        """
        DESCRIPTION: Select card by using the card dropdown
        EXPECTED: -  Card is chosen
        EXPECTED: -  It is possible to choose any other registered card to deposit from
        """
        pass

    def test_006_edit_cvv_field_type_more_than_3_digitsa_z_a_z___plus_space_12_00_9_0_9(self):
        """
        DESCRIPTION: Edit 'CVV' field
        DESCRIPTION: * type <more than 3 digits>
        DESCRIPTION: *<a-z, A-Z, ~!@#$%^&*()`__+={}|[]\:";'<>, <space>>"
        DESCRIPTION: * 12, 00, 9, 0, 9
        EXPECTED: -   It is not allowed to enter more than 3 digits on iOS
        EXPECTED: -   It is allowed to enter more than 3 digits on Android
        EXPECTED: (123.0, 9999, 0.0.0.0.0)
        EXPECTED: -   It is not allowed to enter symbols or letters
        """
        pass

    def test_007_enter_at_least_1_symbol_in_cvv_and_deposit_amount_fieldsand_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter at least 1 symbol in 'CVV*' and 'Deposit Amount' fields
        DESCRIPTION: and tap 'DEPOSIT & PLACE BET' button
        EXPECTED: - 'DEPOSIT & PLACE BET' button becomes enabled when at least 1 symbol is entered into 'CVV' and 'Deposit Amount' fields
        EXPECTED: - As value in 'Deposit Amount' field is less than 5/50 an error message appears below 'Deposit Amount' field: "The minimum deposit amount is <currency symbol>5"
        EXPECTED: - As value in 'CVV' is incorrect an error appears below 'CVV' field: "Your CV2 is incorrect."
        """
        pass
