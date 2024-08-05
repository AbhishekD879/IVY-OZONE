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
class Test_C120274_Verify_Sport_events_without_Primary_Market_displaying_on_In_Play_pages(Common):
    """
    TR_ID: C120274
    NAME: Verify <Sport> events without Primary Market displaying on 'In-Play' pages
    DESCRIPTION: This test case verifies how <Sport> events without Primary Market are displayed on In-Play pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. For reaching Pre-match events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * Primary Market is any Market that has the following attributes:
    PRECONDITIONS: *   isMarketBetInRun="true" on event level
    PRECONDITIONS: *   outcomeMeaningMajorCode="MR"/"HH" on each outcome level
    """
    keep_browser_open = True

    def test_001_select_ltsportgt_event_with_several_markets_including_primary_market__gt_in_ti_system_undisplay_primary_markets_of_selected_event(self):
        """
        DESCRIPTION: Select &lt;Sport&gt; event with several markets including Primary Market -&gt; In TI system undisplay Primary Market(s) of selected event
        EXPECTED: &lt;Sport&gt; event disappears from the page
        """
        pass

    def test_002_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: *   &lt;Sport&gt; event is shown on the page
        EXPECTED: *   &lt;Sport&gt; event is shown as without 'Price/Odds' buttons
        """
        pass

    def test_003_select_ltsportgt_event_with_several_markets_including_primary_market__gt_in_ti_system_remove_ismarketbetinruntrue_attribute_for_primary_markets_for_selected_event_gt_reload_the_page(self):
        """
        DESCRIPTION: Select &lt;Sport&gt; event with several markets including Primary Market -&gt; In TI system remove isMarketBetInRun="true" attribute for Primary Market(s) for selected event.
        DESCRIPTION: -&gt; Reload the page
        EXPECTED: *   &lt;Sport&gt; event is shown on the page
        EXPECTED: *   &lt;Sport&gt; event is shown as without 'Price/Odds' buttons
        """
        pass

    def test_004_select_ltsportgt_event_with_several_markets_including_primary_market__gt_in_ti_system_undisplay_all_markets_for_selected_event(self):
        """
        DESCRIPTION: Select &lt;Sport&gt; event with several markets including Primary Market -&gt; In TI system undisplay ALL Markets for selected event
        EXPECTED: *   &lt;Sport&gt; event disappears from the page
        """
        pass

    def test_005_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: &lt;Sport&gt; event is NOT shown on the page
        """
        pass

    def test_006_repeat_steps_1_6_for_upcoming_events(self):
        """
        DESCRIPTION: Repeat steps 1-6 for upcoming events
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_sports_landing_page_gt_in_play_tab_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Navigate to Sports Landing page &gt; 'In-Play' tab and repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_008_for_mobiletabletnavigate_to_the_homepage_gt_in_play_tab_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to the Homepage &gt; 'In-Play' tab and repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_009_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_repeat_steps_1_7_for_both_in_play_and_live_stream_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and repeat steps 1-7 for both 'In-play' and 'Live Stream' filter switchers
        EXPECTED: 
        """
        pass
