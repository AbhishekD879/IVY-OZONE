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
class Test_C2854902_Tracking_of_successful_Account_Reactivation_journey(Common):
    """
    TR_ID: C2854902
    NAME: Tracking of successful Account Reactivation journey
    DESCRIPTION: This test case verifies tracking of successful Account Reactivation journey
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag - 'Account_Closed_By_Player' is set to 'True' in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set for a user in IMS
    PRECONDITIONS: * “Reactivation” Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The on login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'Reactivation' page is opened
    """
    keep_browser_open = True

    def test_001__enter_valid_password_in_password_field_clicktap_confirm_button(self):
        """
        DESCRIPTION: * Enter valid password in 'Password' field
        DESCRIPTION: * Click/tap 'CONFIRM' button
        EXPECTED: * 'Accout Reactivation' confirmation pop-up is shown
        EXPECTED: * User remains logged in
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackPageview', 'page' : '/gambling-controls/account-reactivation/success' }
        EXPECTED: );
        """
        pass
