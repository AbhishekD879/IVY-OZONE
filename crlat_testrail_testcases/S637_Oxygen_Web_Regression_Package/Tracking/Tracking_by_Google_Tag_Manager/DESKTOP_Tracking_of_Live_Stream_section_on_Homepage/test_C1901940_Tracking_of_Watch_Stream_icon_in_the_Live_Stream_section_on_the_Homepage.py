import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1901940_Tracking_of_Watch_Stream_icon_in_the_Live_Stream_section_on_the_Homepage(Common):
    """
    TR_ID: C1901940
    NAME: Tracking of 'Watch Stream' icon in the 'Live Stream' section on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Watch Stream' icon in the 'Live Stream' section on the Homepage.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * More than one live event with mapped stream should be present
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_scroll_the_page_down_to_in_play__live_stream_section_and_select_live_stream_switcher(self):
        """
        DESCRIPTION: Scroll the page down to 'In-Play & Live Stream' section and select 'Live Stream' switcher
        EXPECTED: * The 'Sports' icons are visible on the 'Sports Ribbon' menu at the 'Live Stream' section
        EXPECTED: * The list of live events with the mapped stream is displayed
        EXPECTED: * 'Watch Stream' icons are displayed at the left side of the event card
        """
        pass

    def test_003_click_on_watch_stream_icon(self):
        """
        DESCRIPTION: Click on 'Watch Stream' icon
        EXPECTED: The stream is loaded in the video player in the 'In-Play & Live Stream' section
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'.
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'live stream',
        EXPECTED: 'eventLabel' : 'watch stream'
        EXPECTED: })
        """
        pass
