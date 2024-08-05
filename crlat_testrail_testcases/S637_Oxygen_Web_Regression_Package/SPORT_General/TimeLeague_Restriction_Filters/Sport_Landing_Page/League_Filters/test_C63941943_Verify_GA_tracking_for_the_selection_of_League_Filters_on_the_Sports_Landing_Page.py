import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C63941943_Verify_GA_tracking_for_the_selection_of_League_Filters_on_the_Sports_Landing_Page(Common):
    """
    TR_ID: C63941943
    NAME: Verify GA tracking  for the selection of League Filters on the Sports Landing Page
    DESCRIPTION: This Test Case verifies League Filters GA tracking on the Sports Landing Page
    PRECONDITIONS: 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Access the application in the browser and click on the inspect option. Select the Console option.
    """
    keep_browser_open = True

    def test_001_navigate_to_the_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to the Sports Landing Page.
        EXPECTED: League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        EXPECTED: Filters are not selected or highlighted by default.
        """
        pass

    def test_002_select_any_of_the_league_filter_which_is_available(self):
        """
        DESCRIPTION: Select any of the League filter which is available.
        EXPECTED: In the Console tab the action of adding or selecting League filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "League Filter"
        EXPECTED: eventCategory: "League filters"
        EXPECTED: eventLabel: "select"
        """
        pass

    def test_003_deselect_the_previously_selected_league_filter(self):
        """
        DESCRIPTION: Deselect the previously selected League filter.
        EXPECTED: In the Console tab the action of de-selecting League filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "League Filter"
        EXPECTED: eventCategory: "League filters"
        EXPECTED: eventLabel: "deselect"
        """
        pass

    def test_004_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
