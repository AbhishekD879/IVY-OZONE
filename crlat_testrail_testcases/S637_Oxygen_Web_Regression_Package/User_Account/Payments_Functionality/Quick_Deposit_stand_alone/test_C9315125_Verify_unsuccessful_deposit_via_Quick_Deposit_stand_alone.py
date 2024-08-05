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
class Test_C9315125_Verify_unsuccessful_deposit_via_Quick_Deposit_stand_alone(Common):
    """
    TR_ID: C9315125
    NAME: Verify unsuccessful deposit via 'Quick Deposit' stand alone
    DESCRIPTION: This test case verifies unsuccessful deposit via 'Quick Deposit' stand alone
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has cards added to his account
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: In order to check response open Dev Tools -> select Network -> WS -> Frames section
    """
    keep_browser_open = True

    def test_001_tap_on_right_menu__tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Right' menu > tap on 'Deposit' button
        EXPECTED: 'Quick Deposit' stand alone is opened
        """
        pass

    def test_002_enter_invalid_value_into_cvv_fieldnote_incorrect_cvv_can_be_used_for_triggering_error(self):
        """
        DESCRIPTION: Enter invalid value into 'CVV' field
        DESCRIPTION: **NOTE** incorrect CVV can be used for triggering error
        EXPECTED: 'CVV' field is populated with entered value
        """
        pass

    def test_003_enter_value_into_amount_field(self):
        """
        DESCRIPTION: Enter value into 'Amount' field
        EXPECTED: 'Amount' field is populated with entered value
        """
        pass

    def test_004_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: Error message is received in data.error.errorMessage value from 33014 response in WS
        EXPECTED: ![](index.php?/attachments/get/36322)
        """
        pass

    def test_005_log_in_with_user_that_has_0_balance_and_credit_cards_added_to_his_accountrepeat_steps_1_4(self):
        """
        DESCRIPTION: Log in with user that has 0 balance and credit cards added to his account:
        DESCRIPTION: Repeat steps #1-4
        EXPECTED: 
        """
        pass
