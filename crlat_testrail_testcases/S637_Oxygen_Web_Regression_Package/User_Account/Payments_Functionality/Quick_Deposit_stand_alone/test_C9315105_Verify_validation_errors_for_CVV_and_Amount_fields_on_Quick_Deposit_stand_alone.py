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
class Test_C9315105_Verify_validation_errors_for_CVV_and_Amount_fields_on_Quick_Deposit_stand_alone(Common):
    """
    TR_ID: C9315105
    NAME: Verify validation errors for 'CVV' and 'Amount' fields on 'Quick Deposit' stand alone
    DESCRIPTION: This test case verifies validation errors for 'CVV' and 'Amount' fields
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has credit cards added to his account
    PRECONDITIONS: 3. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_enter_less_than_3_digits_in_cvv_field(self):
        """
        DESCRIPTION: Enter less than 3 digits in 'CVV' field
        EXPECTED: - 'CVV' field is populated with entered value
        EXPECTED: - 'Deposit' button remains disabled
        """
        pass

    def test_002_enter_value_less_than_5_into_deposit_account_field(self):
        """
        DESCRIPTION: Enter value less than '5' into 'Deposit Account' field
        EXPECTED: - 'Deposit Account' field is populated with entered value
        EXPECTED: - 'Deposit' button becomes enabled
        """
        pass

    def test_003_tap_on_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Deposit' button
        EXPECTED: - 'Your CV2 is incorrect.' validation message is displayed below 'CVV' field
        EXPECTED: - The minimum deposit amount is <currency symbol> '5' validation message is displayed below 'Deposit Amount' field ('50' for currencies other than GBP, USD, EUR)
        EXPECTED: - Deposit is unsuccessful
        EXPECTED: where <currency symbol> - currency that was set during registration
        EXPECTED: ![](index.php?/attachments/get/36335)
        """
        pass
