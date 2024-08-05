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
class Test_C60063986_Verify_filtering_by_League_Filters_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60063986
    NAME: Verify filtering by League Filters on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by League Filters on Sports Landing Page
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

    def test_002_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_003_select_one_more_filter_eg_test_league(self):
        """
        DESCRIPTION: Select one more filter, e.g. 'Test League'
        EXPECTED: * New selected League Filter is highlighted and the previous one is removed
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_004_click_on_the_selected_test_league_filter(self):
        """
        DESCRIPTION: Click on the selected 'Test League' filter
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_005_select_filter_with_a_range_where_no_available_events_eg_invalid_league(self):
        """
        DESCRIPTION: Select filter with a range where no available events, e.g. 'Invalid League'
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * The message "No events found" is displayed on the current page
        """
        pass

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any Time Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        pass
