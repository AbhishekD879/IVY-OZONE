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
class Test_C1901926_Tracking_of_Sports_icons_in_the_Live_Stream_section_on_the_Homepage(Common):
    """
    TR_ID: C1901926
    NAME: Tracking of 'Sports' icons in the 'Live Stream' section on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Sports' icons in the 'Live Stream' section on the Homepage.
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

    def test_002_scroll_the_page_down_to_in_play__live_stream_section_and_select_live_stream_switcher(self):
        """
        DESCRIPTION: Scroll the page down to 'In-Play & Live Stream' section and select 'Live Stream' switcher
        EXPECTED: The 'Sports' icons are visible on the 'Sports Ribbon' menu at the 'Live Stream' section
        """
        pass

    def test_003_click_on_some_sports_icon(self):
        """
        DESCRIPTION: Click on some 'Sports' icon
        EXPECTED: * 'Sports' is selected
        EXPECTED: * The list of live events with the mapped stream of that particular sport is displayed
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'live stream',
        EXPECTED: 'eventLabel' : 'nav - << SPORT NAME >>'
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_for_different_sports_icons(self):
        """
        DESCRIPTION: Repeat steps 3-4 for different 'Sports' icons
        EXPECTED: 
        """
        pass
