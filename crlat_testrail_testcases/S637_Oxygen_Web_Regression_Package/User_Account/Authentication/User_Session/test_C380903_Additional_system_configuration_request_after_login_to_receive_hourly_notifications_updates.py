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
class Test_C380903_Additional_system_configuration_request_after_login_to_receive_hourly_notifications_updates(Common):
    """
    TR_ID: C380903
    NAME: Additional 'system-configuration' request after login to receive hourly notifications updates
    DESCRIPTION: This test case verifies that additional request to receive system configs JSON data with hourly notifications configuration updates is sent:
    DESCRIPTION: * every time a user logs in
    DESCRIPTION: * after restoring internet connection/returning from sleep mode/background
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * 'hourlyAlerts' is enabled in CMS -> System-configuration -> LCCP
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To trigger 'reload components':
    PRECONDITIONS: * move/return device from sleep mode;
    PRECONDITIONS: * move to background/return to foreground;
    PRECONDITIONS: * lose/restore internet connection
    """
    keep_browser_open = True

    def test_001_log_in_to_oxygen_application(self):
        """
        DESCRIPTION: Log in to Oxygen application
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'hourlyAlerts' : "enabled" in 'system-configuration' response -> LCCP
        """
        pass

    def test_002_wait_1_hour(self):
        """
        DESCRIPTION: Wait 1 hour
        EXPECTED: Hourly notification pop up is displayed
        """
        pass

    def test_003_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: User is logged out
        """
        pass

    def test_004_in_cms___system_configuration___lccp_disable_hourlyalerts(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> LCCP disable 'hourlyAlerts'
        EXPECTED: Changes are saved
        """
        pass

    def test_005_log_in_to_oxygen_application(self):
        """
        DESCRIPTION: Log in to Oxygen application
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'hourlyAlerts' : "disabled" in 'system-configuration' response -> LCCP
        """
        pass

    def test_006_wait_1_hour(self):
        """
        DESCRIPTION: Wait 1 hour
        EXPECTED: Hourly notification pop up is NOT displayed
        """
        pass

    def test_007_move_device_to_sleep_mode(self):
        """
        DESCRIPTION: Move device to sleep mode
        EXPECTED: 
        """
        pass

    def test_008_in_cms___system_configuration___lccp_enable_hourlyalerts(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> LCCP enable 'hourlyAlerts'
        EXPECTED: Changes are saved
        """
        pass

    def test_009_unlock_deviceverify_console_and_network_tabs(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify Console and Network tabs
        EXPECTED: * 'reload components' is displayed Console
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'hourlyAlerts' : "enabled" in 'system-configuration' response -> LCCP
        """
        pass

    def test_010_wait_near_1_hour_depends_on_time_when_device_was_locked_after_login(self):
        """
        DESCRIPTION: Wait near 1 hour (depends on time when device was locked after login)
        EXPECTED: Hourly notification pop up is displayed
        """
        pass

    def test_011_lose_internet_connection(self):
        """
        DESCRIPTION: Lose internet connection
        EXPECTED: 
        """
        pass

    def test_012_in_cms___system_configuration___lccp_disable_hourlyalerts(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> LCCP disable 'hourlyAlerts'
        EXPECTED: Changes are saved
        """
        pass

    def test_013_restore_internet_connection(self):
        """
        DESCRIPTION: Restore internet connection
        EXPECTED: * 'reload components' is displayed Console
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'hourlyAlerts' : "disabled" in 'system-configuration' response -> LCCP
        """
        pass

    def test_014_wait_near_1_hour_depends_on_time_when_internet_connection_was_lost_after_login(self):
        """
        DESCRIPTION: Wait near 1 hour (depends on time when internet connection was lost after login)
        EXPECTED: Hourly notification pop up is NOT displayed
        """
        pass

    def test_015_move_app_to_background(self):
        """
        DESCRIPTION: Move app to background
        EXPECTED: 
        """
        pass

    def test_016_in_cms___system_configuration___lccp_enable_hourlyalerts(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> LCCP enable 'hourlyAlerts'
        EXPECTED: Changes are saved
        """
        pass

    def test_017_move_app_to_foreground(self):
        """
        DESCRIPTION: Move app to foreground
        EXPECTED: * 'reload components' is displayed Console
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'hourlyAlerts' : "enabled" in 'system-configuration' response -> LCCP
        """
        pass

    def test_018_wait_near_1_hour_depends_on_time_when_internet_connection_was_lost_after_login(self):
        """
        DESCRIPTION: Wait near 1 hour (depends on time when internet connection was lost after login)
        EXPECTED: Hourly notification pop up is displayed
        """
        pass
