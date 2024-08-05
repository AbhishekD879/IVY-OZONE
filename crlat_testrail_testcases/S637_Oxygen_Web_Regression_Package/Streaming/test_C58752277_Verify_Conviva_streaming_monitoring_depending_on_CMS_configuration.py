import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C58752277_Verify_Conviva_streaming_monitoring_depending_on_CMS_configuration(Common):
    """
    TR_ID: C58752277
    NAME: Verify Conviva streaming monitoring depending on CMS configuration
    DESCRIPTION: Test case verifies presence of Conviva streaming monitoring depending on CMS configuration
    PRECONDITIONS: List of CMS endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: * To enable/disable Conviva monitoring in CMS:
    PRECONDITIONS: ** CMS > System Configuration > Conviva -> enabled **
    PRECONDITIONS: enable testMode - for testing and debug purpose:
    PRECONDITIONS: CMS > System Configuration > Conviva -> testMode
    PRECONDITIONS: * Stream (ATR, IMG or Perform are supported) is mapped and available for any event in application
    PRECONDITIONS: 1) Set Conviva parameter to enabled in CMS
    PRECONDITIONS: 2) Open environment and login with valid user
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_the_event_with_mapped_stream(self):
        """
        DESCRIPTION: Navigate to EDP of the event with mapped stream
        EXPECTED: * EDP is opened
        EXPECTED: * Stream is available for watching
        """
        pass

    def test_002_open_devtools_and_check_for_requests_to_domain_with_convivacomeg_ladbrokescoralgroup_testtestonlyconvivacom(self):
        """
        DESCRIPTION: Open devtools and check for requests to domain with **conviva.com**
        DESCRIPTION: (e.g. ladbrokescoralgroup-test.testonly.conviva.com)
        EXPECTED: * Request is send to Conviva domain once in a second
        EXPECTED: * Status of requests is 200
        """
        pass

    def test_003_for_non_prod_environments_onlycheck_console_log_during_playing_stream(self):
        """
        DESCRIPTION: **[For non-PROD environments only]**
        DESCRIPTION: Check console log during playing stream
        EXPECTED: [Conviva] logs are present in Console
        """
        pass

    def test_004__in_environment_cms_set_cms__system_configuration__conviva_uncheck_enabled_and_testmode_parameters_save_changes(self):
        """
        DESCRIPTION: * In environment CMS set (CMS > System Configuration > Conviva) uncheck "enabled" and 'testMode' parameters
        DESCRIPTION: * Save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_005_refresh_application_and_check_initial_data_from_cms__mobile_or_desktop_request_in_devtools(self):
        """
        DESCRIPTION: Refresh application and check initial data from CMS ( **mobile** or **desktop** request in devtools)
        EXPECTED: In System Configuration > Conviva there is status
        EXPECTED: **enabled:false**
        """
        pass

    def test_006_start_playing_the_stream_on_edp_of_the_event_from_precondition(self):
        """
        DESCRIPTION: Start playing the stream on EDP of the event from precondition
        EXPECTED: Stream is displayed correctly
        """
        pass

    def test_007_open_devtools_and_check_for_requests_to_domain_with_convivacomeg_ladbrokescoralgroup_testtestonlyconvivacom(self):
        """
        DESCRIPTION: Open devtools and check for requests to domain with **conviva.com**
        DESCRIPTION: (e.g. ladbrokescoralgroup-test.testonly.conviva.com)
        EXPECTED: There are NO request to **conviva.com** domain
        """
        pass

    def test_008_for_non_prod_environments_onlycheck_console_log_during_stream_playing(self):
        """
        DESCRIPTION: **[For non-PROD environments only]**
        DESCRIPTION: Check console log during stream playing
        EXPECTED: [Conviva] logs are NOT present in Console
        """
        pass
