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
class Test_C60075400_Verify_previously_selected_option_state_is_saved_in_Market_Selector_after_switching_between_Today_Tomorrow_Future_tabs_on_Football_landing_page(Common):
    """
    TR_ID: C60075400
    NAME: Verify previously selected option state is saved in 'Market Selector' after switching between Today/Tomorrow/Future tabs on Football landing page
    DESCRIPTION: This test case verifies that previously selected option state is saved in 'Market Selector' after switching between Today/Tomorrow/Future tabs on Football landing page
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match result' in 'Market selector' **Coral**
        """
        pass

    def test_002_select_any_other_market_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select any other market in the 'Market Selector' dropdown list
        EXPECTED: * The events for the selected market are shown
        EXPECTED: * Values on Odds Header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_003_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: * Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Odds Header are displayed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are displayed for each event according to selected market
        """
        pass

    def test_004_repeat_step_3_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat step 3 for the 'Future' tab
        EXPECTED: 
        """
        pass

    def test_005_select_the_market_that_is_not_present_in_the_market_selector_dropdown_list_for_some_tab_for_example_to_qualify_is_present_on_today_but_absent_on_tomorrow_tab_(self):
        """
        DESCRIPTION: Select the market that is NOT present in the 'Market Selector' dropdown list for some tab (For example, 'To Qualify' is present on 'Today' but absent on 'Tomorrow' tab )
        EXPECTED: * The events for the selected market are shown
        EXPECTED: * Values on Odds Header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_006_switch_to_the_tab_where_the_selected_market_is_not_present_in_market_selector_dropdown_list_eg_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the tab where the selected market is not present in 'Market Selector' dropdown list (e.g. 'Tomorrow' tab)
        EXPECTED: * 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: * The events for the selected market are shown
        EXPECTED: * Values on Odds Header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_007_switch_back_to_the_tab_from_step_5_eg_today_tab(self):
        """
        DESCRIPTION: Switch back to the tab from step 5 (e.g. 'Today' tab)
        EXPECTED: * Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Odds Header are displayed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are displayed for each event according to selected market
        """
        pass
