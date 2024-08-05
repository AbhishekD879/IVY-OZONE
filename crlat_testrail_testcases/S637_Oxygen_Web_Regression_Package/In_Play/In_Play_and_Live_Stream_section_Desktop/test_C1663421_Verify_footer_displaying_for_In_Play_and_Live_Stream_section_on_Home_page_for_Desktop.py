import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C1663421_Verify_footer_displaying_for_In_Play_and_Live_Stream_section_on_Home_page_for_Desktop(Common):
    """
    TR_ID: C1663421
    NAME: Verify footer displaying for 'In-Play and Live Stream' section on Home page for Desktop
    DESCRIPTION: This test case verifies footer displaying for 'In-Play and Live Stream' section on Home page for Desktop
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Home page is opened
        """
        pass

    def test_002_scroll_the_page_down_to_view_in_play_and_live_stream_section(self):
        """
        DESCRIPTION: Scroll the page down to view 'In-play and Live Stream' section
        EXPECTED: * 'In-play and Live Stream' section is displayed below 'Enhances Multiples' carousel
        EXPECTED: * Two switchers are visible: 'In-Play' and 'Live Stream'
        EXPECTED: * 'In-Play' switcher is selected by default
        EXPECTED: * First 'Sport' tab is selected by default
        """
        pass

    def test_003_verify_footer_displaying_for_sport_with_4_in_play_events_or_less(self):
        """
        DESCRIPTION: Verify footer displaying for sport with 4 in-play events or less
        EXPECTED: * Footer is displayed below the last accordion
        EXPECTED: * Footer text says: 'View all In-Play events'
        EXPECTED: * Link redirects to 'In-play' page with 1st sport tab selected in ribbon
        """
        pass

    def test_004_verify_footer_displaying_for_sport_with_more_than_4_in_play_events(self):
        """
        DESCRIPTION: Verify footer displaying for sport with more than 4 in-play events
        EXPECTED: * Footer is displayed below the last accordion
        EXPECTED: * Footer text says: 'View all <sport name> events'
        EXPECTED: * Link redirects to 'In-play' page with respective <sport> tab selected in ribbon
        """
        pass

    def test_005_select_sport_that_has_5_in_play_events_and_undisplayresult_one_last_from_type(self):
        """
        DESCRIPTION: Select sport that has 5 in-play events and undisplay/result one (last from type)
        EXPECTED: * Event is undisplayed
        EXPECTED: * Footer text changes from 'View all <sport name> events' to 'View all In-Play events'
        EXPECTED: * Footer link redirects to 'In-play' page with 1st sport tab selected in ribbon
        """
        pass

    def test_006_select_live_stream_switcher_and_verify_footer(self):
        """
        DESCRIPTION: Select 'Live Stream' switcher and verify footer
        EXPECTED: * Footer is displayed below the last accordion
        EXPECTED: * Footer text says: 'View all Live Stream events'
        EXPECTED: * Link redirects to 'Live Stream' page
        EXPECTED: * The same footer text and link regardless of number of events
        """
        pass

    def test_007_select_sport_that_has_no_live_streaming_events(self):
        """
        DESCRIPTION: Select sport that has no live streaming events
        EXPECTED: * 'No events found' message is shown
        EXPECTED: * Footer text and link remains displayed
        """
        pass
