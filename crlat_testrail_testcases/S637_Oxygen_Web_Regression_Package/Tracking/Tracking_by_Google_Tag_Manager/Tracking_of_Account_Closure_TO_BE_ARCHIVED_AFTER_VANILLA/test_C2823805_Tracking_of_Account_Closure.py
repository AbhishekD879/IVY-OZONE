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
class Test_C2823805_Tracking_of_Account_Closure(Common):
    """
    TR_ID: C2823805
    NAME: Tracking of Account Closure
    DESCRIPTION: 
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * Select any option from 'Closure Reason' drop-down and click/tap 'CONTINUE' button on Account Closure step 1 page
    PRECONDITIONS: * Enter valid password in 'Password' field on Account Closure step 2 page
    PRECONDITIONS: * To check GA pushes open DevTools -> Console tab
    """
    keep_browser_open = True

    def test_001_clicktap_continue_button_on_account_closure_step_2_page(self):
        """
        DESCRIPTION: Click/tap 'CONTINUE' button on Account Closure step 2 page
        EXPECTED: "Confirmation pop-up Account Closure" is shown
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/gambling-controls/account-closure/confirm' }
        EXPECTED: );
        """
        pass

    def test_003_clicktap_cancel_button(self):
        """
        DESCRIPTION: Click/tap 'CANCEL' button
        EXPECTED: * "Confirmation of Account Closure" pop-up is closed
        EXPECTED: * User stays on Account Closure step 2 page
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'account closure',
        EXPECTED: 'eventAction' : 'cancel',
        EXPECTED: 'eventLabel : ' 'confirm'
        EXPECTED: };
        """
        pass

    def test_005_enter_a_valid_password_into_password_field_and_clicktap_continue_button(self):
        """
        DESCRIPTION: Enter a valid password into "Password" field and click/tap 'CONTINUE' button
        EXPECTED: "Confirmation pop-up Account Closure" is shown again
        """
        pass

    def test_006_tick_the_checkbox_and_clicktap_yes_button(self):
        """
        DESCRIPTION: Tick the checkbox and click/tap 'YES' button
        EXPECTED: * 'Your Account is now closed' pop-up is displayed
        EXPECTED: * User`s account is closed
        EXPECTED: * User is logged out
        """
        pass

    def test_007_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'page' : '/gambling-controls/account-closure/success' }
        EXPECTED: );
        """
        pass
