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
class Test_C147398_Verify_errors_recived_from_Open_API_displaying_in_console(Common):
    """
    TR_ID: C147398
    NAME: Verify errors recived from Open API displaying in console
    DESCRIPTION: This test case verifies that errors received from Open API are displayed in console
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Open Development Tool -> Network -> WS
    PRECONDITIONS: Link to view all the possible success and failure (with errors) responses received from Open API:
    PRECONDITIONS: https://jira.egalacoral.com/secure/attachment/588911/openapi%20id%20config.txt
    """
    keep_browser_open = True

    def test_001_login_in_oxygen_app_with_incorrect_credentials(self):
        """
        DESCRIPTION: Login in Oxygen app with incorrect credentials
        EXPECTED: * Error is displayed to user. User is not logged in
        EXPECTED: * Request 31001 is sent
        """
        pass

    def test_002_open_31009_response_in_ws(self):
        """
        DESCRIPTION: Open 31009 response in WS
        EXPECTED: Next information is displayed with set values:
        EXPECTED: * errorCode ( if exists)
        EXPECTED: * errorMessage
        """
        pass

    def test_003_switch_to_console_and_check_error_displaying(self):
        """
        DESCRIPTION: Switch to Console and check error displaying
        EXPECTED: * **Request description** describes the error: 'Error during 'description'. (have a look on link in Preconditions)
        EXPECTED: * **Request id** equals id of request and is shown in brackets
        EXPECTED: * **id** equals response id
        EXPECTED: * **ErrorMessage, ErrorCode** values equal to values in response from the previous step
        EXPECTED: ![](index.php?/attachments/get/1654)
        """
        pass

    def test_004_open_forgotten_password_pageand_confirm_resetting_password_with_invalid_data(self):
        """
        DESCRIPTION: Open Forgotten Password page,and confirm resetting password with invalid data
        EXPECTED: * Error is shown to user and password is not reset
        EXPECTED: * Request 31058 is sent
        """
        pass

    def test_005_repeat_steps__2_3_but_for_31060_response_in_ws(self):
        """
        DESCRIPTION: Repeat steps # 2-3, but for 31060 response in WS
        EXPECTED: 
        """
        pass

    def test_006_open_forgotten_username_page_and_confirm_username_reminding_with_invalid_data(self):
        """
        DESCRIPTION: Open Forgotten Username page and confirm username reminding with invalid data
        EXPECTED: * Error is shown to user and new username is not sent to email
        EXPECTED: * Request  35520  is sent
        """
        pass

    def test_007_repeat_steps__2_3_but_for_35522_response_in_ws(self):
        """
        DESCRIPTION: Repeat steps # 2-3, but for 35522 response in WS
        EXPECTED: 
        """
        pass

    def test_008_check_the_same_behavior_for_other_errors_from_open_api__have_a_look_on_link_in_preconditions(self):
        """
        DESCRIPTION: Check the same behavior for other errors from Open API ( have a look on link in Preconditions)
        EXPECTED: 
        """
        pass
