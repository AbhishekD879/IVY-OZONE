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
class Test_C849464_Verify_automatically_displaying_undisplayed_markets_selections_on_Sport_event_details_page(Common):
    """
    TR_ID: C849464
    NAME: Verify automatically displaying undisplayed markets & selections on <Sport> event details page
    DESCRIPTION: This test case verifies automatically displaying undisplayed markets/selections on In-Play/Pre-Match <Sport> Event Details Page
    DESCRIPTION: ***JIRA tickets:***
    DESCRIPTION: BMA-22577 Create builder service for newly created markets/selections
    PRECONDITIONS: - Live and Pre Match events are available
    PRECONDITIONS: - To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_in_playpre_match_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: Go to In-Play/Pre-Match event Details page of <Sport> event
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

    def test_004_in_ti_tool_create_undisplayed_market_plus_undisplayed_selection_for_opened_sport_event(self):
        """
        DESCRIPTION: In TI tool: Create undisplayed market + undisplayed selection for opened <Sport> event
        EXPECTED: Undisplayed market & selection are created in TI tool
        """
        pass

    def test_005_in_application_do_not_refresh_sport_event_details_page(self):
        """
        DESCRIPTION: In application: Do not refresh <Sport> event details page
        EXPECTED: Event Details page is opened
        """
        pass

    def test_006_in_ti_tool_display_market_then_display_selection_for_opened_sport_event(self):
        """
        DESCRIPTION: In TI tool: Display market then display selection for opened <Sport> event
        EXPECTED: Market and its selection are displayed
        """
        pass

    def test_007_in_application_verify_opened_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: In application: Verify opened Event Details page of <Sport> event
        EXPECTED: - Displayed market with selections automatically appear on the page
        EXPECTED: - All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        EXPECTED: - For In-Play <Sport> event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appear
        EXPECTED: - If new market belongs to a new collection, the collection automatically appears along with the market
        """
        pass

    def test_008_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly displayed market is visible with selections in corresponding collections
        """
        pass

    def test_009_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        EXPECTED: All available markets are displayed
        """
        pass

    def test_010_in_ti_tool_create_undisplayed_market_of_sport_event__then_display_market__add_displayed_selection_to_it(self):
        """
        DESCRIPTION: In TI tool: Create undisplayed market of <Sport> event > then display market > add displayed selection to it
        EXPECTED: Selection is added to an undisplayed market of a <Sport> event
        """
        pass

    def test_011_in_application_verify_opened_event_details_page_of_sport_event(self):
        """
        DESCRIPTION: In application: Verify opened Event Details page of <Sport> event
        EXPECTED: - Displayed market with selections automatically appear on the page
        EXPECTED: - All other markets are displayed in their actual state (expanded or collapsed)
        EXPECTED: - If order of newly created market is > 2, the market is shown collapsed
        EXPECTED: - If order of newly created market is < 2, the market is shown expanded
        EXPECTED: - For In-Play <Sport> event details page: Only Markets with attribute isMarketBetInRun="true" on the market level automatically appear
        EXPECTED: - If new market belongs to a new collection, the collection automatically appears along with the market
        """
        pass

    def test_012_navigate_through_available_collections(self):
        """
        DESCRIPTION: Navigate through available collections
        EXPECTED: Newly displayed market is visible with selections in corresponding collections
        """
        pass
