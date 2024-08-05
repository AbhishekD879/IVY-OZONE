import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C12600651_Verify_racingPostEnabled_parameter_in_raceInfo_group_in_CMS(Common):
    """
    TR_ID: C12600651
    NAME: Verify 'racingPostEnabled' parameter in 'raceInfo' group in CMS
    DESCRIPTION: This test case verifies enabling/disabling 'timeFormEnabled' parameter in 'raceInfo' group in CMS
    PRECONDITIONS: 1. Navigate to CMS
    PRECONDITIONS: 2. Go to System Configuration -> Structure
    PRECONDITIONS: 3. Search 'Raceinfo' system config
    """
    keep_browser_open = True

    def test_001_enable_racingpostenabled_check_box_in_system_config_in_cms(self):
        """
        DESCRIPTION: Enable 'racingPostEnabled' check box in System Config in CMS
        EXPECTED: 'racingPostEnabled' check box is enabled
        """
        pass

    def test_002_navigate_to_ghhr_landing_page_in_app(self):
        """
        DESCRIPTION: Navigate to GH/HR landing page in App
        EXPECTED: GH/HR landing page is displayed
        """
        pass

    def test_003_navigate_to_network__gt_mobile__gt_system_configuration_and_verify_that_racingpostenabled_parameter_has_true_value(self):
        """
        DESCRIPTION: Navigate to 'Network' -&gt; 'mobile' -&gt; 'System Configuration' and verify that 'racingPostEnabled' parameter has 'true' value
        EXPECTED: 'racingPostEnabled' parameter has {enabled: true} value
        """
        pass

    def test_004_disable_racingpostenabled_check_box_in_system_config_in_cms(self):
        """
        DESCRIPTION: Disable 'racingPostEnabled' check box in System Config in CMS
        EXPECTED: 'racingPostEnabled' check box is disabled
        """
        pass

    def test_005_reload_ghhr_landing_page_in_app(self):
        """
        DESCRIPTION: Reload GH/HR landing page in App
        EXPECTED: GH/HR landing page is reloaded
        """
        pass

    def test_006_navigate_to_network__gt_mobile__gt_system_configuration_and_verify_that_racingpostenabled_parameter_has_false_value(self):
        """
        DESCRIPTION: Navigate to 'Network' -&gt; 'mobile' -&gt; 'System Configuration' and verify that 'racingPostEnabled' parameter has 'false' value
        EXPECTED: 'racingPostEnabled' has {enabled: false} value
        """
        pass
