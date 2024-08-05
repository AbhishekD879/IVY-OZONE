import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2986504_Verify_events_on_Races_event_details_page_from_Next_Races_module(Common):
    """
    TR_ID: C2986504
    NAME: Verify events on <Races> event details page from 'Next Races' module
    DESCRIPTION: This test case verifies events on <Races> EDP when navigating from 'Next Races' module
    PRECONDITIONS: 1. 'Next Races' module is configured in CMS on:
    PRECONDITIONS: - Horse Racing > 'Featured' tab
    PRECONDITIONS: - [NOT YET IMPLEMENTED] Horse Racing > 'Next Races' tab
    PRECONDITIONS: - Home Page > 'Next Races' tab
    PRECONDITIONS: 2. 'Next Races' are available on Greyhounds > 'Today' tab
    PRECONDITIONS: 3. Events from different <Types> are available within 'Next Races' module
    PRECONDITIONS: 4. App is loaded
    PRECONDITIONS: 5. Home page > 'Next Races' tab is opened
    """
    keep_browser_open = True

    def test_001_tap_on_any_event_from_next_races(self):
        """
        DESCRIPTION: Tap on any event from 'Next Races'
        EXPECTED: - &lt;Races&gt; event details page is opened
        EXPECTED: - Corresponding 'Event Time' tab is selected and visible
        """
        pass

    def test_002_verify_event_time_tabs(self):
        """
        DESCRIPTION: Verify 'Event Time' tabs
        EXPECTED: Only 'Event Time' tabs that are available in 'Next Races' module are displayed
        EXPECTED: (Events from different &lt;Types&gt; of &lt;Races&gt;)
        """
        pass

    def test_003_navigate_through_event_time_tabs(self):
        """
        DESCRIPTION: Navigate through 'Event Time' tabs
        EXPECTED: Corresponding events from 'Next Races' module are displayed
        """
        pass

    def test_004_repeat_steps_1_3_for__horse_racing_gt_featured_tab_gt_next_races_modulenot_yet_implemented__horse_racing_gt_next_races_tab__greyhounds_gt_today_tab(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Horse Racing &gt; 'Featured' tab &gt; 'Next Races' module
        DESCRIPTION: [NOT YET IMPLEMENTED]- Horse Racing &gt; 'Next Races' tab
        DESCRIPTION: - Greyhounds &gt; 'Today' tab
        EXPECTED: 
        """
        pass
