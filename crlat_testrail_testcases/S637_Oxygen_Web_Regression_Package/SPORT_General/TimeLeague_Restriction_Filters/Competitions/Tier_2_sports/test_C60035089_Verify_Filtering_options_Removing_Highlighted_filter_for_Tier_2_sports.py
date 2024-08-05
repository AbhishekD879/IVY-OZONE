import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60035089_Verify_Filtering_options_Removing_Highlighted_filter_for_Tier_2_sports(Common):
    """
    TR_ID: C60035089
    NAME: Verify Filtering options,  Removing Highlighted filter  for Tier 2 sports
    DESCRIPTION: This test case verifies Filtering options, Removing Highlighted filter for Tier 2 sports
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours, 2 hours(custom added), 21 hours(custom added)(Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
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
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        pass

    def test_002_select_filter_eg_3_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 3 hours
        EXPECTED: - Page loads only events that are due to start within the next 3 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        pass

    def test_003_select_one_more_filter_eg_24_hours(self):
        """
        DESCRIPTION: Select one more filter, e.g. 24 hours
        EXPECTED: - New Time Filter is highlighted and the previous one is removed
        EXPECTED: - Page loads only events that are due to start within the next 24 hours for that given league
        EXPECTED: - Events are sorted by time
        """
        pass

    def test_004_click_on_the_selected_time_filter_to_remove_highlight(self):
        """
        DESCRIPTION: Click on the selected time filter to remove highlight
        EXPECTED: User returns to default view
        """
        pass

    def test_005_select_filter_with_a_range_where_no_available_events_eg_1_hour(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 1 hour
        EXPECTED: The message "No events found" is displayed on current page
        """
        pass
