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
class Test_C44870159_Forgot_username_functionality(Common):
    """
    TR_ID: C44870159
    NAME: Forgot username functionality
    DESCRIPTION: 
    PRECONDITIONS: Verify forgot username functionality
    """
    keep_browser_open = True

    def test_001_tapclick_log_in_button(self):
        """
        DESCRIPTION: Tap/click 'Log In' button
        EXPECTED: 'Log in' pop-up appears
        """
        pass

    def test_002_tapclick_forgot_password_link(self):
        """
        DESCRIPTION: Tap/click 'Forgot password?' link
        EXPECTED: 'Reset Password' page is opened
        """
        pass

    def test_003_type_username_in_username_fieldtype_email_in__email_field(self):
        """
        DESCRIPTION: Type username in 'Username' field
        DESCRIPTION: Type email in  'Email' field
        EXPECTED: 
        """
        pass

    def test_004_clicktap_reset_password_button(self):
        """
        DESCRIPTION: Click/Tap 'Reset Password' button
        EXPECTED: Fields' values are validated (if validation is not successful - incorrect fields are highlighted in red)
        EXPECTED: User is redirected to Home Page and 'Success' pop-up appears with 'A new password has been sent to your registered email address. Please remember to check your Spam/Junk folder.' message
        """
        pass

    def test_005_check_email_box(self):
        """
        DESCRIPTION: Check email box
        EXPECTED: Email from Coral is received. New password is provided in email.
        """
        pass

    def test_006_log_in_to_application_using_old_password(self):
        """
        DESCRIPTION: Log in to application using old password
        EXPECTED: Login is not successfull
        """
        pass

    def test_007_log_in_to_application_using_new_temporary_password_from_email(self):
        """
        DESCRIPTION: Log in to application using new temporary password from email
        EXPECTED: 'Change password' appears immediately.
        EXPECTED: User is not able to be logged in while he does not change his temporary password
        """
        pass

    def test_008_enter_temporary_password_into_old_password_fieldenter_new_passwordenter_confirm_new_password(self):
        """
        DESCRIPTION: Enter temporary password into 'Old password' field
        DESCRIPTION: Enter 'New password'
        DESCRIPTION: Enter 'Confirm new password'
        EXPECTED: 
        """
        pass

    def test_009_clicktap_change_password_button(self):
        """
        DESCRIPTION: Click/Tap 'Change Password' button
        EXPECTED: User is successfully logged in
        """
        pass
