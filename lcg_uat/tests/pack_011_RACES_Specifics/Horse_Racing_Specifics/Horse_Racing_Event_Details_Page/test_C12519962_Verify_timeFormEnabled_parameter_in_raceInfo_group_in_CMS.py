import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #timeFormEnabled Disabling is not possible in Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.races
@vtest
class Test_C12519962_Verify_timeFormEnabled_parameter_in_raceInfo_group_in_CMS(Common):
    """
    TR_ID: C12519962
    NAME: Verify 'timeFormEnabled' parameter in 'raceInfo' group in CMS
    DESCRIPTION: This test case verifies enabling/disabling 'timeFormEnabled' parameter in 'raceInfo' group in CMS
    PRECONDITIONS: 1. Navigate to CMS
    PRECONDITIONS: 2. Go to System Configuration -> Structure
    PRECONDITIONS: 3. Search 'Raceinfo' system config
    """
    keep_browser_open = True

    def test_001_enable_timeformenabled_check_box_in_system_config_in_cms(self):
        """
        DESCRIPTION: Enable 'timeFormEnabled' check box in System Config in CMS
        EXPECTED: 'timeFormEnabled' check box is enabled
        """
        self.__class__.status = self.cms_config.get_system_configuration_structure()['raceInfo']['timeFormEnabled']
        self.cms_config.update_system_configuration_structure(config_item='raceInfo',
                                                              field_name='timeFormEnabled', field_value=True)

    def test_002_navigate_to_ghhr_landing_page_in_app(self):
        """
        DESCRIPTION: Navigate to GH/HR landing page in App
        EXPECTED: GH/HR landing page is displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=20),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_003_navigate_to_network___mobile___system_configuration_and_verify_that_timeformenabled_parameter_has_true_value(self):
        """
        DESCRIPTION: Navigate to 'Network' -> 'mobile' -> 'System Configuration' and verify that 'timeFormEnabled' parameter has 'true' value
        EXPECTED: 'timeFormEnabled' has {enabled: true} value
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state_changed()
        self.__class__.raceInfoMobile = self.cms_config.get_initial_data()
        self.assertTrue(self.raceInfoMobile, msg='No raceInfoMobile tag in initial-data response')
        self.assertTrue(self.raceInfoMobile['systemConfiguration']['raceInfo']['timeFormEnabled'],
                        msg=f'"timeFormEnabled parameter in raceInfo is" {self.raceInfoMobile["systemConfiguration"]["raceInfo"]["timeFormEnabled"]}')

    def test_004_disable_timeformenabled_check_box_in_system_config_in_cms(self):
        """
        DESCRIPTION: Disable 'timeFormEnabled' check box in System Config in CMS
        EXPECTED: 'timeFormEnabled' check box is disabled
        """
        self.cms_config.update_system_configuration_structure(config_item='raceInfo',
                                                              field_name='timeFormEnabled', field_value=False)

    def test_005_reload_ghhr_landing_page_in_app(self):
        """
        DESCRIPTION: Reload GH/HR landing page in App
        EXPECTED: GH/HR landing page is reloaded
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=20),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_006_navigate_to_network___mobile___system_configuration_and_verify_that_timeformenabled_parameter_has_false_value(self):
        """
        DESCRIPTION: Navigate to 'Network' -> 'mobile' -> 'System Configuration' and verify that 'timeFormEnabled' parameter has 'false' value
        EXPECTED: 'timeFormEnabled' has {enabled: false} value
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state_changed()
        self.__class__.raceInfoMobile = self.cms_config.get_initial_data()
        self.assertTrue(self.raceInfoMobile, msg='No raceInfoMobile tag in initial-data response')
        self.assertFalse(self.raceInfoMobile['systemConfiguration']['raceInfo']['timeFormEnabled'],
                         msg="timeFormEnabled parameter in raceInfo is True")
        self.cms_config.update_system_configuration_structure(config_item='raceInfo',
                                                              field_name='timeFormEnabled', field_value=self.status)
