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
class Test_C58836097_Verify_Conviva_stream_tracking_in_Pulse(Common):
    """
    TR_ID: C58836097
    NAME: Verify Conviva stream tracking in Pulse
    DESCRIPTION: Test case verifies Conviva streaming monitoring in Pulse monitoring tool
    PRECONDITIONS: List of CMS endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: * To enable/disable Conviva monitoring in CMS: CMS > System Configuration > Conviva -> enabled
    PRECONDITIONS: enable testMode - for testing and debug purpose:
    PRECONDITIONS: CMS > System Configuration > Conviva -> testMode
    PRECONDITIONS: Stream (ATR, IMG or Perform, RUK, RPGTV are supported) is mapped and available for any event in application, IGMedia streams are not supported
    PRECONDITIONS: 1) Set Conviva parameter to enabled in CMS
    PRECONDITIONS: 2) In another tab/browser open Pulse (https://pulse.conviva.com/ ) and login with credentials:
    PRECONDITIONS: username: andrei.banarescu@ladbrokescoral.com
    PRECONDITIONS: password: LadbrokesCoral19
    PRECONDITIONS: 3) Open environment (Coral/Ladbrokes) and login with valid user
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_the_event_with_mapped_stream(self):
        """
        DESCRIPTION: Navigate to Event Details Page of the event with mapped stream
        EXPECTED: * EDP is opened
        EXPECTED: * Stream is available for watching
        """
        pass

    def test_002_tapclick_on_watch_live_button_and_make_sure_stream_is_playing(self):
        """
        DESCRIPTION: Tap/click on 'Watch Live' button and make sure stream is playing
        EXPECTED: 
        """
        pass

    def test_003__open_tabbrowser_with_pulse_verify_event_appears_in_the_content_summary_all_traffic_real_time_table_on_real_time_tab_of_dashboards(self):
        """
        DESCRIPTION: * Open tab/browser with Pulse
        DESCRIPTION: * Verify event appears in the 'Content Summary: All Traffic (Real Time)' table on 'Real-time' tab of dashboards
        EXPECTED: * Event appears in the table with asset name with '[eventID]eventName' and number of Concurrent plays
        EXPECTED: * It could take up to 1 minute for event to appear in table
        EXPECTED: ![](index.php?/attachments/get/109047083)
        """
        pass

    def test_004__open_application_in_another_browser_login_with_any_other_user_navigate_to_event_details_page_of_the_event_with_mapped_stream_and_start_the_stream(self):
        """
        DESCRIPTION: * Open application in another browser
        DESCRIPTION: * Login with any other user
        DESCRIPTION: * Navigate to Event Details Page of the event with mapped stream and start the stream
        EXPECTED: * Stream is available for watching
        EXPECTED: * Stream is playing
        """
        pass

    def test_005__open_tabbrowser_with_pulse_verify_event_appears_in_the_content_summary_all_traffic_real_time_table_on_real_time_tab_of_dashboards(self):
        """
        DESCRIPTION: * Open tab/browser with Pulse
        DESCRIPTION: * Verify event appears in the 'Content Summary: All Traffic (Real Time)' table on 'Real-time' tab of dashboards
        EXPECTED: * Number of 'Concurrent plays' for event under the test increased
        EXPECTED: * It could take up to 1 minute for event to update in table
        EXPECTED: * (!) Note that it could increase by more than 1 concurrent play if any other user runs this event stream at the same time
        EXPECTED: ![](index.php?/attachments/get/109047090)
        """
        pass
