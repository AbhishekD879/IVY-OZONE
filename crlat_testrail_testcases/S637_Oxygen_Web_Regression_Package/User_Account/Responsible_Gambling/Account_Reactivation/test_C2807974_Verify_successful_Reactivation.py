import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C2807974_Verify_successful_Reactivation(Common):
    """
    TR_ID: C2807974
    NAME: Verify successful Reactivation
    DESCRIPTION: This test case verifies successful Reactivation pop up
    DESCRIPTION: AUTOTEST [C7165593]
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag 'Account_Closed_By_Player' is set to 'True' for a user in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set for a user in IMS
    PRECONDITIONS: * 'Reactivation' Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    PRECONDITIONS: * User is logged
    PRECONDITIONS: * Reactivation' page is opened
    PRECONDITIONS: Design -> Reactivation -> https://app.zeplin.io/project/5bf56b032790467ebfb30d0f/dashboard
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

    def test_002_verify_the_pop_up_content(self):
        """
        DESCRIPTION: Verify the pop up content
        EXPECTED: Successful Reactivation pop up consists of:
        EXPECTED: * Message: 'Your account has been successfully reactivated.'
        EXPECTED: * 'OK' button active by default
        """
        pass

    def test_003__navigate_to_dev_tools___ws_verfiy_websocket_setplayertagsrequest_35544(self):
        """
        DESCRIPTION: * Navigate to Dev Tools -> WS
        DESCRIPTION: * Verfiy Websocket SetPlayerTagsRequest (35544)
        EXPECTED: 'Account_Closed_By_Player' is set to 'False'
        """
        pass

    def test_004_clicktap_ok(self):
        """
        DESCRIPTION: Click/tap 'OK'
        EXPECTED: * Pop up is closed
        EXPECTED: * User remains logged in and navigated to home page
        """
        pass
