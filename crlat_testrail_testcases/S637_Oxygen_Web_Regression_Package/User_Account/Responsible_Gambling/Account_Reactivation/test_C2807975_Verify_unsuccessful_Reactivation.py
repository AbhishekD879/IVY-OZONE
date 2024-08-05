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
class Test_C2807975_Verify_unsuccessful_Reactivation(Common):
    """
    TR_ID: C2807975
    NAME: Verify unsuccessful Reactivation
    DESCRIPTION: This test case verifies unsuccessful Reactivation message
    DESCRIPTION: AUTOTEST [C9272857]
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag 'Account_Closed_By_Player' is set to 'True' for a user in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set for a user in IMS
    PRECONDITIONS: * 'Reactivation' Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'Reactivation' page is opened
    PRECONDITIONS: Design -> Reactivation -> https://app.zeplin.io/project/5bf56b032790467ebfb30d0f/dashboard
    """
    keep_browser_open = True

    def test_001__enter_incorrect_password_in_password_field_clicktap_confirm_button(self):
        """
        DESCRIPTION: * Enter incorrect password in 'Password' field
        DESCRIPTION: * Click/tap 'CONFIRM' button
        EXPECTED: * Incorrect password message is displayed below to 'Password' field in red color:
        EXPECTED: 'Your password is invalid. Please try again'
        EXPECTED: (See pasapi response in Network > Doc)
        """
        pass

    def test_002_clicktap_confirm_button_again(self):
        """
        DESCRIPTION: Click/tap 'CONFIRM' button again
        EXPECTED: * Incorrect password message is displayed below to 'Password' field in red color:
        EXPECTED: 'Your password is invalid. Please try again'
        EXPECTED: OR
        EXPECTED: ‘Oops, Something went wrong, please try again or call our customer support at 0800 731 6191 to reopen your account’
        EXPECTED: (Depending on pasapi response see Network > Doc)
        EXPECTED: * In openapi WS response:"Account_Closed_By_Player"="False"
        """
        pass
