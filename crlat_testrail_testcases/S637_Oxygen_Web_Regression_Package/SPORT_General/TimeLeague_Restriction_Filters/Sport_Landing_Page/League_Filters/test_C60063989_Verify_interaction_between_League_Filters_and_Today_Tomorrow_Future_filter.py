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
class Test_C60063989_Verify_interaction_between_League_Filters_and_Today_Tomorrow_Future_filter(Common):
    """
    TR_ID: C60063989
    NAME: Verify interaction between League Filters and Today/Tomorrow/Future filter
    DESCRIPTION: This Test Case verifies interaction between League Filters and Today/Tomorrow/Future filter
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

    def test_001_navigate_to_sports_landing_page_today_tab(self):
        """
        DESCRIPTION: Navigate to Sports Landing page (Today Tab)
        EXPECTED: * League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        EXPECTED: * Filters are not selected or highlighted by default
        """
        pass

    def test_002_switch_to_tomorrowfuture_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow/Future Tab
        EXPECTED: * League Filters Component is not displayed
        """
        pass

    def test_003_switch_back_to_today_tab_and_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Switch back to Today Tab and Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_004_switch_to_tomorrowfuture_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow/Future Tab
        EXPECTED: * League Filters Component is not displayed
        EXPECTED: * Page loads all Tomorrow Events if user switches to Tomorrow tab or Future events if user switches to Future tab
        """
        pass

    def test_005_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to Today Tab
        EXPECTED: * Filters are not selected or highlighted
        EXPECTED: * League Filters Component is displayed with the following filters: 'Top Leagues', 'Test League', 'Invalid League'
        """
        pass

    def test_006_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
