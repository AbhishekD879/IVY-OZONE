import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60063708_Verify_filtering_by_Time_Filters_for_Tier_2_Sports_without_Market_Selector_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60063708
    NAME: Verify filtering by Time Filters for Tier 2 Sports without Market Selector  on Sports Landing Page
    DESCRIPTION: This test case verifies filtering by Time Filters for Tier 2 Sports without Market Selector  on Sports Landing Page
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
    PRECONDITIONS: 2. Navigate to Sports Landing page (market selector should be absent for this sport), e.g. Cricket
    """
    keep_browser_open = True

    def test_001_select_filter_eg_3_hour(self):
        """
        DESCRIPTION: Select filter, e.g. 3 hour
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

    def test_002_click_on_the_selected_time_filter(self):
        """
        DESCRIPTION: Click on the selected time filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_003_select_filter_eg_6_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 6 hours
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 6 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 6 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass
