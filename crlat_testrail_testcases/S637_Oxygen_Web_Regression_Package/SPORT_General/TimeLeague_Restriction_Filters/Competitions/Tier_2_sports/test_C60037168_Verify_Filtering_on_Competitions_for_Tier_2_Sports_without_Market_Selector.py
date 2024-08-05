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
class Test_C60037168_Verify_Filtering_on_Competitions_for_Tier_2_Sports_without_Market_Selector(Common):
    """
    TR_ID: C60037168
    NAME: Verify Filtering on Competitions for Tier 2 Sports without Market Selector
    DESCRIPTION: This test case verifies  Filtering on Competitions for Tier 2 Sports without Market Selector
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: * SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - List of Sports
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page (market selector should be absent for this sport), e.g. Cricket
    """
    keep_browser_open = True

    def test_001_clicktap_on_the_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on the 'Competition' tab
        EXPECTED: - Market selector is absent
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        pass

    def test_002_select_filter_eg_1_hour(self):
        """
        DESCRIPTION: Select filter, e.g. 1 hour
        EXPECTED: - Page loads only events that are due to start within the next 1 hour for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        pass

    def test_003_click_on_the_selected_time_filter_to_remove_highlight(self):
        """
        DESCRIPTION: Click on the selected time filter to remove highlight
        EXPECTED: User returns to the default view
        """
        pass

    def test_004_select_filter_eg_6_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 6 hours
        EXPECTED: - Page loads only events that are due to start within the next 6 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        pass

    def test_005_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering would not be applied to newly selected tab
        """
        pass

    def test_006_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering that previously applied is reset
        """
        pass
