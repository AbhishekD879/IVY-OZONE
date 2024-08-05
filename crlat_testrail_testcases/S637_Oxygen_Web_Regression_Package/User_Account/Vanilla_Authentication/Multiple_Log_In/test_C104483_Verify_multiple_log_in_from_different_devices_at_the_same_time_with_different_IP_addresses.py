import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C104483_Verify_multiple_log_in_from_different_devices_at_the_same_time_with_different_IP_addresses(Common):
    """
    TR_ID: C104483
    NAME: Verify multiple log in from different devices at the same time with different IP addresses
    DESCRIPTION: This test case verifies multiple log in from different devices at the same time  with different IP addresses
    PRECONDITIONS: A user should NOT be able to log into their Sportbook account from as multiple devices with the same IP address
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in_from_device_1(self):
        """
        DESCRIPTION: Load Oxygen and log in from Device 1
        EXPECTED: User is logged in
        """
        pass

    def test_002_load_oxygen_and_log_in_the_same_account_from_device_2(self):
        """
        DESCRIPTION: Load Oxygen and log in the same account from Device 2
        EXPECTED: User is logged in
        """
        pass

    def test_003_reload_app_via_browser_refresh_button_and_check_whether_user_stays_logged_in_from_device_1(self):
        """
        DESCRIPTION: Reload app via browser refresh button and check whether User stays logged in from Device 1
        EXPECTED: User is logged out
        """
        pass

    def test_004_navigate_through_the_application_from_device_2(self):
        """
        DESCRIPTION: Navigate through the application from Device 2
        EXPECTED: User stays logged in
        """
        pass

    def test_005_repeat_steps_1_4_when_multiple_log_in_from_same_device_and_different_browser(self):
        """
        DESCRIPTION: Repeat steps 1-4 when multiple log in from same device and different browser
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_7_when_multiple_log_in_from_oxygen_html5_and_oxygen_native_client(self):
        """
        DESCRIPTION: Repeat steps 1-7 when multiple log in from Oxygen HTML5 and Oxygen Native Client
        EXPECTED: 
        """
        pass
