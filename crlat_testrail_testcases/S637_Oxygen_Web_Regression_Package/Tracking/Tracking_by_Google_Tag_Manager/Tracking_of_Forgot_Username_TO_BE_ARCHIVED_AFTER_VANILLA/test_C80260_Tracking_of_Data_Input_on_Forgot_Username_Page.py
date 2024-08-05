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
class Test_C80260_Tracking_of_Data_Input_on_Forgot_Username_Page(Common):
    """
    TR_ID: C80260
    NAME: Tracking of Data Input on Forgot Username Page
    DESCRIPTION: This test case verify tracking of data input on 'Forgot username' page
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

    def test_004_enter_valid_email_in_email_field(self):
        """
        DESCRIPTION: Enter valid email in 'Email' field
        EXPECTED: 'Email' field is filled with data
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_open_the_last_object(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and open the last object
        EXPECTED: Next parameters are displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'forgotten username',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : 'Email' }
        EXPECTED: );
        """
        pass

    def test_006_choose_day_from_day_dropdown(self):
        """
        DESCRIPTION: Choose day from 'Day' dropdown
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps #5
        EXPECTED: Next parameters are displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'forgotten username',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : 'Day' }
        EXPECTED: );
        """
        pass

    def test_008_choose_month_from_month_dropdown(self):
        """
        DESCRIPTION: Choose month from 'Month' dropdown
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps #5
        EXPECTED: Next parameters are displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'forgotten username',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : 'Month' }
        EXPECTED: );
        """
        pass

    def test_010_choose_year_from_year_dropdown(self):
        """
        DESCRIPTION: Choose year from 'Year' dropdown
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps #5
        EXPECTED: Next parameters are displayed:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'forgotten username',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : 'Year' }
        EXPECTED: );
        """
        pass
