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
class Test_C16268988_Vanilla_Verify_Betsip_on_both_devices_while_multiple_log_in(Common):
    """
    TR_ID: C16268988
    NAME: [Vanilla] Verify Betsip on both devices while multiple log in
    DESCRIPTION: This test case verifies Betslip on both devices while multiple log in.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_multiple_log_in_from_multiple_devices(self):
        """
        DESCRIPTION: Make multiple log in from multiple devices
        EXPECTED: User is logged in from multiple devices
        """
        pass

    def test_002_make_empty_betslip_on_both_devices(self):
        """
        DESCRIPTION: Make empty Betslip on both devices
        EXPECTED: - Betslip is empty
        EXPECTED: - Betslip counter shows 0
        """
        pass

    def test_003_add_at_least_1_selection_to_betslip_on_device_1(self):
        """
        DESCRIPTION: Add at least 1 selection to Betslip on Device 1
        EXPECTED: Selection is added to Betslip on Device 1
        """
        pass

    def test_004_check_the_betslip_on_device_2(self):
        """
        DESCRIPTION: Check the Betslip on Device 2
        EXPECTED: - Betslip is empty on Device 2
        EXPECTED: - Betslip counter shows 0
        """
        pass

    def test_005_add_at_least_1_selection_to_betslip_on_device_2(self):
        """
        DESCRIPTION: Add at least 1 selection to Betslip on Device 2
        EXPECTED: Selection is added to Betslip on Device 2
        """
        pass

    def test_006_check_the_betslip_on_device_1(self):
        """
        DESCRIPTION: Check the Betslip on Device 1
        EXPECTED: - 1 selection stays in the Betslip (from step 3)
        EXPECTED: - Betslip counter shows 1
        """
        pass

    def test_007_reload_the_app_via_browser_refresh_button_on_both_devices(self):
        """
        DESCRIPTION: Reload the app via browser refresh button on both devices
        EXPECTED: Betslip should NOT be synchronized on both devices
        """
        pass

    def test_008_make_empty_betslip_on_both_devices(self):
        """
        DESCRIPTION: Make empty Betslip on both devices
        EXPECTED: 
        """
        pass

    def test_009_add_the_same_at_least_2_selections_to_betslip_on_both_devices(self):
        """
        DESCRIPTION: Add the same, at least 2 selections, to Betslip on both devices
        EXPECTED: Selections are added to Betslip on both devices
        """
        pass

    def test_010_reload_the_app_via_browser_refresh_button_on_both_devices(self):
        """
        DESCRIPTION: Reload the app via browser refresh button on both devices
        EXPECTED: - Betslip should NOT be synchronized on both devices
        EXPECTED: - There are no duplicates
        """
        pass

    def test_011_delete_1_selection_from_betslip_on_device_1(self):
        """
        DESCRIPTION: Delete 1 selection from Betslip on Device 1
        EXPECTED: Selection is removed from Betslip
        """
        pass

    def test_012_check_the_betslip_on_device_2(self):
        """
        DESCRIPTION: Check the Betslip on Device 2
        EXPECTED: - Betslip should NOT be synchronized on both devices
        EXPECTED: - 2 selections still present on Betslip
        """
        pass
