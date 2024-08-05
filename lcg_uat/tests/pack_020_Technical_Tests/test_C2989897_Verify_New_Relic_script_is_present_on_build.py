import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.high
# @pytest.mark.new_relic
# @pytest.mark.desktop
# @pytest.mark.other
# @pytest.mark.safari
# @vtest
@pytest.mark.na
class Test_C2989897_Verify_New_Relic_script_is_present_on_build(Common):
    """
    TR_ID: C2989897
    NAME: Verify New Relic script is present on build
    DESCRIPTION: This test case verifies whether NewRelic is integrated with the application
    PRECONDITIONS: Browser console is opened
    PRECONDITIONS: In CMS make sure 'newRelic' group>'interceptAjax' is enabled in System Configuration
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In CMS make sure 'newRelic' group>'interceptAjax' is enabled in System Configuration
        """
        new_relic_cms_config = self.get_initial_data_system_configuration().get('newRelic', {})
        if not new_relic_cms_config:
            new_relic_cms_config = self.cms_config.get_system_configuration_item('newRelic')
        if not new_relic_cms_config.get('interceptAjax'):
            raise CmsClientException('"interceptAjax" is disabled in "newRelic" group in System Configuration')

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_type_in_browser_console_newrelicevents_and_tap_enter_go_to_some_page_and_type_in_console_newrelicevents(self):
        """
        DESCRIPTION: Type in browser console "newRelicEvents = {}" and tap 'Enter'
        DESCRIPTION: go to some page and type in console 'newRelicEvents'
        EXPECTED: New Relic object is shown in console output
        """
        self.site.initialize_new_relic

        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='Login dialog is not present on page')

        new_relic = self.site.get_new_relic
        self.assertTrue(new_relic, msg='New Relic object is not present in console output')
