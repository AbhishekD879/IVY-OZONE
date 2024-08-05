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
class Test_C60037205_Verify_interaction_between_Time_Filters_and_Market_switcher(Common):
    """
    TR_ID: C60037205
    NAME: Verify interaction between Time Filters and Market switcher
    DESCRIPTION: This Test Case verifies interaction between Time Filters and Market switcher
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
    PRECONDITIONS: 2. Navigate to Sports Landing page (Today tab)
    """
    keep_browser_open = True

    def test_001_select_some_time_filter_eg_3_hours(self):
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

    def test_002_select_another_market_from_the_market_switcher(self):
        """
        DESCRIPTION: Select another Market from the Market Switcher
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_003_change_market_from_market_selector_where_no_events_present_or_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change market from Market Selector, where no events present or events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        pass

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Default Market is displayed in the Market Switcher
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_005_select_another_market_from_the_market_switcher(self):
        """
        DESCRIPTION: Select another Market from the Market Switcher
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Page loads only events that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_006_select_some_time_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select some Time Filter, e.g. 12 hours
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Market is displayed in the Market Switcher
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport AND that in line with selected Market
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_007_change_time_filter_where_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change Time Filter, where events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        pass

    def test_008_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
