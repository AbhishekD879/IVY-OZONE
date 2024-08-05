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
class Test_C12783674_Virtual_Scroll_with_InnerScroll_disabled(Common):
    """
    TR_ID: C12783674
    NAME: Virtual Scroll with InnerScroll disabled
    DESCRIPTION: This test case verifies Virtual Scroll functionality on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when InnerScroll is disabled in CMS.
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 1) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 3) 'iOS/AndroidInnerScroll' should be disabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Sport #1 (e.g. Football) should contain:
    PRECONDITIONS: - League #1 with 10 or more live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: - League #2 with less than 10 live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: 2) League #1 should have lowest *disporder* in order to be shown first/at the top of the list; League #2 should be next one
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: Open/Tap on 'In-Play' tab on Home page
    """
    keep_browser_open = True

    def test_001_scroll_down_within_league_1_content(self):
        """
        DESCRIPTION: Scroll down within League #1 content
        EXPECTED: * 1st sport accordion (e.g. Football) becomes sticky below 'Coral/Ladbrokes' header
        EXPECTED: * League #1 header is NOT sticky
        EXPECTED: * The rest of the content (i.e. Sports Menu Ribbon, banners, In-play header etc.)becomes hidden
        EXPECTED: ![](index.php?/attachments/get/30399)
        """
        pass

    def test_002_scroll_up_and_down_within_league_1_content(self):
        """
        DESCRIPTION: Scroll up and down within League #1 content
        EXPECTED: * 1st sport accordion remains sticky
        EXPECTED: * Content of league #1 is visible while scrolling
        """
        pass

    def test_003_scroll_down_within_league_1_content_until_reaching_league_2_content(self):
        """
        DESCRIPTION: Scroll down within League #1 content until reaching League #2 content
        EXPECTED: * 1st sport accordion remains sticky
        EXPECTED: * Neither League #1 header nor League #2 header is sticky
        """
        pass

    def test_004_scroll_down_within_league_2_content(self):
        """
        DESCRIPTION: Scroll down within League #2 content
        EXPECTED: * 1st sport accordion remains sticky
        EXPECTED: * League #2 header is NOT sticky
        """
        pass

    def test_005_repeat_steps_1_4_in_the_upcoming_events_section(self):
        """
        DESCRIPTION: Repeat steps 1-4 in the 'UPCOMING EVENTS' section
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_4_on_watch_live_tab_of_in_play_page_for_both_live_now_and_upcoming_sections(self):
        """
        DESCRIPTION: Repeat steps 1-4 on 'WATCH LIVE' tab of 'IN-PLAY' page (for both "live now' and 'upcoming' sections)
        EXPECTED: For step #1:
        EXPECTED: * 1st sport accordion (e.g. Football) becomes sticky below 'In-play' header and 'Back' button
        EXPECTED: * League #1 header is NOT sticky
        EXPECTED: * The rest of the content becomes hidden
        EXPECTED: ![](index.php?/attachments/get/30400)
        """
        pass
