import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C15392887_EDITED_Quick_Deposit_section(Common):
    """
    TR_ID: C15392887
    NAME: [EDITED]  Quick Deposit section
    DESCRIPTION: This test case verifies Quick Deposit section within Betslip
    DESCRIPTION: "The Testcase needs to be edited according to Ladbrokes design and QB should be added too (+desktop)" - QB will be described as separate test scenario.
    PRECONDITIONS: 1. Load the app and log in with a user that has at list one credit card added;
    PRECONDITIONS: 2. Add selection to Betslip;
    PRECONDITIONS: 3. Betslip is opened with added selection;
    PRECONDITIONS: 4. User has a positive balance (recommended balance is less than 20 as it MAX amount for a single deposit(GVC Limitation))
    """
    keep_browser_open = True

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_002_change_value_in_stake_field_make_sure_that_value_still_exceeds_users_balance(self):
        """
        DESCRIPTION: Change value in 'Stake' field, make sure that value still exceeds user's balance
        EXPECTED: * Difference between entered stake value and users balance is recalculated immediately and displayed on  'Please deposit a min..' error message
        """
        pass

    def test_003_clicktap_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT AND PLACE BET' immediately and is disabled by default
        """
        pass

    def test_004_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: Quick Deposit section consists of:
        EXPECTED: * 'Quick Deposit' header and 'X' button
        EXPECTED: * Warning icon and 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message
        EXPECTED: * Credit cards drop-down
        EXPECTED: * 'CVV' label and field
        EXPECTED: * 'SET LIMITS' clickable link
        EXPECTED: * Quick stakes buttons are displayed
        EXPECTED: * 'Deposit Amount' label and field and '-' and '+' buttons
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        """
        pass

    def test_005_verify_credit_cards_drop_down(self):
        """
        DESCRIPTION: Verify credit cards drop-down
        EXPECTED: - Credit cards drop-down consists of in case when at list two cards are available:
        EXPECTED: * Card icon
        EXPECTED: * Card number displayed in the next format:
        EXPECTED: ****XXXX
        EXPECTED: where 'XXXX' - the last 4 number of the card
        EXPECTED: - Credit cards drop-down is missing when only one card is available, card is shown without dropdown
        """
        pass

    def test_006_clicktap_card_dropdown(self):
        """
        DESCRIPTION: Click/Tap card dropdown
        EXPECTED: * Credit card is displayed in the next format when only one item is present:
        EXPECTED: ****XXXX
        EXPECTED: * Credit card is displayed in the next format when at list two items are present
        EXPECTED: <payment system> ****XXXX
        EXPECTED: where
        EXPECTED: 'XXXX' - the last 4 number of the card,
        EXPECTED: <payment system>  - may be 'Visa', 'Master Card', 'Maestro'
        """
        pass

    def test_007_verify_card_correctness(self):
        """
        DESCRIPTION: Verify card correctness
        EXPECTED: Last 4 number of card corresponds to **data.payments.methods.[i].account.[j].specificParams** from 33012 response in WS
        EXPECTED: where
        EXPECTED: i - the number of all deposit methods added by user
        EXPECTED: j - the number of all cards added by user within one deposit method
        """
        pass

    def test_008_verify_deposit_amount_field(self):
        """
        DESCRIPTION: Verify 'Deposit Amount' field
        EXPECTED: * 'Deposit Amount' field is auto-populated with the difference between entered stake value and users balance if the amount needed for bet >5 or =5 EUR,GBP,USD;
        EXPECTED: * 'Deposit Amount' should be auto-populated with a minimum amount value if the amount needed for bet <5 EUR,GBP,USD;
        """
        pass

    def test_009_verify___and_plus_buttons(self):
        """
        DESCRIPTION: Verify '-' and '+' buttons
        EXPECTED: * '-' and '+' buttons always erase/add a sum of 10 (user currency)
        EXPECTED: * When amount less then 15 is inserted the minus button clears the field completely
        """
        pass

    def test_010_not_present_in_new_versions_of_cashier_app_verify_set_limits_link_navigation(self):
        """
        DESCRIPTION: NOT Present in new versions of Cashier app (Verify 'SET LIMITS' link navigation
        EXPECTED: * Betslip is closed after tapping 'SET LIMITS' link
        EXPECTED: * 'My Limits' page is opened in the same window
        EXPECTED: * URL is: https://xxx.coral.co.uk/limits
        """
        pass

    def test_011_verify_x_button(self):
        """
        DESCRIPTION: Verify 'X' button
        EXPECTED: * 'Quick Deposit' section is closed after clicking/tapping 'X' button
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message stays displayed at the bottom of Betslip
        """
        pass
