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
class Test_C2745710_STG2HLVerify_Time_Out_Password_page(Common):
    """
    TR_ID: C2745710
    NAME: [STG2][HL]Verify 'Time-Out Password' page
    DESCRIPTION: This test case verifies 'Time-Out Password' page
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

    def test_001_verify_time_out_password_page(self):
        """
        DESCRIPTION: Verify 'Time-Out Password' page
        EXPECTED: * 'Password' placeholder is displayed within the field by default
        EXPECTED: * 'Continue' button is disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_002_verify_time_out_expiration_date(self):
        """
        DESCRIPTION: Verify Time-Out expiration date
        EXPECTED: Time-Out expiration date is based on values set by the user on previous 'Time-Out' page
        """
        pass

    def test_003_start_entering_the_correct_password_in_the_password_field(self):
        """
        DESCRIPTION: Start entering the correct password in the 'Password' field
        EXPECTED: * 'Password' placeholder is replaced by entered characters
        EXPECTED: * 'Continue' button becomes enabled/active
        """
        pass

    def test_004_clicktap_on_show_button(self):
        """
        DESCRIPTION: Click/Tap on 'Show' button
        EXPECTED: * 'Hide' button is replaced by 'Show' button
        EXPECTED: * Characters within the 'Password' field becomes visible
        """
        pass

    def test_005_clicktap_on_hide_button(self):
        """
        DESCRIPTION: Click/Tap on 'Hide' button
        EXPECTED: * 'Hide' button is replaced by 'Show' button
        EXPECTED: * Characters within the 'Password' field becomes hidden again
        """
        pass

    def test_006_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: 'Confirmation of Time-Out' pop-up appears
        """
        pass
