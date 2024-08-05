import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C9272836_Verify_successful_deposit_via_Quick_Deposit_stand_alone_section(Common):
    """
    TR_ID: C9272836
    NAME: Verify successful deposit via 'Quick Deposit' stand alone section
    DESCRIPTION: This test case verifies successful depositing journey via 'Quick Deposit' stand alone
    DESCRIPTION: AUTOTEST [C16413759]
    PRECONDITIONS: 1. Roxanne app is loaded;
    PRECONDITIONS: 2. User has credit cards added to his account in 'Account One' portal;
    PRECONDITIONS: 3. User's balance is below 100 GBP
    PRECONDITIONS: 4. User is logged into an app.
    """
    keep_browser_open = True

    def test_001_tap_on_balance__tap_on_deposit_button_on_right_menu(self):
        """
        DESCRIPTION: Tap on 'Balance' > Tap on 'Deposit' button (on 'Right' menu)
        EXPECTED: 'Quick Deposit' section is opened
        """
        pass

    def test_002_select_any_card_within_the_credit_cards_dropdown(self):
        """
        DESCRIPTION: Select any card within the credit cards dropdown
        EXPECTED: Card is selected
        """
        pass

    def test_003_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: 'CVV' field is populated with entered 3-digit value
        """
        pass

    def test_004_enter_valid_value_into_deposit_amount_fieldvalid_value_is_a_value_that_doesnt_contradict_with_a_minimum_deposit_amount_rule(self):
        """
        DESCRIPTION: Enter valid value into 'Deposit Amount' field
        DESCRIPTION: (valid value is a value that doesn't contradict with a minimum deposit amount rule)
        EXPECTED: - 'Deposit Amount' field is populated with entered value
        EXPECTED: - 'Deposit' button becomes enabled
        """
        pass

    def test_005_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: * 'Quick Deposit' section remains opened
        EXPECTED: * User's balance is increased with amount entred on step 4
        EXPECTED: * Pop-up appears containing the following elements:
        EXPECTED: - Green 'check icon' and "Successful Deposit!" Header
        EXPECTED: - "Your new balance is <#Currency>X.XX",
        EXPECTED: - 'OK' button
        EXPECTED: ![](index.php?/attachments/get/36334)
        EXPECTED: where 'X.XX' is the amount shown in the balance at the right upper corner
        EXPECTED: 'currency' - the same as was set during registration
        """
        pass

    def test_006_click_ok_button_in_the_pop_up(self):
        """
        DESCRIPTION: Click 'OK' button in the pop-up
        EXPECTED: * Pop-up is closed.
        EXPECTED: * 'Quick Deposit' section is closed
        """
        pass
