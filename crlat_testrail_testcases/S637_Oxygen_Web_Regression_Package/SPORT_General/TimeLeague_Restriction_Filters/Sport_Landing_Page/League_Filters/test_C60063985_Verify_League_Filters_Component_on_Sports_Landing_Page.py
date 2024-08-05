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
class Test_C60063985_Verify_League_Filters_Component_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60063985
    NAME: Verify League Filters Component on Sports Landing Page
    DESCRIPTION: This Test Case verifies League Filters Component on Sports Landing Page
    PRECONDITIONS: * 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: * SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
    PRECONDITIONS: 1. Load the app
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: * League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        EXPECTED: * Filters are not selected or highlighted by default
        """
        pass

    def test_002_go_to_cms_gt_sports_pages_gt_sport_categories_gt_sport_gt_matchesdelete_all_filters_except_1_eg_top_leaguessave_changes(self):
        """
        DESCRIPTION: Go to CMS &gt; Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches
        DESCRIPTION: Delete all filters except 1 (e.g. 'Top Leagues')
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_003_return_to_sports_landing_page(self):
        """
        DESCRIPTION: Return to Sports Landing page
        EXPECTED: * League Filters Component is displayed with the only one filter: 'Top Leagues'
        EXPECTED: * Filter is not selected or highlighted by default
        """
        pass

    def test_004_go_to_cms__gt_system_configuration__gt_structure__gt_featuretoggledisable_the_sporteventfilters_checkboxsave_the_changes(self):
        """
        DESCRIPTION: Go to CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle
        DESCRIPTION: Disable the SportEventFilters checkbox
        DESCRIPTION: Save the Changes
        EXPECTED: Changes are saved
        """
        pass

    def test_005_return_to_sports_landing_page(self):
        """
        DESCRIPTION: Return to Sports Landing page
        EXPECTED: League Filters Component is not displayed
        """
        pass

    def test_006_go_to_cms__gt_system_configuration__gt_structure__gt_featuretoggleenable_the_sporteventfilters_checkboxsave_the_changes(self):
        """
        DESCRIPTION: Go to CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle
        DESCRIPTION: Enable the SportEventFilters checkbox
        DESCRIPTION: Save the Changes
        EXPECTED: Changes are saved
        """
        pass

    def test_007_go_to_cms_gt_sports_pages_gt_sport_categories_gt_sport_gt_matchesdisable_the_enabled_league_filters_checkboxsave_changes(self):
        """
        DESCRIPTION: Go to CMS &gt; Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches
        DESCRIPTION: Disable the 'Enabled League Filters' checkbox
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_008_return_to_sports_landing_page(self):
        """
        DESCRIPTION: Return to Sports Landing page
        EXPECTED: -League Filters Component is not displayed
        EXPECTED: -But Time Filters Component is displayed
        """
        pass

    def test_009_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
