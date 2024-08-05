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
class Test_C1894932_Tracking_of_Additional_Market_link_in_the_In_Play_section_on_the_Homepage(Common):
    """
    TR_ID: C1894932
    NAME: Tracking of 'Additional Market' link in the 'In-Play' section on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Additional Market' link in the 'In-Play' section on the Homepage.
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

    def test_002_scroll_the_page_down_to_in_play__live_stream_section_and_select_in_play_switcher(self):
        """
        DESCRIPTION: Scroll the page down to 'In-Play & Live Stream' section and select 'In-Play' switcher
        EXPECTED: * The 'Sports' icons are visible on the 'Sports Ribbon' menu at the 'In-Play' section and the first is selected by default
        EXPECTED: * The 'Additional Market' links are visible on the event cards at 'In-Play' section
        """
        pass

    def test_003_click_on_some_additional_market_link(self):
        """
        DESCRIPTION: Click on some 'Additional Market' link
        EXPECTED: Event Details page for the particular event is opened with the list of markets
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: A few events corresponding to each click have been created in data Layer and includes:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'home',
        EXPECTED: 'eventAction' : 'in-play',
        EXPECTED: 'eventLabel' : 'more markets'
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_3_4_for_additional_market_links_from_different_events(self):
        """
        DESCRIPTION: Repeat steps 3-4 for 'Additional Market' links from different events
        EXPECTED: 
        """
        pass
