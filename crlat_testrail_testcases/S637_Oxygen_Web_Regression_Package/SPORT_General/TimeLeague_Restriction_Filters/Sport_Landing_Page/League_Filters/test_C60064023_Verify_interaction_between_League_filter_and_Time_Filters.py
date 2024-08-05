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
class Test_C60064023_Verify_interaction_between_League_filter_and_Time_Filters(Common):
    """
    TR_ID: C60064023
    NAME: Verify interaction between League filter and Time Filters
    DESCRIPTION: This Test Case verifies interaction between League filter and Time Filters
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages &gt; Sport Categories &gt; Sport &gt; Matches)
    PRECONDITIONS: * SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **Time Filters are available for Desktop only on Today Tab**
    PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
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

    def test_002_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 3 hours AND that in line with 'Top Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours AND that in line with 'Top Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_003_click_the_selected_time_filter(self):
        """
        DESCRIPTION: Click the Selected Time Filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only that in line with 'Top Leagues' League Filter for that given Sport without time filtering
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_004_select_another_league_filter_eg_test_league(self):
        """
        DESCRIPTION: Select another League Filter (e.g. 'Test League')
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only that in line with 'Test Leagues' League Filter for that given Sport without time filtering
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_005_select_some_time_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select some Time Filter (e.g. 12 hours)
        EXPECTED: **For Mobile:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events (Upcoming Matches List only) that are due to start within the next 12 hours AND that in line with 'Test Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        EXPECTED: **For Desktop:**
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 12 hours AND that in line with 'Test Leagues' League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_006_select_another_league_filter_eg_invalid_league(self):
        """
        DESCRIPTION: Select another League Filter (e.g. 'Invalid League')
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any League Filter is not highlighted
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads with all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_008_select_some_time_filter_where_events_from_selected_time_frame_arent_available_eg_1_hoursselect_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some Time Filter where events from selected time frame aren't available (e.g. 1 hours)
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        pass

    def test_009_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
