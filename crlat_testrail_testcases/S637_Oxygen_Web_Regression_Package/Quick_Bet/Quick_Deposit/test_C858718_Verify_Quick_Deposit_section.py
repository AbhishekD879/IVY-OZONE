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
class Test_C858718_Verify_Quick_Deposit_section(Common):
    """
    TR_ID: C858718
    NAME: Verify Quick Deposit section
    DESCRIPTION: This test case verifies Quick Deposit section within Quick Bet
    DESCRIPTION: NOTE: **Vanilla** specific test cases [C23820446] and [C14876363]
    DESCRIPTION: Test case needs to be updated according to new wallet functionality
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: 4. User has the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    PRECONDITIONS: 5. In order to check response open Dev Tools -> select Network -> WS -> Frames section
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_sport_raceselection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race>selection to Quick Bet
        EXPECTED: Quick bet section(modal) appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance_and_select_ew_checkbox_if_available(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance and select 'E/W' checkbox (if available)
        EXPECTED: * 'Stake' field is populated with value
        EXPECTED: * 'E/W' checkbox is selected
        EXPECTED: * Info icon and 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message is displayed below Quick Stakes buttons immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and user's balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_004_change_value_in_stake_field_make_sure_that_value_still_exceeds_users_balance(self):
        """
        DESCRIPTION: Change value in 'Stake' field, make sure that value still exceeds user's balance
        EXPECTED: * Difference between entered stake value and users balance is recalculated immediately and displayed within  'Please deposit a min..' message
        """
        pass

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed over of Quick Bet
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET' immediately and is disabled by default. Only this button is present
        EXPECTED: * X close button is displayed on the upper right corner
        """
        pass

    def test_006_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: Quick Deposit section consists of:
        EXPECTED: * 'Quick Deposit' header and 'X' button
        EXPECTED: * Info icon and 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message
        EXPECTED: * Credit cards drop-down
        EXPECTED: * 'CVV' label and field
        EXPECTED: * 'SET LIMITS' clickable link
        EXPECTED: * Quick stakes buttons are displayed
        EXPECTED: * 'Deposit Amount' label and field and '-' and '+' buttons
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        """
        pass

    def test_007_verify_credit_cards_drop_down(self):
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

    def test_008_tap_card_dropdown(self):
        """
        DESCRIPTION: Tap card dropdown
        EXPECTED: * Credit card is displayed in the next format when focusing selected card:
        EXPECTED: ****XXXX
        EXPECTED: * Credit card is displayed in the next format for the rest cards available:
        EXPECTED: <payment system> ****XXXX
        EXPECTED: where
        EXPECTED: 'XXXX' - the last 4 number of the card,
        EXPECTED: <payment system>  - may be 'Visa', 'Master Card', 'Maestro'
        """
        pass

    def test_009_verify_card_correctness(self):
        """
        DESCRIPTION: Verify card correctness
        EXPECTED: Last 4 number of card corresponds to **data.payments.methods.[i].account.[j].specificParams** from 33012 response in WS
        EXPECTED: where
        EXPECTED: i - the number of all deposit methods added by user
        EXPECTED: j - the number of all cards added by user within one deposit method
        """
        pass

    def test_010_verify_payment_methods_availability(self):
        """
        DESCRIPTION: Verify payment methods availability
        EXPECTED: * Only credit cards are acceptable within Quick Deposit section
        EXPECTED: * Paypal and Neteller payment methods are NOT shown even when they are returned in 33012 response in WS
        """
        pass

    def test_011_verify_deposit_amount_field(self):
        """
        DESCRIPTION: Verify 'Deposit Amount' field
        EXPECTED: * 'Deposit Amount' field is auto-populated with the difference between entered stake value and users balance
        """
        pass

    def test_012_verify___plus_buttons(self):
        """
        DESCRIPTION: Verify '-'/ '+' buttons
        EXPECTED: * The amount is decreased/increased by 10 every time user clicks them (works both for key board and quick deposit buttons)
        EXPECTED: * If the amount is less than 15 all the amount will be cleared when pressing minus button
        EXPECTED: * If the input field is empty the '+' button populates it with amount of 10
        """
        pass

    def test_013_verify_set_limits_link_navigation(self):
        """
        DESCRIPTION: Verify 'SET LIMITS' link navigation
        EXPECTED: * 'My Limits' page is opened in the same window
        EXPECTED: * URL is: https://xxx.coral.co.uk/limits
        """
        pass

    def test_014_verify_set_limits_back_button(self):
        """
        DESCRIPTION: Verify 'SET LIMITS' Back button
        EXPECTED: * User is navigated to the even page
        EXPECTED: * Quick Bet is not opened
        """
        pass

    def test_015_verify_x_button(self):
        """
        DESCRIPTION: Verify 'X' button
        EXPECTED: * 'Quick Deposit' section is closed after tapping 'X' button
        EXPECTED: * 'Quick Bet' section is displayed
        EXPECTED: * Entered value is displayed in 'Stake' field
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass
