import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2031560_Verify_validation_rules_of_Enter_Code_or_Number_field(Common):
    """
    TR_ID: C2031560
    NAME: Verify validation rules of 'Enter Code or Number' field
    DESCRIPTION: This test case verify validation rules on the Bet Tracker page
    PRECONDITIONS: Make sure Bet Tracker feature is turned on in CMS: System configuration -> Connect -> shop Bet Tracker
    PRECONDITIONS: * Load SpotBook App
    PRECONDITIONS: * Chose 'Connect' from header ribbon -> Connect landing page is opened
    PRECONDITIONS: * Tap 'Shop Bet Tracker' item -> Bet Tracker page is opened
    """
    keep_browser_open = True

    def test_001_verify_enter_code_or_number_field(self):
        """
        DESCRIPTION: Verify 'Enter Code or Number' field
        EXPECTED: * After tapping ''Use Coupon Code or Bet Receipt number'' link additional area is expanded
        EXPECTED: * Entry field and 'Submit' button are displayed
        """
        pass

    def test_002_verify_that_only_7_letters_code_or_12_for_otc_or_13_for_ssbt_codes_numbers_could_be_entered_into_enter_code_or_number_field(self):
        """
        DESCRIPTION: Verify that only 7 letters code OR 12 (for OTC) or 13 (for SSBT codes) numbers could be entered into 'Enter Code or Number' field
        EXPECTED: 
        """
        pass

    def test_003_enter_mixture_of_numbers_and_letters_into_enter_code_or_number_field(self):
        """
        DESCRIPTION: Enter mixture of numbers and letters into 'Enter Code or Number' field
        EXPECTED: Error message is displayed immediately after entering first incorrect symbol:
        EXPECTED: 'Only letters OR numbers can be entered in this field'
        """
        pass

    def test_004_verify_that_only_7_letters_code_could_be_submitted_successfully(self):
        """
        DESCRIPTION: Verify that only 7 letters code could be submitted successfully
        EXPECTED: * Field 'Enter Code or Number' doesn't allow to enter more than 7 letters
        EXPECTED: * If less than 7 letters code is submitted then error message is displayed 'The coupon code/number entered is incorrect, please try again'
        """
        pass

    def test_005_verify_field_behavior_while_entering_cash_out_code_only_letters(self):
        """
        DESCRIPTION: Verify field behavior while entering cash out code (only letters)
        EXPECTED: After entering 4th letter a hyphen is inserted automatically, so code is to be displayed in format XXX-XXXX
        """
        pass

    def test_006_verify_that_12_otc_digit_numbers_could_be_submitted_successfully(self):
        """
        DESCRIPTION: Verify that 12 (OTC) digit numbers could be submitted successfully
        EXPECTED: * If less than 12 numbers are submitted then error message is displayed 'The coupon code/number entered is incorrect, please try again'
        EXPECTED: * 12-digit OTC code is successfully added
        """
        pass

    def test_007_verify_that_13_ssbt_digit_numbers_could_be_submitted_successfully(self):
        """
        DESCRIPTION: Verify that 13 (SSBT) digit numbers could be submitted successfully
        EXPECTED: * 13-digit SSBT code is successfully added
        EXPECTED: * 13+ number cannot be entered into the field
        """
        pass
