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
class Test_C60035083_Verify_interaction_between_Market_switcher_and_Time_Frame_for_Tier_1_sports(Common):
    """
    TR_ID: C60035083
    NAME: Verify interaction between Market switcher and Time Frame for Tier 1 sports
    DESCRIPTION: This test case verifies interaction between the Market switcher and Time Frame for Tier 1 sports
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours(Sports Pages &gt; Sports Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Tier1 Sport Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
    """
    keep_browser_open = True

    def test_001_clicktap_on_some_league(self):
        """
        DESCRIPTION: Click/Tap on some League
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

    def test_003_change_market_from_market_selector(self):
        """
        DESCRIPTION: Change market from Market Selector
        EXPECTED: - Markets update to reflect the change in market, in line with the time/league filter selected by user
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        EXPECTED: - Selected market is displayed
        """
        pass

    def test_004_change_market_from_market_selector_where_no_events_present_or_events_from_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change market from Market Selector, where no events present or events from selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        pass

    def test_005_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering by time and market would not be applied to newly selected tab
        """
        pass

    def test_006_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering by time and market that previously applied is reset
        """
        pass

    def test_007_change_market_from_market_selector(self):
        """
        DESCRIPTION: Change market from Market Selector
        EXPECTED: Markets update to reflect the change in market
        """
        pass

    def test_008_select_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 12 hours
        EXPECTED: - Events update to be in line with filter selected as well as the market selected by user
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        EXPECTED: - Selected market is displayed
        """
        pass

    def test_009_change_time_filter_where_events_from_the_selected_time_frame_arent_available(self):
        """
        DESCRIPTION: Change Time Filter, where events from the selected time frame aren't available
        EXPECTED: The message "No events found" is displayed on the current page
        """
        pass
