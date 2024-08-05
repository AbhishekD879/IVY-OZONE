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
class Test_C81543_Tracking_of_Forgot_Username_page_view(Common):
    """
    TR_ID: C81543
    NAME: Tracking of Forgot Username page view
    DESCRIPTION: This test case verify tracking of Forgot Username page view
    PRECONDITIONS: 1. Open console
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

    def test_005_click_forgot_username_button(self):
        """
        DESCRIPTION: Click 'Forgot username?' button
        EXPECTED: - User is navigated to Homegape
        EXPECTED: - Pop-up with confirmation is displayed to user
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and open the last object
        EXPECTED: Next parameters are displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/forgot-username/submit' }
        EXPECTED: );
        """
        pass
