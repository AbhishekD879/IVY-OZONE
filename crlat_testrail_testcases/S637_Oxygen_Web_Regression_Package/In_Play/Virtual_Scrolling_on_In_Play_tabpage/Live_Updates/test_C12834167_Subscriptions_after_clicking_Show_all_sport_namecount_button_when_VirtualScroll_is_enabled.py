import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C12834167_Subscriptions_after_clicking_Show_all_sport_namecount_button_when_VirtualScroll_is_enabled(Common):
    """
    TR_ID: C12834167
    NAME: Subscriptions after clicking 'Show all <sport name><count>' button when VirtualScroll is enabled
    DESCRIPTION: This test case verifies subscriptions after clicking 'Show all <sport name><count>' button when VirtualScroll is enabled in CMS.
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 1) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 3) System configuration > Structure > 'InPlayCompetitionsExpanded' should be set to any value e.g. 4
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Sport #1 (e.g. Football) should contain several leagues e.g. 7 with:
    PRECONDITIONS: - live events
    PRECONDITIONS: - upcoming events
    PRECONDITIONS: - events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: *To verify subscriptions open dev tools > Network>WS>inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket*
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: Open/Tap on 'In-Play' tab on Home page
    """
    keep_browser_open = True

    def test_001_scroll_down_until_show_all_sport_namecount_button(self):
        """
        DESCRIPTION: Scroll down until 'Show all <sport name><count>' button
        EXPECTED: ![](index.php?/attachments/get/30552)
        """
        pass

    def test_002_click_show_all_sport_namecount_and_verify_subscriptions(self):
        """
        DESCRIPTION: Click 'Show all <sport name><count>' and verify subscriptions
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the number of remaining leagues OR to 15 first if there are more that 15 remained (even if they are not visible)
        EXPECTED: * Subscriptions are done to only those leagues that are visible
        EXPECTED: ![](index.php?/attachments/get/30553)
        """
        pass

    def test_003__scroll_down_until_upcoming_events_section_expand_sport_accordion_repeat_steps_1_2(self):
        """
        DESCRIPTION: * Scroll down until 'Upcoming events' section
        DESCRIPTION: * Expand sport accordion
        DESCRIPTION: * Repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_in_play_page__watch_live_tab_and_repeat_steps_1_3(self):
        """
        DESCRIPTION: Navigate to 'In-play' page > 'Watch live' tab and repeat steps 1-3
        EXPECTED: 
        """
        pass
