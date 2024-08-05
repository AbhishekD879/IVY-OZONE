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
class Test_C1901930_Tracking_of_the_View_All_link_in_the_Live_Stream_section_on_the_Homepage(Common):
    """
    TR_ID: C1901930
    NAME: Tracking of the 'View All' link in the 'Live Stream' section on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'View All' link in the 'Live Stream' section on the Homepage.
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
        EXPECTED: * The 'Sports' icons are visible on the 'Sports Ribbon' menu at the 'Live Stream' section and the first is selected by default
        EXPECTED: * The 'View All' link is visible on footer at the bottom of the 'Live Stream' section
        """
        pass

    def test_003_click_on_view_all_link_at_the_footer_below_live_stream_section(self):
        """
        DESCRIPTION: Click on "View All" link at the footer below 'Live Stream' section
        EXPECTED: * 'Live Stream' page is opened
        EXPECTED: * The list of live events with mapped stream is displayed
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'.
        EXPECTED: dataLayer.push( {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'live stream',
        EXPECTED: 'eventLabel' : 'view all'
        EXPECTED: })
        """
        pass
