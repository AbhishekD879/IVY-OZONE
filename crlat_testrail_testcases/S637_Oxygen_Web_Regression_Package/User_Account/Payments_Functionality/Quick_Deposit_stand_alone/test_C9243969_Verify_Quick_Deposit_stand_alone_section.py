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
class Test_C9243969_Verify_Quick_Deposit_stand_alone_section(Common):
    """
    TR_ID: C9243969
    NAME: Verify 'Quick Deposit' stand alone section
    DESCRIPTION: This test case verifies opening of 'Quick Deposit' via 'Deposit' button on 'Right' menu, when there are credit cards added to a user account in 'Account One' portal
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile [C16646869]
    PRECONDITIONS: 1. Roxanne app is loaded;
    PRECONDITIONS: 2. User with credit cards added to his account in 'Account One' portal is logged into an app.
    PRECONDITIONS: 3. User's balance is below 100 GBP
    """
    keep_browser_open = True

    def test_001_tap_on_balance_button(self):
        """
        DESCRIPTION: Tap on 'Balance' button
        EXPECTED: 'Right' menu (My Account) is opened
        """
        pass

    def test_002_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: 'My Account' menu is closed
        EXPECTED: 'Quick Deposit' section is opened
        """
        pass

    def test_003_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' section
        EXPECTED: - 'Quick Deposit' header and 'X' button
        EXPECTED: -  Credit card section
        EXPECTED: - 'CVV' editable field
        EXPECTED: - 'Deposit Amount' editable field with '-' and '+' buttons
        EXPECTED: - 'SET LIMITS' link
        EXPECTED: - 'Quick Stakes' buttons
        EXPECTED: - 'Deposit' button (disabled by default)
        """
        pass

    def test_004_verify_credit_card_section(self):
        """
        DESCRIPTION: Verify Credit card section
        EXPECTED: Credit card section consists of:
        EXPECTED: - Credit cards Dropdown (case when user has more than 1 card registered and his/her current balance is less than 100 GBP)
        EXPECTED: ![](index.php?/attachments/get/36326)
        EXPECTED: or
        EXPECTED: - Credit card Placeholder (case when user's balance is above or equal to 100 GBP OR one card added)
        EXPECTED: ![](index.php?/attachments/get/36327)
        EXPECTED: Both dropdown and placeholder contain:
        EXPECTED: - Credit Card Provider icon
        EXPECTED: - Card number displayed in the next format: **** **** **** XXXX
        EXPECTED: where 'XXXX' - the last 4 number of the card
        EXPECTED: ---
        EXPECTED: **Expanded(tapped) Credit cards dropdown is a native device OS-dependent feature**
        """
        pass

    def test_005_select_any_other_credit_card_if_available(self):
        """
        DESCRIPTION: Select any other credit card (if available)
        EXPECTED: 
        """
        pass

    def test_006_verify_other_payment_methods_availability(self):
        """
        DESCRIPTION: Verify other payment methods availability
        EXPECTED: Only credit cards are acceptable within 'Quick Deposit' section
        """
        pass

    def test_007_verify_amount_field(self):
        """
        DESCRIPTION: Verify 'Amount' field
        EXPECTED: - 'Amount' field is not populated
        EXPECTED: - Placeholder consists out of <currency symbol><5 or 50 (for currencies other than GBP/USD/EUR)> and 'Min' word
        EXPECTED: i.e. 'Є5 Min'
        """
        pass

    def test_008_verify___plus_buttons(self):
        """
        DESCRIPTION: Verify '-'/ '+' buttons
        EXPECTED: * The amount is decreased/increased by 10 every time user clicks them (works both for key board and quick deposit buttons)
        EXPECTED: * If the amount is less than 15 all the amount will be cleared when pressing minus button
        EXPECTED: * If the input field is empty the '+' button populates it with amount of 10
        """
        pass

    def test_009_verify_set_limits_link(self):
        """
        DESCRIPTION: Verify 'SET LIMITS' link
        EXPECTED: * 'Quick Deposit' section is closed after tapping 'SET LIMITS' link
        EXPECTED: * User is navigated to Account One portal
        """
        pass

    def test_010_go_back_to_the_app_and_open_quick_deposit_section_again(self):
        """
        DESCRIPTION: Go back to the app and open 'Quick Deposit' section again
        EXPECTED: 'Quick Deposit' section is opened
        """
        pass

    def test_011_tap_on_x_icon(self):
        """
        DESCRIPTION: Tap on 'X' icon
        EXPECTED: 'Quick Deposit' section is closed
        """
        pass
