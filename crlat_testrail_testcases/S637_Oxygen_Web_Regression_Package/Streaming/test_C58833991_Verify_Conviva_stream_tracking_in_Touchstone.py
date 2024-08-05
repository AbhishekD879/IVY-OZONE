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
class Test_C58833991_Verify_Conviva_stream_tracking_in_Touchstone(Common):
    """
    TR_ID: C58833991
    NAME: Verify Conviva stream tracking in Touchstone
    DESCRIPTION: Test case verifies Conviva streaming monitoring in Touchstone
    PRECONDITIONS: List of CMS endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: * To enable/disable Conviva monitoring in CMS:
    PRECONDITIONS: ** CMS > System Configuration > Conviva -> enabled **
    PRECONDITIONS: enable testMode - for testing and debug purpose:
    PRECONDITIONS: CMS > System Configuration > Conviva -> testMode
    PRECONDITIONS: * Stream (ATR, IMG or Perform, RUK, RPGTV are supported) is mapped and available for any event in application, IGMedia streams are not supported
    PRECONDITIONS: 1) Set Conviva parameter to enabled in CMS
    PRECONDITIONS: 2) In another tab/browser open Touchstone (https://touchstone.conviva.com/sources ) and login with credentials:
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

    def test_003__open_tabbrowser_with_touchstone_verify_event_appears_in_the_table_on_home_page(self):
        """
        DESCRIPTION: * Open tab/browser with Touchstone
        DESCRIPTION: * Verify event appears in the table on Home page
        EXPECTED: Event appears in the table with active status, event name and OB id, Browser/OS, Remote address
        EXPECTED: ![](index.php?/attachments/get/109046522)
        """
        pass

    def test_004_tapclick_on_monitor_this_device_button(self):
        """
        DESCRIPTION: Tap/Click on 'Monitor this device' button
        EXPECTED: Page with more information about the stream playing is opened: Content information, Player & SDK Information, Tags and others.
        EXPECTED: ![](index.php?/attachments/get/109046525)
        """
        pass

    def test_005_in_coralladbrokes_app_play_another_stream_same_provider_or_another(self):
        """
        DESCRIPTION: In Coral/Ladbrokes app play another stream (same provider or another)
        EXPECTED: Stream is playing
        """
        pass

    def test_006_in_touchstone_open_dropdown_and_make_sure_that_new_event_appears(self):
        """
        DESCRIPTION: In Touchstone open dropdown and make sure that new event appears
        EXPECTED: ![](index.php?/attachments/get/109046526)
        """
        pass
