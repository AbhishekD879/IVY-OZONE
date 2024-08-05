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
class Test_C60035088_Verify_Time_Filters_Component_on_Competitions_tab_for_Tier_2_sports(Common):
    """
    TR_ID: C60035088
    NAME: Verify Time Filters Component on Competitions tab for Tier 2 sports
    DESCRIPTION: This test case verifies Time Filters Component on Competitions tab for Tier 2 sports
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours(Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Tier 2 Sport Landing page
    """
    keep_browser_open = True

    def test_001_clicktap_on_the_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Competition' tab
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames:
        EXPECTED: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: ![](index.php?/attachments/get/121591741)
        """
        pass

    def test_002_clicktap_on_the_filter_that_doesnt_fit_within_single_screen(self):
        """
        DESCRIPTION: Click/Tap on the filter that doesn't fit within single screen
        EXPECTED: Time/League Filters is swipable with pretext (Starting In being within fixed position)
        """
        pass

    def test_003_go_to_cms_gt_sports_pages_gt_sport_categories_gt_sport_gt_competitionsdelete_all_filters_except_1_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS &gt; Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions
        DESCRIPTION: Delete all filters except 1 and save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_004_return_to_app_tier2_sport_landing_page_gt_competitionand_look_at_filters(self):
        """
        DESCRIPTION: Return to app Tier2 Sport Landing page &gt; Competition
        DESCRIPTION: and look at filters
        EXPECTED: Just 1 unselected filter is displayed
        """
        pass

    def test_005_select_current_filter(self):
        """
        DESCRIPTION: Select current filter
        EXPECTED: Filtering is applied to events
        """
        pass

    def test_006_go_to_cms_gt_sports_pages_gt_sport_categories_gt_sport_gt_competitionsdisable_time_frame_and_save_a_change(self):
        """
        DESCRIPTION: Go to CMS &gt; Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions
        DESCRIPTION: Disable Time Frame and save a change
        EXPECTED: Change is saved
        """
        pass

    def test_007_return_to_app_tier1_sport_landing_page_gt_competitionand_look_at_filters(self):
        """
        DESCRIPTION: Return to app Tier1 Sport Landing page &gt; Competition
        DESCRIPTION: and look at filters
        EXPECTED: No filters are displayed
        EXPECTED: Events are displayed without filtering
        """
        pass
