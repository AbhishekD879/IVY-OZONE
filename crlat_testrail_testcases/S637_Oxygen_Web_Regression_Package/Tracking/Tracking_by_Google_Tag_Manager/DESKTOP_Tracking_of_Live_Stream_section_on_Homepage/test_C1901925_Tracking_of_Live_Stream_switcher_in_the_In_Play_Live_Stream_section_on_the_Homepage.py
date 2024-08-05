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
class Test_C1901925_Tracking_of_Live_Stream_switcher_in_the_In_Play_Live_Stream_section_on_the_Homepage(Common):
    """
    TR_ID: C1901925
    NAME: Tracking of 'Live Stream' switcher in the 'In-Play & Live Stream' section on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Live Stream' switcher in the 'In-Play & Live Stream' section on the Homepage.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_scroll_the_page_down_to_in_play__live_stream_section(self):
        """
        DESCRIPTION: Scroll the page down to 'In-Play & Live Stream' section
        EXPECTED: * 'In-Play & Live Stream' section is available
        EXPECTED: * 'Sports Ribbon' menu is displayed
        EXPECTED: * 'In-Play' switcher is selected by default
        """
        pass

    def test_003_click_on_live_stream_switcher(self):
        """
        DESCRIPTION: Click on 'Live Stream' switcher
        EXPECTED: * 'Live Stream' switcher is selected
        EXPECTED: * The list of live events with the mapped stream is displayed
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
        EXPECTED: 'eventLabel' : 'show events'
        EXPECTED: })
        """
        pass
