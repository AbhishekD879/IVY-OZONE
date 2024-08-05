import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C9770239_In_play_content_scrolling_when_VirtualScroll_is_disabled(Common):
    """
    TR_ID: C9770239
    NAME: In-play content scrolling when VirtualScroll is disabled
    DESCRIPTION: This test case verifies scrolling of In-play content on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when VirtualScroll is disabled in CMS
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 1) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2) Virtual Scroll should be disabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: Open/Tap on 'In-Play' tab on Home page
    """
    keep_browser_open = True

    def test_001_scroll_down_until_reaching_content_of_1st_sport_accordion(self):
        """
        DESCRIPTION: Scroll down until reaching content of 1st sport accordion
        EXPECTED: * No elements (i.e. sport accordion/league header) are sticky
        EXPECTED: * 'Coral/Ladbrokes' header together with 'Login/Join now' buttons remain visible
        EXPECTED: ![](index.php?/attachments/get/30403)
        """
        pass

    def test_002__scroll_down_until_reaching_upcoming_events_section_expand_1st_sport_accordion_scroll_down(self):
        """
        DESCRIPTION: * Scroll down until reaching 'Upcoming events' section
        DESCRIPTION: * Expand 1st sport accordion
        DESCRIPTION: * Scroll down
        EXPECTED: * No elements (i.e. sport accordion/league header) are sticky
        EXPECTED: * 'Coral/Ladbrokes' header together with 'Login/Join now' buttons remain visible
        """
        pass

    def test_003_navigate_to_in_play_page__watch_live_tab(self):
        """
        DESCRIPTION: Navigate to 'In-play' page > 'Watch live' tab
        EXPECTED: 
        """
        pass

    def test_004_scroll_down_until_reaching_content_of_1st_sport_accordion(self):
        """
        DESCRIPTION: Scroll down until reaching content of 1st sport accordion
        EXPECTED: * No elements (i.e. sport accordion/league header) are sticky
        EXPECTED: * 'Coral/Ladbrokes' header together with 'Login/Join now' buttons remain visible
        EXPECTED: * 'In-play' header and 'Back' button remain visible
        """
        pass
