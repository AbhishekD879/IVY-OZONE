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
class Test_C63943057_Verify_GA_tracking_for_the_selection_of_Time_Filters_on_the_Competitions_Page_for_Tier_1_sports(Common):
    """
    TR_ID: C63943057
    NAME: Verify GA tracking for the selection of Time Filters on the Competitions Page for Tier 1 sports
    DESCRIPTION: This Test Case verifies Time Filters GA tracking on the Competitions Page for the Tier 1 sports.
    PRECONDITIONS: 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages &gt; Sport Categories &gt; Tier 1 Sport &gt; Competitions Tab )
    PRECONDITIONS: SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Access the application in the browser and click on the inspect option. Select the Console option.
    """
    keep_browser_open = True

    def test_001_navigate_to_tier_1___sports_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Tier 1 - Sports Landing page - Competitions tab.
        EXPECTED: Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: Filters are not selected or highlighted by default
        EXPECTED: For Desktop:
        EXPECTED: Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: Filters are not selected or highlighted by default
        """
        pass

    def test_002_select_any_of_the_time_filter_which_is_available(self):
        """
        DESCRIPTION: Select any of the Time filter which is available.
        EXPECTED: In the Console tab the action of adding or selecting time filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "1h; 3h; 5h"
        EXPECTED: eventCategory: "Time filters"
        EXPECTED: eventLabel: "select"
        """
        pass

    def test_003_deselect_the_previously_selected_time_filter(self):
        """
        DESCRIPTION: Deselect the previously selected Time filter.
        EXPECTED: In the Console tab the action of de-selecting time filter should be tracked or captured.
        EXPECTED: Details to be captured
        EXPECTED: categoryID: "Sports Category ID"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "1h; 3h; 5h"
        EXPECTED: eventCategory: "Time filters"
        EXPECTED: eventLabel: "deselect"
        """
        pass
