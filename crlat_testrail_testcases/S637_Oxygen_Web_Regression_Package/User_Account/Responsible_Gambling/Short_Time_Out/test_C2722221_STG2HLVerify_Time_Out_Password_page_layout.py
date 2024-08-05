import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C2722221_STG2HLVerify_Time_Out_Password_page_layout(Common):
    """
    TR_ID: C2722221
    NAME: [STG2][HL]Verify 'Time-Out Password' page layout
    DESCRIPTION: This test case verifies 'Time-Out Password' page layout
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link for reach the 'Time-Out' page
    PRECONDITIONS: * Select any value from the 'Select period of time-out' dropdown and tick any 'Reason for time-out' checkbox
    PRECONDITIONS: * Click/Tap on 'Continue' button
    PRECONDITIONS: * 'Time-Out Password' page is opened
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 'Responsible Gambling' page with all sections are CMS configurable. Please, take a look at https://ladbrokescoral.testrail.com/index.php?/cases/view/28369 to get acquainted with the instruction how to create or update content on 'Responsible Gambling' page.
    """
    keep_browser_open = True

    def test_001_verify_time_out_password_page_layout(self):
        """
        DESCRIPTION: Verify 'Time-Out Password' page layout
        EXPECTED: * Header with 'Time Out' title and 'Back' button
        EXPECTED: * Time-Out expiration date
        EXPECTED: * 'Password' field
        EXPECTED: * Hard-coded text
        EXPECTED: * 'Continue' button
        EXPECTED: * 'Cancel' button
        """
        pass

    def test_002_verify_time_out_expiration_date(self):
        """
        DESCRIPTION: Verify Time-Out expiration date
        EXPECTED: Time-Out expiration date is displayed in the next format:
        EXPECTED: dd/mm/yyyy hh:mm
        """
        pass

    def test_003_verify_password_field(self):
        """
        DESCRIPTION: Verify 'Password' field
        EXPECTED: * 'Please confirm with your password below:' text is displayed above the field
        EXPECTED: * 'Password' placeholder is displayed within the field by default
        """
        pass

    def test_004_verify_showhide_button(self):
        """
        DESCRIPTION: Verify 'Show'/'Hide' button
        EXPECTED: * 'Show'/'Hide' button is located within the 'Password' field
        EXPECTED: * 'Show' inscription is displayed by default
        """
        pass

    def test_005_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'Continue' button
        EXPECTED: * Button is located at the bottom of the page
        EXPECTED: * Button is disabled and not clickable until 'Password' field is filled in
        """
        pass

    def test_006_verify_cancel_button(self):
        """
        DESCRIPTION: Verify 'Cancel' button
        EXPECTED: * Button is located below 'Continue' button
        EXPECTED: * Button is active and clickable
        """
        pass
