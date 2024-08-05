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
class Test_C12797357_Subscriptions_on_initial_load_when_VirtualScroll_is_enabled(Common):
    """
    TR_ID: C12797357
    NAME: Subscriptions on initial load when VirtualScroll is enabled
    DESCRIPTION: This test case verifies subscriptions on initial load of In-play content on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when VirtualScroll is enabled in CMS.
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 1) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 2) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 3) System configuration > Structure > 'InPlayCompetitionsExpanded' should be set to any value e.g. 4
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Sport #1 (e.g. Football) should contain several leagues e.g. 5 with:
    PRECONDITIONS: - live events
    PRECONDITIONS: - upcoming events
    PRECONDITIONS: - events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: *To verify subscriptions open* Network>WS>inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: Open/Tap on 'In-Play' tab on Home page
    """
    keep_browser_open = True

    def test_001_verify_subscriptions_on_initial_load_of_in_play_content(self):
        """
        DESCRIPTION: Verify subscriptions on initial load of in-play content
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the value, set in 'InPlayCompetitionsExpanded' in CMS
        EXPECTED: * Subscription to events of only those leagues that are visible
        EXPECTED: ![](index.php?/attachments/get/30547)
        """
        pass

    def test_002_scroll_down_until_upcoming_events_section(self):
        """
        DESCRIPTION: Scroll down until 'Upcoming events' section
        EXPECTED: 
        """
        pass

    def test_003_expand_sport_accordion_and_verify_subscriptions(self):
        """
        DESCRIPTION: Expand sport accordion and verify subscriptions
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the value, set in 'InPlayCompetitionsExpanded' in CMS
        EXPECTED: * Subscription to events of only those leagues that are visible
        """
        pass

    def test_004_navigate_to_in_play_page__watch_live_tab_and_verify_subscriptions(self):
        """
        DESCRIPTION: Navigate to 'In-play' page > 'Watch live' tab and verify subscriptions
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the value, set in 'InPlayCompetitionsExpanded' in CMS
        EXPECTED: * Subscription to events of only those leagues that are visible
        """
        pass

    def test_005_scroll_down_until_upcoming_events_section(self):
        """
        DESCRIPTION: Scroll down until 'Upcoming events' section
        EXPECTED: 
        """
        pass

    def test_006_expand_sport_accordion_and_verify_subscriptions(self):
        """
        DESCRIPTION: Expand sport accordion and verify subscriptions
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the value, set in 'InPlayCompetitionsExpanded' in CMS
        EXPECTED: * Subscription to events of only those leagues that are visible
        """
        pass
