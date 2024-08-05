import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.safari
@vtest
class Test_C_Verify_getting_system_configuration(Common):
    """
    NAME: Verify getting CMS system configuration
    """
    keep_browser_open = True

    def test_001_does_system_configuration_exist(self):
        """
        DESCRIPTION: Check System Configuration Exist
        EXPECTED: System Configuration does Exist
        """
        cfg = self.cms_config.does_system_configuration_exist(device_type='mobile')
        self.assertTrue(cfg, msg='Cannot get system configuration from server')
