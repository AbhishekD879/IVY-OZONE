import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58694702_TO_DELETEVerify_Virtual_Sport_initialData_checkbox_configuration_in_CMS(Common):
    """
    TR_ID: C58694702
    NAME: [TO DELETE]Verify Virtual Sport  'initialData' checkbox configuration in CMS
    DESCRIPTION: Verify Virtual Sport  'initialData' checkbox configuration in CMS
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 1. Load CMS and login there
    PRECONDITIONS: 2. Navigate to System Configuration -> 'Config' tab
    PRECONDITIONS: 3. In CMS Open DevTools (Click on 'Inspect')-> 'Network' tab -> 'XHR' filter
    PRECONDITIONS: 4. Load Coral/Ladbrokes app
    PRECONDITIONS: 5. In App Open DevTools -> 'Network' tab -> 'XHR' filter -> set 'cms' filter to view all requests that go to cms.
    """
    keep_browser_open = True

    def test_001_go_to_cms_system_configuration_section__config_tab__find_virtualsport_config(self):
        """
        DESCRIPTION: Go to CMS >'System-configuration' section > Config' tab > find 'VirtualSport' config
        EXPECTED: * 'System-configuration' section is opened
        EXPECTED: * 'Initial Data' checkbox is present within 'VirtualSport' config and unchecked by default
        EXPECTED: * The response contains 'The initialDataConfig: false'
        EXPECTED: ![](index.php?/attachments/get/107694080)
        """
        pass

    def test_002_check_initial_data_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Check 'Initial Data' checkbox and save changes
        EXPECTED: Changes are saved > 'Initial Data' checkbox is checked
        """
        pass

    def test_003_verify_the_response_in_network_of_devtools(self):
        """
        DESCRIPTION: Verify the response in 'Network' of 'Devtools'
        EXPECTED: The response contains 'The initialDataConfig: true'
        EXPECTED: ![](index.php?/attachments/get/107694077)
        """
        pass

    def test_004_load_app_and_check_get_initial_data_request_to_cms(self):
        """
        DESCRIPTION: Load app and check GET 'initial-data' request to CMS
        EXPECTED: 'VirtualSport' config is received in
        EXPECTED: GET /{brand}/initial-data/{desktop} or {mobile}
        EXPECTED: request from CMS
        EXPECTED: ![](index.php?/attachments/get/107698497)
        """
        pass

    def test_005_go_to_virtual_sports_page(self):
        """
        DESCRIPTION: Go to 'Virtual Sports' page
        EXPECTED: * Virtual Sports page is loaded
        EXPECTED: * GET /{brand}/system-configurations/virtual-sports request is sent to CMS to retrieve config
        EXPECTED: * 'VirtualSport' config is received in the request above
        EXPECTED: ![](index.php?/attachments/get/107698443)
        """
        pass

    def test_006_go_back_to_cms__virtualsport_config_uncheck_initial_data_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to CMS > 'VirtualSport' config, uncheck 'Initial Data' checkbox and save changes
        EXPECTED: * Changes are saved > 'Initial Data' checkbox is unchecked
        EXPECTED: * The response contains 'The initialDataConfig: false'
        EXPECTED: ![](index.php?/attachments/get/107694081)
        """
        pass

    def test_007_go_to_app_and_check_get_initial_data_request_to_cms(self):
        """
        DESCRIPTION: Go to app and check GET 'initial-data' request to CMS
        EXPECTED: 'VirtualSport' config is NOT received in
        EXPECTED: GET /{brand}/initial-data/{desktop} or {mobile}
        EXPECTED: request from CMS
        EXPECTED: ![](index.php?/attachments/get/107698449)
        """
        pass

    def test_008_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps #5
        EXPECTED: Results are the same
        """
        pass
