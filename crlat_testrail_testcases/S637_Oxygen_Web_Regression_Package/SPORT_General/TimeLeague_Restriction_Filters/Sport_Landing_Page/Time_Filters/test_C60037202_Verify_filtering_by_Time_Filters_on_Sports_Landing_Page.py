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
class Test_C60037202_Verify_filtering_by_Time_Filters_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60037202
    NAME: Verify filtering by Time Filters on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by Time Filters on Sports Landing Page
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

    def test_003_for_mobileselect_one_more_filter_eg_24_hoursfor_desktopselect_one_more_filter_eg_12_hours(self):
        """
        DESCRIPTION: **For Mobile:**
        DESCRIPTION: Select one more filter, e.g. 24 hours
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Select one more filter, e.g. 12 hours
        EXPECTED: **For Mobile:**
        EXPECTED: * New selected Time Filter is highlighted and the previous one is removed
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 24 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * New selected Time Filter is highlighted and the previous one is removed
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 12 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_004_click_on_the_selected_time_filter(self):
        """
        DESCRIPTION: Click on the selected time filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_005_select_filter_with_a_range_where_no_available_events_eg_1_hour(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 1 hour
        EXPECTED: The message "No events found" is displayed on the current page
        """
        pass

    def test_006_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
