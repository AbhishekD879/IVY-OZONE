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
class Test_C14742516_Verify_last_inplay_event_of_competition_removed_when_market_in_Market_selector_Match_Result(Common):
    """
    TR_ID: C14742516
    NAME: Verify last inplay event of competition removed when market in Market selector !=Match Result
    DESCRIPTION: This test case verifies that last inplay event of competition is removed from In-play page/tab when market in Market selector !=Match Result
    PRECONDITIONS: **TI (Backoffice) config:**
    PRECONDITIONS: * Several football inplay events should be configured in different competitions
    PRECONDITIONS: * 1 of competitions should have ONLY 1 event in it. This event should have other markets except Match Result, e.g: Both Teams To Score, Total Goals Over/Under 1.5. To Qualify. This event should be the only one with other markets
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

    def test_002_in_ti_undisplay_the_event_from_preconditions_this_event_should_be_the_only_one_with_other_markets(self):
        """
        DESCRIPTION: In TI undisplay the event from preconditions. (This event should be the only one with other markets)
        EXPECTED: * Event is removed from In Play page
        EXPECTED: * Default market becomes selected in Market selector
        EXPECTED: * Events containing default market are loaded
        EXPECTED: * Upcoming events (if there are any) remain displayed unchanged
        """
        pass

    def test_003__navigate_to_football_landing_page_gt_in_play_tab_repeat_steps_1_2(self):
        """
        DESCRIPTION: * Navigate to Football Landing page &gt; 'In-play' tab
        DESCRIPTION: * Repeat steps 1-2
        EXPECTED: 
        """
        pass
