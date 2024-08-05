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
class Test_C1167444_UPDATE_Verify_last_Football_inplay_event_removed_when_Market_in_Market_selector_Match_Result(Common):
    """
    TR_ID: C1167444
    NAME: (!!UPDATE) Verify last Football inplay event removed when Market in Market selector != Match Result
    DESCRIPTION: This test case verifies that last Football inplay event is removed from In-play page/tab when Market in Market selector != Match Result
    PRECONDITIONS: **TI (Backoffice) config:**
    PRECONDITIONS: * Only 1 football inplay event should be configured
    PRECONDITIONS: * This event should have other markets except Match Result, e.g: Both Teams To Score, Total Goals Over/Under 1.5. To Qualify.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to In-play page > 'Football' tab
    """
    keep_browser_open = True

    def test_001_select_any_other_market_in_market_selector_eg_total_goals_overunder_15(self):
        """
        DESCRIPTION: Select any other market in Market Selector (e.g 'Total Goals Over/Under 1.5')
        EXPECTED: 
        """
        pass

    def test_002_in_ti_undisplay_the_event_from_preconditions_this_event_should_be_the_last_available_on_the_page_so_before_doing_so_make_sure_there_are_no_other_competitionsevents_on_the_page(self):
        """
        DESCRIPTION: In TI undisplay the event from preconditions. (This event should be the last available on the page, so before doing so make sure there are no other competitions/events on the page)
        EXPECTED: * Event is removed from In Play page
        EXPECTED: * "There are currently no Live events available" message is displayed below 'Live now' section
        EXPECTED: * Upcoming events (if there are any) remain displayed
        """
        pass

    def test_003_repeat_steps_1_2_on_football_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat Steps 1-2 on Football Landing page - In Play tab
        EXPECTED: 
        """
        pass
