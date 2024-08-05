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
class Test_C14294010_In_play_content_subscriptions_when_VirtualScroll_is_enabled(Common):
    """
    TR_ID: C14294010
    NAME: In-play content subscriptions when VirtualScroll is enabled
    DESCRIPTION: This test case verifies In-play content subscriptions on 'In-play' tab (Home page) and 'Watch live' tab (In-play page) when VirtualScroll is enabled in CMS.
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

    def test_001_verify_subscriptions_on_initial_load_of_in_play_content(self):
        """
        DESCRIPTION: Verify subscriptions on initial load of in-play content
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the value, set in 'InPlayCompetitionsExpanded' in CMS
        EXPECTED: * Subscription to events of only those leagues that are visible
        EXPECTED: ![](index.php?/attachments/get/30547)
        """
        pass

    def test_002__scroll_down_until_show_all_sport_namecount_button_click_show_all_button_and_verify_subscriptions(self):
        """
        DESCRIPTION: * Scroll down until 'Show all <sport name><count>' button
        DESCRIPTION: * Click 'Show all' button and verify subscriptions
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the number of remaining leagues OR to 15 first if there are more that 15 remained(even if they are not visible)
        EXPECTED: * Subscriptions are done to only those leagues that are visible
        EXPECTED: ![](index.php?/attachments/get/30553)
        """
        pass

    def test_003__scroll_down_so_that_the_last_event_of_specific_league_is_not_shown_any_more_and_events_of_the_next_league_become_visible_verify_subscriptions(self):
        """
        DESCRIPTION: * Scroll down so that the last event of specific league is not shown any more AND events of the next league become visible
        DESCRIPTION: * Verify subscriptions
        EXPECTED: * Unsubscribe from all events of not visible league is done
        EXPECTED: * Subscription to events of the league that became visible is done
        """
        pass

    def test_004_collapse_sport_accordion_and_verify_subscriptions(self):
        """
        DESCRIPTION: Collapse sport accordion and verify subscriptions
        EXPECTED: * Unsubscribe from all events within that sport is done
        """
        pass

    def test_005__scroll_down_until_upcoming_events_section_expand_sport_accordion_and_verify_subscriptions(self):
        """
        DESCRIPTION: * Scroll down until 'Upcoming events' section
        DESCRIPTION: * Expand sport accordion and verify subscriptions
        EXPECTED: * Count of 'GET_TYPE' subscriptions corresponds to the value, set in 'InPlayCompetitionsExpanded' in CMS
        EXPECTED: * Subscription to events of only those leagues that are visible
        """
        pass

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_in_play_page__watch_live_tab_and_repeat_steps_1_6(self):
        """
        DESCRIPTION: Navigate to 'In-play' page > 'Watch live' tab and repeat steps 1-6
        EXPECTED: 
        """
        pass
