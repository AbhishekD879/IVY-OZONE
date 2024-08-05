import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C373930_Additional_system_configuration_request_to_receive_ACCA_notifications_updates(Common):
    """
    TR_ID: C373930
    NAME: Additional 'system-configuration' request to receive ACCA notifications updates
    DESCRIPTION: This test case verifies that additional request to receive system configs JSON data from Akamai is sent:
    DESCRIPTION: * before the betslip is opened;
    DESCRIPTION: * after restoring internet connection/returning from sleep mode/background
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * User is logged in to Oxygen application
    PRECONDITIONS: * At least 3 selection are added to betslip
    PRECONDITIONS: * 'superAcca' is enabled in CMS -> System-configuration -> BETSLIP
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To trigger 'reload components':
    PRECONDITIONS: * move/return device from sleep mode;
    PRECONDITIONS: * move to background/return to foreground;
    PRECONDITIONS: * lose/restore internet connection
    """
    keep_browser_open = True

    def test_001_in_oxygen_application_navigate_to_betslip(self):
        """
        DESCRIPTION: In Oxygen application navigate to betslip
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'superAcca : true' in 'system-configuration' response -> Betslip (type 'initial' in XHR Filter field)
        EXPECTED: * ACCA notification is displayed on betslip
        """
        pass

    def test_002_on_mobile_close_betslipon_tabletdesktop_navigate_to_another_tab_within_betslip_widget(self):
        """
        DESCRIPTION: On Mobile close Betslip;
        DESCRIPTION: On Tablet/Desktop navigate to another tab within Betslip widget
        EXPECTED: 
        """
        pass

    def test_003_in_cms___system_configuration___betslip_disable_superacca(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> BETSLIP disable 'superAcca'
        EXPECTED: Changes are saved
        """
        pass

    def test_004_in_oxygen_application_navigate_to_betslip(self):
        """
        DESCRIPTION: In Oxygen application navigate to betslip
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'superAcca : false' in 'system-configuration' response -> Betslip (type 'initial' in XHR Filter field)
        EXPECTED: * ACCA notification is NOT displayed on betslip
        """
        pass

    def test_005_move_device_to_sleep_mode(self):
        """
        DESCRIPTION: Move device to sleep mode
        EXPECTED: 
        """
        pass

    def test_006_in_cms___system_configuration___betslip_enable_superacca(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> BETSLIP enable 'superAcca'
        EXPECTED: Changes are saved
        """
        pass

    def test_007_unlock_deviceverify_console_and_network_tabs(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify Console and Network tabs
        EXPECTED: * 'reload components' is displayed Console
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'superAcca : true' in 'system-configuration' response -> Betslip (type 'initial' in XHR Filter field)
        """
        pass

    def test_008_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: * Betslip content is reloaded
        EXPECTED: * ACCA notification is displayed on betslip
        """
        pass

    def test_009_lose_internet_connection(self):
        """
        DESCRIPTION: Lose internet connection
        EXPECTED: 
        """
        pass

    def test_010_in_cms___system_configuration___betslip_disable_superacca(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> BETSLIP disable 'superAcca'
        EXPECTED: Changes are saved
        """
        pass

    def test_011_restore_internet_connection(self):
        """
        DESCRIPTION: Restore internet connection
        EXPECTED: * 'reload components' is displayed Console
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'superAcca : false' in 'system-configuration' response -> Betslip (type 'initial' in XHR Filter field)
        """
        pass

    def test_012_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: * Betslip content is reloaded
        EXPECTED: * ACCA notification is NOT displayed on betslip
        """
        pass

    def test_013_move_app_to_background(self):
        """
        DESCRIPTION: Move app to background
        EXPECTED: 
        """
        pass

    def test_014_in_cms___system_configuration___betslip_enable_superacca(self):
        """
        DESCRIPTION: In CMS -> System-configuration -> BETSLIP enable 'superAcca'
        EXPECTED: Changes are saved
        """
        pass

    def test_015_move_app_to_foreground(self):
        """
        DESCRIPTION: Move app to foreground
        EXPECTED: * 'reload components' is displayed Console
        EXPECTED: * 'system-configuration' request is sent
        EXPECTED: * 'superAcca : true' in 'system-configuration' response -> Betslip (type 'initial' in XHR Filter field)
        """
        pass

    def test_016_verify_betslip(self):
        """
        DESCRIPTION: Verify betslip
        EXPECTED: * Betslip content is reloaded
        EXPECTED: * ACCA notification is displayed on betslip
        """
        pass
