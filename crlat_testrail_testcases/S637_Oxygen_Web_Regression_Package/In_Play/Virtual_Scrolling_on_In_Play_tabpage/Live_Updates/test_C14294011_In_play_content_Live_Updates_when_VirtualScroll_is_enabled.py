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
class Test_C14294011_In_play_content_Live_Updates_when_VirtualScroll_is_enabled(Common):
    """
    TR_ID: C14294011
    NAME: In-play content Live Updates when VirtualScroll is enabled
    DESCRIPTION: This test case verifies In-play content Live Updates on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when VirtualScroll is enabled in CMS.
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
    PRECONDITIONS: *To verify subscriptions open Network>WS>inplay-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket*
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: Open/Tap on 'In-Play' tab on Home page
    """
    keep_browser_open = True

    def test_001_in_ti_trigger_price_change_or_eventmarketselection_suspension_for_any_event_that_is_visible(self):
        """
        DESCRIPTION: In TI trigger price change or event/market/selection suspension for any event that is visible
        EXPECTED: * Update regarding price change or suspensionis received in WS
        EXPECTED: * Price change or suspension is immediately shown on front-end
        """
        pass

    def test_002_in_ti_trigger_price_change_or_eventmarketselection_suspension_for_any_event_that_is_not_visible(self):
        """
        DESCRIPTION: In TI trigger price change or event/market/selection suspension for any event that is NOT visible
        EXPECTED: * No updates in WS for that event
        """
        pass

    def test_003_scroll_down_so_that_event_from_step_2_becomes_visible(self):
        """
        DESCRIPTION: Scroll down so that event from step 2 becomes visible
        EXPECTED: * Subscription to that league is done
        EXPECTED: * Update regarding price change or suspension is received in WS
        EXPECTED: * Price change or suspension is reflected on front-end
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
