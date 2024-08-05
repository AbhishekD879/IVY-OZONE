import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64055788_League_filter_Time_filter_should_disappear_if_there_is_no_events_available_in_Matches_tab_competitions_tab(Common):
    """
    TR_ID: C64055788
    NAME: League filter & Time filter should disappear if there is no events available in Matches tab & competitions tab.
    DESCRIPTION: Verify that the league filter & time filter should disappear if there is no events available in Matches tab & competitions tab.
    PRECONDITIONS: * Checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; Feature Toggle-&gt;sporteventfilters.
    PRECONDITIONS: * Initially validate for tier-1 sport.
    PRECONDITIONS: Condition 1:-
    PRECONDITIONS: *Any one Time Filter in Matches and Competitions page & League Filter in Matches page should be configured in CMS.
    PRECONDITIONS: *No events should be available in SLP & Competitions page in Front End.
    PRECONDITIONS: Condition 2:-
    PRECONDITIONS: *Create 72h Time Filter  in Matches and Competitions page & any league filter in Matches page should be configured in CMS.
    PRECONDITIONS: *Events should be available beyond 72h in SLP & Competitions page in Front End.
    PRECONDITIONS: Condition 3:-
    PRECONDITIONS: *Configure any Time Filter between 1h-72h & Valid League Filter in CMS.
    PRECONDITIONS: *Events should be available within 72h in SLP & Competitions page in Front End.
    PRECONDITIONS: Condition 4:-
    PRECONDITIONS: *Configure Time Filter from 1h-72h & create invalid League(The league which don't have available events in FE) Filter in CMS.
    PRECONDITIONS: *Events should be available within 72h in SLP & Competitions page in Front End.
    """
    keep_browser_open = True

    def test_001_based_on_pre_condition_1_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 1 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: * 'No events Found' message will be displayed.
        """
        pass

    def test_002_based_on_pre_condition_1_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Based on Pre-Condition 1 Navigate to Competitions page.
        EXPECTED: * 'No events Found' message will be displayed.
        """
        pass

    def test_003_based_on_pre_condition_2_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 2 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: Desktop:
        EXPECTED: * 'No events Found' message will be displayed.
        EXPECTED: Mobile:
        EXPECTED: * Events shown beyond 72h along with Time frame.
        """
        pass

    def test_004_based_on_pre_condition_2_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Based on Pre-Condition 2 Navigate to Competitions page.
        EXPECTED: * Events shown beyond 72h along with Time frame.
        """
        pass

    def test_005_based_on_pre_condition_3_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 3 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: Desktop:
        EXPECTED: * Time frame going to display if events are available in Today's tab.
        EXPECTED: Mobile:
        EXPECTED: * Time Frame going to displays according to the Time filters & League Filters configurations in CMS
        """
        pass

    def test_006_based_on_pre_condition_3_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Based on Pre-Condition 3 Navigate to Competitions page.
        EXPECTED: * Time Frame going to displays according to the Time filters configurations in CMS
        """
        pass

    def test_007_based_on_pre_condition_4_navigate_to_sports_landing_page_gt_matches_tab(self):
        """
        DESCRIPTION: Based on Pre-Condition 4 Navigate to Sports Landing Page-&gt; Matches tab.
        EXPECTED: Desktop:
        EXPECTED: * Time frame going to display if events are available in Today's tab.
        EXPECTED: Mobile:
        EXPECTED: * Time Frame going to displays according to the Time filters & League Filters configurations in CMS
        """
        pass

    def test_008_repeat_step_1_7_for_tier_2_sport(self):
        """
        DESCRIPTION: Repeat step 1-7 for tier-2 sport.
        EXPECTED: 
        """
        pass
