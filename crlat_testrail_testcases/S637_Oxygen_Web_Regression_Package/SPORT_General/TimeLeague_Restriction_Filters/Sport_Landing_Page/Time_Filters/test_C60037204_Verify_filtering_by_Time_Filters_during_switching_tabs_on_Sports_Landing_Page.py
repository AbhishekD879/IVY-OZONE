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
class Test_C60037204_Verify_filtering_by_Time_Filters_during_switching_tabs_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60037204
    NAME: Verify filtering by Time Filters during switching tabs on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by Time Filters during switching tabs on Sports Landing Page
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **Time Filters are available for Desktop only up to 12 hours and only on Today Tab**
    PRECONDITIONS: 1. Load the app
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to Sports Landing page
        EXPECTED: **For Mobile:**
        EXPECTED: * Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: * Filters are not selected or highlighted by default
        EXPECTED: **For Desktop:**
        EXPECTED: * Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: * Filters are not selected or highlighted by default
        """
        pass

    def test_002_select_some_time_filter_eg_3_hours(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. 3 hours)
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_003_switch_to_another_tab_eg_in_play(self):
        """
        DESCRIPTION: Switch to another tab (e.g. In-Play)
        EXPECTED: * Time Filters Component is not displayed on the In-Play tab
        EXPECTED: * All In-Play Events are displayed without filtering by Time Filter
        """
        pass

    def test_004_switch_back_to_matches_tab(self):
        """
        DESCRIPTION: Switch back to Matches tab
        EXPECTED: * Time Filters Component is displayed with the following time frames: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours
        EXPECTED: * Filters are not selected or highlighted by default
        EXPECTED: * All Events are displayed without filtering by Time Filter
        """
        pass

    def test_005_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
