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
class Test_C58833987_Verify_initial_checkbox_configuration_in_CMS_for_FallbackScoreboard_config(Common):
    """
    TR_ID: C58833987
    NAME: Verify 'initial' checkbox configuration in CMS for 'FallbackScoreboard' config
    DESCRIPTION: This test case verifies verifies 'initial' checkbox configuration in CMS for 'FallbackScoreboard' config
    PRECONDITIONS: 1. Load CMS and login there
    PRECONDITIONS: 2. Navigate to System Configuration -> 'Config' tab
    PRECONDITIONS: 3. In CMS Open DevTools (Click on 'Inspect')-> 'Network' tab -> 'XHR' filter
    PRECONDITIONS: 4. Load Coral/Ladbrokes app
    PRECONDITIONS: 5. In App Open DevTools -> 'Network' tab -> 'XHR' filter -> set 'cms' filter to view all requests that go to cms.
    """
    keep_browser_open = True

    def test_001_go_to_cms_system_configuration_section__config_tab__find_scoreboardssports_config(self):
        """
        DESCRIPTION: Go to CMS >'System-configuration' section > Config' tab > find 'ScoreboardsSports' config
        EXPECTED: * 'System-configuration' section is opened
        EXPECTED: * 'Initial Data' checkbox is present within 'ScoreboardsSports' config
        """
        pass

    def test_002_check_initial_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Check 'Initial' checkbox and save changes
        EXPECTED: * Changes are saved > 'Initial Data' checkbox is checked
        EXPECTED: * The response contains 'The initialDataConfig: true'
        """
        pass

    def test_003_load_app_and_check_get_initial_data_request_to_cms(self):
        """
        DESCRIPTION: Load app and check GET 'initial-data' request to CMS
        EXPECTED: 'ScoreboardsSports' config is received in
        EXPECTED: GET /{brand}/initial-data/{desktop} or {mobile}
        EXPECTED: request from CMS
        """
        pass

    def test_004_go_to_sport_edp(self):
        """
        DESCRIPTION: Go to Sport EDP
        EXPECTED: * Sport EDP page is loaded
        EXPECTED: * GET /{brand}/system-configurations/ScoreboardsSportsrequest is sent to CMS to retrieve config
        EXPECTED: ![](index.php?/attachments/get/109046295)
        """
        pass

    def test_005_go_back_to_cms__scoreboardssports_config_uncheck_initial_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to CMS > 'ScoreboardsSports' config, uncheck 'Initial' checkbox and save changes
        EXPECTED: * Changes are saved > 'Initial Data' checkbox is unchecked
        EXPECTED: * The response contains 'The initialDataConfig: false'
        """
        pass

    def test_006_go_to_app_and_check_get_initial_data_request_to_cms(self):
        """
        DESCRIPTION: Go to app and check GET 'initial-data' request to CMS
        EXPECTED: 'ScoreboardsSports' config is NOT received in
        EXPECTED: GET /{brand}//initial-data/{desktop} or {mobile}
        EXPECTED: request from CMS
        """
        pass

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: Results are the same
        """
        pass
