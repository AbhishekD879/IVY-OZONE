import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870139_Verify_QD_is_working_fine_correct_pop_up_display_and_user_balance_is_updated_Quick_Deposit__and__buttons_functionality_Verify_Quick_Deposite_with_in_Quickbet__Verify_Multiple_deposit_cards_list_out_in_a_dorp_down_box_in_quickbet_betslip(Common):
    """
    TR_ID: C44870139
    NAME: "Verify QD is working fine , correct pop up display and user balance is updated -Quick Deposit   + and - buttons functionality -Verify Quick Deposite with in Quickbet  - Verify Multiple deposit cards list out in a dorp down box in quickbet/betslip"
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User has credit cards added to his account in 'Account One' portal;
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' section
        EXPECTED: 'Quick Deposit' header and 'X' button
        EXPECTED: Credit card section
        EXPECTED: 'CVV' editable field
        EXPECTED: 'Deposit Amount' editable field with '-' and '+' buttons
        EXPECTED: 'SET LIMITS' link
        EXPECTED: 'Quick Stakes' buttons
        EXPECTED: 'Deposit' button (disabled by default)
        """
        pass

    def test_002_verify_credit_card_section(self):
        """
        DESCRIPTION: Verify Credit card section
        EXPECTED: Credit card section consists of:
        EXPECTED: Credit cards Dropdown (case when user has more than 1 card registered)
        EXPECTED: or
        EXPECTED: Credit card Placeholder (No drop down seen when user adds only  one card added)
        EXPECTED: Both dropdown and placeholder contain:
        EXPECTED: Credit Card Provider icon
        EXPECTED: Card number displayed in the next format: **** **** **** XXXX
        EXPECTED: where 'XXXX' - the last 4 number of the card
        """
        pass

    def test_003_verify_amount_field(self):
        """
        DESCRIPTION: Verify 'Amount' field
        EXPECTED: 'Amount' field consists of text £5
        """
        pass

    def test_004_verify___plus_buttons(self):
        """
        DESCRIPTION: Verify '-'/ '+' buttons
        EXPECTED: The amount is decreased/increased by 10 every time user clicks them (works both for key board and quick deposit buttons)
        EXPECTED: If the input field is empty the '+' button populates it with amount of 10
        """
        pass

    def test_005_verify_set_limits_link(self):
        """
        DESCRIPTION: Verify 'SET LIMITS' link
        EXPECTED: 'Quick Deposit' section is closed after tapping 'SET LIMITS' link
        EXPECTED: User is navigated to Account One portal
        """
        pass

    def test_006_go_back_to_the_app_and_open_quick_deposit_section_again(self):
        """
        DESCRIPTION: Go back to the app and open 'Quick Deposit' section again
        EXPECTED: 'Quick Deposit' section is opened
        """
        pass

    def test_007_tap_on_x_icon(self):
        """
        DESCRIPTION: Tap on 'X' icon
        EXPECTED: 'Quick Deposit' section is closed
        """
        pass
