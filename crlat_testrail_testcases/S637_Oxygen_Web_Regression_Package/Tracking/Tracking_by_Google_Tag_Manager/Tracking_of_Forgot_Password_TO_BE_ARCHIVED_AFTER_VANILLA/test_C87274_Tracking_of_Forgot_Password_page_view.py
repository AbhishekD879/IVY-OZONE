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
class Test_C87274_Tracking_of_Forgot_Password_page_view(Common):
    """
    TR_ID: C87274
    NAME: Tracking of Forgot Password page view
    DESCRIPTION: This test case verify tracking of Forgot Password page view
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
        EXPECTED: 'Forgot username' page is opened
        """
        pass

    def test_004_enter_valid_username_in_username_field_and_valid_email_in_email_field(self):
        """
        DESCRIPTION: Enter valid username in 'username' field and valid email in 'Email' field
        EXPECTED: 'Username' and 'Email' field  are filled with valid data
        """
        pass

    def test_005_choose_date_from_date_of_birth_dropdowns(self):
        """
        DESCRIPTION: Choose date from 'Date of Birth' dropdowns
        EXPECTED: Date of Birth' dropdowns are filled with valid data
        """
        pass

    def test_006_click_forgot_password_button(self):
        """
        DESCRIPTION: Click 'Forgot password?' button
        EXPECTED: - User is navigated to Homegape
        EXPECTED: - Pop-up with confirmation is displayed to user
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and open the last object
        EXPECTED: Next parameters are displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/forgotten-password/submit' }
        EXPECTED: );
        """
        pass
