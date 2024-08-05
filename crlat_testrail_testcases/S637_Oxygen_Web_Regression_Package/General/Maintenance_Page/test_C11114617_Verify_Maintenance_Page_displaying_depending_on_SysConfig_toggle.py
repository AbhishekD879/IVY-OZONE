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
class Test_C11114617_Verify_Maintenance_Page_displaying_depending_on_SysConfig_toggle(Common):
    """
    TR_ID: C11114617
    NAME: Verify Maintenance Page displaying depending on SysConfig toggle
    DESCRIPTION: This test case verifies Maintenance Page displaying depending on SysConfig toggle
    PRECONDITIONS: CMS > System configuration > Config > maintenancePage > enabled = true
    PRECONDITIONS: Maintenance Page is configured and enabled in CMS
    """
    keep_browser_open = True

    def test_001__load_app_verify_the_cms_initial_data_response(self):
        """
        DESCRIPTION: * Load app
        DESCRIPTION: * Verify the CMS initial data response
        EXPECTED: * App is loaded
        EXPECTED: * CMS initial data response contains sysConfig - maintenancePage > enabled = true
        """
        pass

    def test_002_verify_cms_maintenance_page_call(self):
        """
        DESCRIPTION: Verify CMS maintenance-page call
        EXPECTED: * CMS maintenance-page call is executed
        EXPECTED: * CMS maintenance-page response contains data set up in CMS
        """
        pass

    def test_003__go_to_cms__system_configuration__config__maintenancepage_set_the_config_to_enabled__false(self):
        """
        DESCRIPTION: * Go to CMS > System configuration > Config > maintenancePage
        DESCRIPTION: * Set the config to enabled = false
        EXPECTED: CMS config is successfully saved
        """
        pass

    def test_004__reload_the_app_verify_the_cms_initial_data_response(self):
        """
        DESCRIPTION: * Reload the app
        DESCRIPTION: * Verify the CMS initial data response
        EXPECTED: * App is reloaded
        EXPECTED: * CMS initial data response contains sysConfig - maintenancePage > enabled = false
        """
        pass

    def test_005_verify_cms_maintenance_page_call(self):
        """
        DESCRIPTION: Verify CMS maintenance-page call
        EXPECTED: * CMS maintenance-page call is NOT executed
        """
        pass
