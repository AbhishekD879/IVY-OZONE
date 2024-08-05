import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C58833961_Verify_Overask_initialData_checkbox_configuration_in_CMS(Common):
    """
    TR_ID: C58833961
    NAME: Verify Overask 'initialData' checkbox configuration in CMS
    DESCRIPTION: Verify Overask 'initialData' checkbox configuration in CMS
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 1. Load CMS and login
    PRECONDITIONS: 2. Navigate to System Configuration -> 'Config' tab
    PRECONDITIONS: 3. In CMS Open DevTools (Click on 'Inspect')-> 'Network' tab -> 'XHR' filter
    PRECONDITIONS: 4. Prepare an event with overask
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: Load Coral/Ladbrokes app
    PRECONDITIONS: In App Open DevTools -> 'Network' tab -> 'XHR' filter -> set 'cms' filter to view all requests that go to cms.
    """
    keep_browser_open = True

    def test_001_go_to_cms_system_configuration_section__config_tab__find_overask_config(self):
        """
        DESCRIPTION: Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
        EXPECTED: * 'System-configuration' section is opened
        EXPECTED: * 'Initial Data' checkbox is present within 'Overask' config and unchecked by default
        EXPECTED: * The response contains 'The initialDataConfig: false'
        EXPECTED: ![](index.php?/attachments/get/109045765) ![](index.php?/attachments/get/109045770)
        """
        pass

    def test_002_check_initial_data_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Check 'Initial Data' checkbox and save changes
        EXPECTED: * The changes are saved
        EXPECTED: * The 'Initial Data' checkbox is ticked
        """
        pass

    def test_003_verify_the_response_in_network_of_devtools(self):
        """
        DESCRIPTION: Verify the response in 'Network' of 'Devtools'
        EXPECTED: The response contains 'The initialDataConfig: true'
        EXPECTED: ![](index.php?/attachments/get/109045904) ![](index.php?/attachments/get/109045906)
        """
        pass

    def test_004_verify_the_response_in_network_of_devtools_of_the_initial_data_call_for_the_same_group_on_coralladbrokes_homepage(self):
        """
        DESCRIPTION: Verify the response in 'Network' of 'Devtools' of the Initial Data call for the same group on Coral/Ladbrokes Homepage
        EXPECTED: The response for the config is present
        EXPECTED: ![](index.php?/attachments/get/109045911) ![](index.php?/attachments/get/109045912)
        """
        pass

    def test_005_trigger_an_overask(self):
        """
        DESCRIPTION: Trigger an overask
        EXPECTED: Overask is triggered
        """
        pass

    def test_006_go_back_to_cms__overask_config_uncheck_initial_data_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to CMS > 'Overask' config, uncheck 'Initial Data' checkbox and save changes
        EXPECTED: * Changes are saved > 'Initial Data' checkbox is unchecked
        EXPECTED: * The response contains 'The initialDataConfig: false
        EXPECTED: ![](index.php?/attachments/get/109045765) ![](index.php?/attachments/get/109045770)
        """
        pass

    def test_007_verify_the_response_in_network_of_devtools_of_the_initial_data_call_for_the_same_group_on_coralladbrokes_homepage(self):
        """
        DESCRIPTION: Verify the response in 'Network' of 'Devtools' of the Initial Data call for the same group on Coral/Ladbrokes Homepage
        EXPECTED: The response for the config is absent
        """
        pass

    def test_008_trigger_an_overask(self):
        """
        DESCRIPTION: Trigger an overask
        EXPECTED: Overask is triggered
        """
        pass
