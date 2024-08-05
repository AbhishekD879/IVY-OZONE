import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1198502_Verify_aggregation_MS_usage_for_Horse_Racing_silks_depending_on_CMS_configuration(Common):
    """
    TR_ID: C1198502
    NAME: Verify aggregation MS usage for Horse Racing silks depending on CMS configuration
    DESCRIPTION: This test case verifies aggregation MS usage depending on CMS configuration
    PRECONDITIONS: In CMS -> Config aggregationMS group is created with field type 'Checkbox' and default value 'Enabled'
    PRECONDITIONS: Featured Module for Racing type is configured and there are available silks for the module's events
    PRECONDITIONS: Featured tab is configured to display on the Homepage as a first one
    """
    keep_browser_open = True

    def test_001_in_cms___system_configuration___check_that_aggregationms_is_enabledload_oxygen_application_for_the_first_time_initial_loading(self):
        """
        DESCRIPTION: In CMS - System Configuration -> check that aggregationMS is enabled.
        DESCRIPTION: Load Oxygen application for the first time (initial loading).
        EXPECTED: - Featured tab is displayed
        EXPECTED: - Featured module for selected Racing type is displayed
        EXPECTED: - Silks for events from the module are displayed on the page
        """
        pass

    def test_002_in_network_select_request_httpsaggregation_ms_devsymphony_solutionseuracingpost(self):
        """
        DESCRIPTION: In Network select request https://aggregation-ms-dev.symphony-solutions.eu/racingpost
        EXPECTED: - Request is present in Network
        EXPECTED: - File with all silks is displayed in response preview
        """
        pass

    def test_003_go_to_horse_racing_landing_page_and_verify_silks_displaying_on_the_page(self):
        """
        DESCRIPTION: Go to Horse racing landing page and verify silks displaying on the page
        EXPECTED: - Silks for events from the next Races module are displayed on the page
        EXPECTED: - New 'https://aggregation-ms-dev.symphony-solutions.eu/racingpost' request is displayed in 'Network - Img' with all generated sprites for Horse Racing landing page
        """
        pass

    def test_004_repeat_step_3_for_horse_racing_event_details_page(self):
        """
        DESCRIPTION: Repeat step 3 for Horse Racing event details page
        EXPECTED: - Silks for event details page are displayed
        EXPECTED: - New 'https://aggregation-ms-dev.symphony-solutions.eu/racingpost' request is displayed in Network - Img' with all generated sprites for Horse Racing event details page
        """
        pass

    def test_005_repeat_step_3_for_next_races_tab_on_the_homepage(self):
        """
        DESCRIPTION: Repeat step 3 for 'Next Races' tab on the Homepage
        EXPECTED: - Silks for 'Next Races' widget are displayed
        EXPECTED: - New 'https://aggregation-ms-dev.symphony-solutions.eu/racingpost' request is displayed in Network - Img' with all generated sprites for Horse Racing event details page
        """
        pass

    def test_006_in_cms___system_configuration_set_is_enabled__false_for_aggregationms_groupload_oxygen_application_for_the_first_time_initial_loading(self):
        """
        DESCRIPTION: In CMS -> System Configuration set is enabled = false for AggregationMS group.
        DESCRIPTION: Load Oxygen application for the first time (initial loading).
        EXPECTED: - Featured tab is displayed
        EXPECTED: - Featured module for selected Racing type is displayed
        EXPECTED: - Silks for events from the module are displayed on the page
        """
        pass

    def test_007_in_network_select_request_httpsaggregation_ms_devsymphony_solutionseuracingpost(self):
        """
        DESCRIPTION: In Network select request https://aggregation-ms-dev.symphony-solutions.eu/racingpost
        EXPECTED: - request is absent
        EXPECTED: - all silks are received in 'https://img.coral.co.uk/'  separate files
        """
        pass

    def test_008_go_to_horse_racing_landing_page_and_verify_silks_displaying_on_the_page(self):
        """
        DESCRIPTION: Go to Horse racing landing page and verify silks displaying on the page
        EXPECTED: - Silks for events from the Next Races module are displayed on the page
        EXPECTED: - all silks are received in 'https://img.coral.co.uk/'  separate files
        """
        pass

    def test_009_repeat_step_8_for_horse_racing_event_details_page(self):
        """
        DESCRIPTION: Repeat step 8 for Horse Racing event details page
        EXPECTED: - Silks for event details page are displayed
        EXPECTED: - all silks are received in 'https://img.coral.co.uk/'  separate files
        """
        pass

    def test_010_repeat_step_8_for_next_races_tab_on_the_homepage(self):
        """
        DESCRIPTION: Repeat step 8 for 'Next Races' tab on the Homepage
        EXPECTED: - Silks for events from the 'Next Races' widget are displayed on the page
        EXPECTED: - all silks are received in 'https://img.coral.co.uk/'  separate files
        """
        pass
