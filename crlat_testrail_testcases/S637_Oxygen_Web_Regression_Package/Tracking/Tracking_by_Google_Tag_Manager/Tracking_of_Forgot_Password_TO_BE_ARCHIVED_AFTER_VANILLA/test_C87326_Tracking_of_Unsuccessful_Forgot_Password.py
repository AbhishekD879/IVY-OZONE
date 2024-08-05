import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C87326_Tracking_of_Unsuccessful_Forgot_Password(Common):
    """
    TR_ID: C87326
    NAME: Tracking of Unsuccessful Forgot Password
    DESCRIPTION: This test case verify tracking of unsuccessful forgot password journey
    PRECONDITIONS: 1. Open console
    PRECONDITIONS: 2. To see responce open Dev tools -> Network-> Request 'ForgotPassword.php?casinoname=coraltst2...' -> response
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_click_log_in_button(self):
        """
        DESCRIPTION: Click 'Log in' button
        EXPECTED: 'Log in' pop-up is appeared
        """
        pass

    def test_003_click_forgot_password_link(self):
        """
        DESCRIPTION: Click 'Forgot password?' link
        EXPECTED: 'Forgot password' page is opened
        """
        pass

    def test_004_enter__username_in_username_field_and_choose_email_in_email_field(self):
        """
        DESCRIPTION: Enter  username in 'Username' field and choose email in 'Email' Field
        EXPECTED: 'Username' and 'Email' fields are filled with data
        """
        pass

    def test_005_choose_date_from_date_of_birth_dropdowns(self):
        """
        DESCRIPTION: Choose date from 'Date of Birth' dropdowns
        EXPECTED: 'Date of Birth' dropdowns are filled with data
        """
        pass

    def test_006_trigger_an_error_during_submission_of_forgot_password_form(self):
        """
        DESCRIPTION: Trigger an error during submission of 'Forgot password' form
        EXPECTED: 
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and open the last object
        EXPECTED: The following parameters are present in 'dataLayer' object:
        EXPECTED: - event
        EXPECTED: - eventCategory
        EXPECTED: - eventAction
        EXPECTED: - eventLabel
        EXPECTED: - errorMesage
        EXPECTED: - errorCode
        """
        pass

    def test_008_verify_static_parameters_in_response(self):
        """
        DESCRIPTION: Verify static parameters in response
        EXPECTED: The next parameters are static and not changeable for all 'dataLayer' objects for failed submission of 'Forgot password' form:
        EXPECTED: - 'event' : ''trackEvent''
        EXPECTED: - 'eventCategory' : ''forgotten password''
        EXPECTED: - 'eventAction' : ''submission''
        EXPECTED: - 'eventLabel' : ''failure''
        """
        pass

    def test_009_verify_parameter_errorcode(self):
        """
        DESCRIPTION: Verify parameter 'errorCode'
        EXPECTED: - 'errorCode' parameter corresponds to *error code* attribute from response
        EXPECTED: - 'errorCode' parameter is displayed in lower case and without underscore
        """
        pass

    def test_010_verify_parameter_errormessage(self):
        """
        DESCRIPTION: Verify parameter 'errorMessage'
        EXPECTED: - 'errorMessage' parameter is equal to error message presented to user
        EXPECTED: - 'errorMessage' parameter is displayed in lower case and without underscore
        """
        pass
