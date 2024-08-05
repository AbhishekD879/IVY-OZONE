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
class Test_C12927051_In_Play_content_scrolling_when_VirtualScoll_is_ON_and_InnerScroll_enabled_disabled(Common):
    """
    TR_ID: C12927051
    NAME: In-Play content scrolling when VirtualScoll is ON and InnerScroll enabled/disabled
    DESCRIPTION: This test case verifies Virtual Scroll functionality on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when InnerScroll is enabled/disabled in CMS.
    DESCRIPTION: Note: Cannot automate it - the test case contains a lot of UI verification that cannot be done/or hardly done by script
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Open/Tap on 'In-Play' tab on the Homepage
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 1) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 3) 'iOS/AndroidInnerScroll' should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Sport #1 (e.g. Football) should contain:
    PRECONDITIONS: - League #1 with 10 or more live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: - League #2 with less than 10 live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: 2) League #1 should have the lowest disporder in order to be shown first/at the top of the list; League #2 should be next one
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_scroll_down_within_league_1_content(self):
        """
        DESCRIPTION: Scroll down within League #1 content
        EXPECTED: * 1st sport accordion (e.g. Football) becomes sticky below 'Coral/Ladbrokes' header
        EXPECTED: * League #1 header becomes sticky below 1st sport accordion
        EXPECTED: * The rest of the content (i.e. Sports Menu Ribbon, banners, In-play header etc.)becomes hidden
        EXPECTED: ![](index.php?/attachments/get/30395)
        """
        pass

    def test_002_scroll_up_and_down_within_league_1_content(self):
        """
        DESCRIPTION: Scroll up and down within League #1 content
        EXPECTED: * 1st sport accordion and League #1 header remain sticky
        EXPECTED: * Content of league #1 is visible while scrolling
        """
        pass

    def test_003_scroll_down_within_league_1_content_until_reaching_league_2_content(self):
        """
        DESCRIPTION: Scroll down within League #1 content until reaching League #2 content
        EXPECTED: * 1st sport accordion remains sticky
        EXPECTED: * League #1 header becomes hidden
        EXPECTED: ![](index.php?/attachments/get/30396)
        """
        pass

    def test_004_scroll_down_within_league_2_content(self):
        """
        DESCRIPTION: Scroll down within League #2 content
        EXPECTED: * 1st sport accordion remains sticky
        EXPECTED: * League #2 header is NOT sticky (count of events is NOT enough to activate sticky league effect)
        EXPECTED: ![](index.php?/attachments/get/30397)
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
        EXPECTED: * League #1 header becomes sticky below 1st sport accordion
        EXPECTED: * The rest of the content becomes hidden
        EXPECTED: ![](index.php?/attachments/get/30398)
        """
        pass

    def test_007__disable_iosandroidinnerscroll_in_cms__system_configuration__structure__virtualscrollconfig_on_fe_refresh_the_home_page__in_play_tab(self):
        """
        DESCRIPTION: * Disable 'iOS/AndroidInnerScroll' in CMS > System configuration > Structure > VirtualScrollConfig
        DESCRIPTION: * On FE refresh the Home page > 'In-play' tab
        EXPECTED: 
        """
        pass

    def test_008_scroll_down_within_league_1_content(self):
        """
        DESCRIPTION: Scroll down within League #1 content
        EXPECTED: * 1st sport accordion (e.g. Football) becomes sticky below 'Coral/Ladbrokes' header
        EXPECTED: * League #1 header is NOT sticky
        EXPECTED: * The rest of the content (i.e. Sports Menu Ribbon, banners, In-play header etc.)becomes hidden
        EXPECTED: ![](index.php?/attachments/get/30399)
        """
        pass
