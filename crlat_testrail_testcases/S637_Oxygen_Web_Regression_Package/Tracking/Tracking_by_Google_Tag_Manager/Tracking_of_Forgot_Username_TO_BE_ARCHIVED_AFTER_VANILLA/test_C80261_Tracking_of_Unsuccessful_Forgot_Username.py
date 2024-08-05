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
class Test_C80261_Tracking_of_Unsuccessful_Forgot_Username(Common):
    """
    TR_ID: C80261
    NAME: Tracking of Unsuccessful Forgot Username
    DESCRIPTION: This test case verify tracking of unsuccessful forgot username journey
    PRECONDITIONS: 1. Open console
    PRECONDITIONS: 2. To see responce open Dev tools -> Network -> WS -> Frames -> choose last item
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

    def test_003_click_forgot_username_link(self):
        """
        DESCRIPTION: Click 'Forgot username?' link
        EXPECTED: 'Forgot username' page is opened
        """
        pass

    def test_004_enter_valid_email_in_email_field_and_choose_date_from_date_of_birth_dropdowns(self):
        """
        DESCRIPTION: Enter valid email in 'Email' field and choose date from 'Date of Birth' dropdowns
        EXPECTED: 'Email' field and 'Date of Birth' dropdowns are filled with valid data
        """
        pass

    def test_005_trigger_an_error_during_submission_of_forgot_username_form(self):
        """
        DESCRIPTION: Trigger an error during submission of 'Forgot username' form
        EXPECTED: 
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
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

    def test_007_verify_static_parameters_in_response(self):
        """
        DESCRIPTION: Verify static parameters in response
        EXPECTED: The next parameters are static and not changeable for all 'dataLayer' objects for failed submission of 'Forgot username' form:
        EXPECTED: - 'event' : ''trackEvent''
        EXPECTED: - 'eventCategory' : ''forgotten username''
        EXPECTED: - 'eventAction' : ''submission''
        EXPECTED: - 'eventLabel' : ''failure''
        """
        pass

    def test_008_verify_parameter_errorcode(self):
        """
        DESCRIPTION: Verify parameter 'errorCode'
        EXPECTED: - 'errorCode' parameter corresponds to *error code* attribute from response
        EXPECTED: - 'errorCode' parameter is displayed in lower case and without underscore
        """
        pass

    def test_009_verify_parameter_errormessage(self):
        """
        DESCRIPTION: Verify parameter 'errorMessage'
        EXPECTED: - 'errorMessage' parameter is equal to error message presented to user
        EXPECTED: - 'errorMessage' parameter is displayed in lower case and without underscore
        """
        pass
