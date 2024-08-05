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
class Test_C44870139_Verify_QD_is_working_fine_correct_pop_up_display__Quick_Deposit__and__buttons_functionality_Verify_Quick_Deposit_with_in_Quickbet__Verify_Multiple_deposit_cards_list_out_in_a_dorp_down_box_in_quickbet_betslip(Common):
    """
    TR_ID: C44870139
    NAME: "Verify QD is working fine , correct pop up display  -Quick Deposit   + and - buttons functionality -Verify Quick Deposit with in Quickbet  - Verify Multiple deposit cards list out in a dorp down box in quickbet/betslip"
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User has credit cards added to his account in 'Account One' portal;
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User tries to place a bet with insufficient balance ( i.e tries to place a bet of more than the balance)
    """
    keep_browser_open = True

    def test_001_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' section
        EXPECTED: 'Quick Deposit' header and 'X' button
        EXPECTED: Credit/Visa card section
        EXPECTED: 'CVV' editable field
        EXPECTED: 'Deposit Amount' editable field with '-' and '+' buttons
        EXPECTED: 'Quick Stakes' buttons
        EXPECTED: 'Deposit' button (disabled by default) and enabled only after CVV number is entered
        """
        pass

    def test_002_from_the_about_step_in_creditvisa_card_sectionverify_creditvisa_card_section(self):
        """
        DESCRIPTION: From the about step in Credit/Visa card section
        DESCRIPTION: Verify Credit/Visa card section
        EXPECTED: Credit card section consists of:
        EXPECTED: Credit cards Dropdown (case when user has more than 1 card registered)
        EXPECTED: or
        EXPECTED: Credit card Placeholder (No other card is seen when user adds only one card added)
        EXPECTED: Both dropdown and placeholder contain:
        EXPECTED: Credit Card Provider icon
        EXPECTED: Card number displayed in the next format: XXXX **** **** XXXX
        EXPECTED: where 'XXXX' - the first and last 4 number of the card
        EXPECTED: For mobile: 'Other payment option' is available on the Card drop down.
        """
        pass

    def test_003_from_the_step_1_in_the_amount_field_sectionverify_amount_field(self):
        """
        DESCRIPTION: From the Step 1 in the Amount field section
        DESCRIPTION: Verify 'Amount' field
        EXPECTED: 'Amount' field consists of £XX (required or selected amount to place a bet)
        """
        pass

    def test_004_from_the_step_1_in_the____plus_buttonsverify___plus_buttons(self):
        """
        DESCRIPTION: From the Step 1 in the  '-'/ '+' buttons
        DESCRIPTION: Verify '-'/ '+' buttons
        EXPECTED: The amount is decreased/increased by 5 every time user clicks them (works both for key board and quick deposit buttons)
        EXPECTED: If the input field is empty the '+' button populates it with amount of £5
        """
        pass

    def test_005_from_the_step_1close_x_the_qd_widget_and_click_on_make_a_deposit_tab_under_betslip(self):
        """
        DESCRIPTION: From the Step 1
        DESCRIPTION: Close ('X') the QD widget and click on 'Make a deposit' tab under betslip.
        EXPECTED: 'Quick Deposit' section is opened
        """
        pass

    def test_006_from_the_step_1tap_on_x_icon(self):
        """
        DESCRIPTION: From the Step 1
        DESCRIPTION: Tap on 'X' icon
        EXPECTED: 'Quick Deposit' section is closed
        """
        pass
