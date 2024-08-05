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
class Test_C647970_Re_establishing_connection_to_OpenAPI_after_inactivity_period(Common):
    """
    TR_ID: C647970
    NAME: Re-establishing connection to OpenAPI after inactivity period
    DESCRIPTION: This test case verifies re-establishing connection to OpenAPI when user brings a browser/app from the background or after a period of sleep
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: ------
    PRECONDITIONS: *TC needs to be updated!*
    PRECONDITIONS: expected results in Steps 2 and 5 seems to be outdated.
    PRECONDITIONS: There is no 'reload components' in console, nor new windowSession (ID: 31127) ws call to OpenApi. WS connection to OpenApi remains the same, app behaves as expected, no need to establish new connection or make new IMS calls.
    PRECONDITIONS: In the flows with Internet connection lost (Steps 11-14) there is always 'reload components' message displayed in console and New connection to OpenAPI is established (regardless if internet connection lost was <1 or >1 minute).
    """
    keep_browser_open = True

    def test_001_lock_device_for_less_than_1_minuteunlock_device(self):
        """
        DESCRIPTION: Lock device for less than 1 minute
        DESCRIPTION: Unlock device
        EXPECTED: * if user data is still in cookies app user is still logged in
        EXPECTED: * if user data is no longer available in cookies app user is logged out
        """
        pass

    def test_002_verify_console(self):
        """
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * connection to OpenAPI is re-established, the same OpenAPI connection is used
        EXPECTED: * old windowSession (ID: 31130) is closed and new windowSession (ID: 31127) is opened within the same OpenAPI connection
        """
        pass

    def test_003_make_several_openapi_related_user_actions_deposit_withdrawal_change_password_navigate_to_transaction_history_change_session_and_deposit_limits_etc(self):
        """
        DESCRIPTION: Make several OpenAPI related user actions: deposit, withdrawal, change password, navigate to transaction history, change session and deposit limits etc.)
        EXPECTED: All actions are successfully completed
        """
        pass

    def test_004_lock_device_for_more_than_1_minuteunlock_device(self):
        """
        DESCRIPTION: Lock device for more than 1 minute
        DESCRIPTION: Unlock device
        EXPECTED: * if user data is still in cookies app user is still logged in
        EXPECTED: * if user data is no longer available in cookies app user is logged out
        """
        pass

    def test_005_verify_console(self):
        """
        DESCRIPTION: Verify console
        EXPECTED: * 'reload components' in console
        EXPECTED: * connection to OpenAPI is re-established, one new OpenAPI connection is created with new windowSession (ID: 31127) opened within it
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        EXPECTED: 
        """
        pass

    def test_007_move_app_to_background_for_less_than_1_minutemove_app_to_foreground(self):
        """
        DESCRIPTION: Move app to background for less than 1 minute
        DESCRIPTION: Move app to foreground
        EXPECTED: * if user data is still in cookies app user is still logged in
        EXPECTED: * if user data is no longer available in cookies app user is logged out
        """
        pass

    def test_008_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_009_move_app_to_background_for_more_than_1_minutemove_app_to_foreground(self):
        """
        DESCRIPTION: Move app to background for more than 1 minute
        DESCRIPTION: Move app to foreground
        EXPECTED: * if user data is still in cookies app user is still logged in
        EXPECTED: * if user data is no longer available in cookies app user is logged out
        """
        pass

    def test_010_repeat_steps_53(self):
        """
        DESCRIPTION: Repeat steps #5,3
        EXPECTED: 
        """
        pass

    def test_011_make_device_lose_internet_connection_for_less_than_1_minuterestore_internet_connection(self):
        """
        DESCRIPTION: Make device lose internet connection for less than 1 minute
        DESCRIPTION: Restore internet connection
        EXPECTED: * if user data is still in cookies app user is still logged in
        EXPECTED: * if user data is no longer available in cookies app user is logged out
        """
        pass

    def test_012_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass

    def test_013_make_device_lose_internet_connection_for_more_than_1_minuterestore_internet_connection(self):
        """
        DESCRIPTION: Make device lose internet connection for more than 1 minute
        DESCRIPTION: Restore internet connection
        EXPECTED: * if user data is still in cookies app user is still logged in
        EXPECTED: * if user data is no longer available in cookies app user is logged out
        """
        pass

    def test_014_repeat_steps_53(self):
        """
        DESCRIPTION: Repeat steps #5,3
        EXPECTED: 
        """
        pass
