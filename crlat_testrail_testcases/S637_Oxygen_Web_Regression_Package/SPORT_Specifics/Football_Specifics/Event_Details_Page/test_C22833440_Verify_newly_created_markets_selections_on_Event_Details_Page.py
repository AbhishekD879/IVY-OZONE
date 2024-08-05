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
class Test_C22833440_Verify_newly_created_markets_selections_on_Event_Details_Page(Common):
    """
    TR_ID: C22833440
    NAME: Verify newly created markets & selections on Event Details Page
    DESCRIPTION: This test case verifies automatically displaying newly created markets/selections on In-Play/Pre-Match Football Event Details Page
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Live and Pre Match events are available
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_in_playpre_match_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to In-Play/Pre-Match event Details page of football event
        EXPECTED: - Event Details page is opened
        EXPECTED: - Main Markets collection is opened by default
        EXPECTED: - Corresponding markets are displayed
        """
        pass

    def test_003_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        EXPECTED: All available markets are displayed
        """
        pass

    def test_004_in_ti_tool_create_new_market_without_selections_verify_event_details_page(self):
        """
        DESCRIPTION: In TI tool: Create new market (without selections)> Verify Event Details page
        EXPECTED: Newly created market is NOT displayed
        """
        pass

    def test_005_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly created market is NOT displayed
        """
        pass

    def test_006_in_ti_tool_add_selections_to_the_newly_created_market_in_step_4__in_application_verify_opened_event_details_page_of_football_event(self):
        """
        DESCRIPTION: In TI tool: Add selection(s) to the newly created market (in step 4) > In application: Verify opened Event Details page of football event
        EXPECTED: - Newly created market with selections automatically appears on the page
        EXPECTED: - All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        EXPECTED: - For In-Play football event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appear
        EXPECTED: - If new market belongs to a new collection, the collection automatically appears along with the market
        """
        pass

    def test_007_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Already created market is displayed with selection(s) in corresponding collection
        """
        pass

    def test_008_refresh_event_details_page_of_football_event_in_ti_tool_add_another_selection_to_the_market_from_step_4__in_application_verify_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: Refresh Event Details page of football event >
        DESCRIPTION: In TI tool: Add another selection to the market (from step 4) > In application: Verify Event Details page of <Sport> event
        EXPECTED: Newly created selection automatically appears on the page for a corresponding market
        """
        pass

    def test_009_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        EXPECTED: All available markets are displayed
        """
        pass

    def test_010_in_ti_tool_create_new_market_with_selections_in_application_verify_opened_event_details_page_of_football_event(self):
        """
        DESCRIPTION: In TI tool: Create new market with selections> In application: Verify opened Event Details page of Football event
        EXPECTED: - Newly created market with selections automatically appears on the page
        EXPECTED: All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        EXPECTED: - For In-Play event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appears
        EXPECTED: - If new market belongs to a new collection, the collection automatically appears along with the market
        """
        pass

    def test_011_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly created market is displayed with selections in corresponding collections
        """
        pass

    def test_012_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        EXPECTED: All available markets are displayed
        """
        pass

    def test_013_in_ti_tool_add_combined_market_without_selectionsin_application_verify_opened_event_details_page_of_event(self):
        """
        DESCRIPTION: In TI tool: Add combined market without selections>In application: Verify opened Event Details page of event
        EXPECTED: Newly created market is NOT displayed
        """
        pass

    def test_014_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly created combined market is NOT displayed
        """
        pass

    def test_015_in_ti_tool_add_selections_to_one_market_within_combined_markets_group__in_application_verify_opened_event_details_page_of_event(self):
        """
        DESCRIPTION: In TI tool: Add selection(s) to one market within combined markets group > In application: Verify opened Event Details page of event
        EXPECTED: - Newly created combined market automatically appears on the page
        EXPECTED: - Added selection(s) is/are displayed for a corresponding market within combined markets group
        EXPECTED: - No selections are shown for other markets within combined markets group
        EXPECTED: - All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        EXPECTED: - For In-Play football event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appears
        EXPECTED: - If new market belongs to a new collection, the collection automatically appears along with the market
        """
        pass

    def test_016_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly created combined market is displayed with selection(s) in corresponding collections
        """
        pass

    def test_017_refresh_event_details_page_of_football_event_in_ti_tool_add_another_selection_to_the_available_combined_market__in_application_verify_event_details_page_of_event(self):
        """
        DESCRIPTION: Refresh Event Details page of football event >
        DESCRIPTION: In TI tool: Add another selection to the available combined market > In application: Verify Event Details page of event
        EXPECTED: Newly created selection automatically appears on the page for a corresponding combined market
        """
        pass

    def test_018_in_ti_tool_add_selections_to_other_markets_within_combined_markets_group__verify_event_details_page_of_event(self):
        """
        DESCRIPTION: In TI tool: Add selection(s) to other market(s) within combined markets group > Verify Event Details page of event
        EXPECTED: - Сombined market automatically reappears on the page
        EXPECTED: - Added selection(s) is/are displayed for a corresponding market within combined markets group
        EXPECTED: - All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        EXPECTED: - For In-Play football event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appears
        EXPECTED: - If new market belongs to a new collection, the collection automatically appears along with the market
        """
        pass

    def test_019_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly created combined market is displayed with selection(s) in corresponding collections
        """
        pass
