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
class Test_C60075273_Verify_previously_selected_option_state_is_saved_in_Market_Selector_after_switching_between_Today_Tomorrow_Future_tabs_on_Rugby_Union_landing_page(Common):
    """
    TR_ID: C60075273
    NAME: Verify previously selected option state is saved in 'Market Selector' after switching between Today/Tomorrow/Future tabs on Rugby Union  landing page
    DESCRIPTION: This test case verifies that previously selected option state is saved in 'Market Selector' after switching between Today/Tomorrow/Future tabs on Rugby Union landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Rugby Union Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting (WDW)| - "Match Result"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap 2-way"
    PRECONDITIONS: * |Total Match Points (Over/Under)| - "Total Points"
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
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        pass

    def test_002_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for the selected market are shown
        EXPECTED: • Values on Odds Header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_003_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected 'Match Result' option is displayed in the 'Market Selector' dropdown
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Odds Header are displayed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are displayed for each event according to selected market
        EXPECTED: Note:
        EXPECTED: If events are not present for 'Match Result' market and if events are present for Handicap 2-way or Total Points market then Handicap 2-way or Total Points will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        pass

    def test_004_repeat_step_3_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat step 3 for the 'Future' tab
        EXPECTED: 
        """
        pass

    def test_005_select_the_market_that_is_not_present_in_the_market_selector_dropdown_list_for_some_tab_for_example_total_points_is_present_on_today_but_absent_on_tomorrow_tab_(self):
        """
        DESCRIPTION: Select the market that is NOT present in the 'Market Selector' dropdown list for some tab (For example, 'Total Points' is present on 'Today' but absent on 'Tomorrow' tab )
        EXPECTED: Today Tab:
        EXPECTED: • The events for the 'Total Points' market are shown
        EXPECTED: • Values on Odds Header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_006_switch_to_the_tab_where_the_total_points_market_is_not_present_in_market_selector_dropdown_list_eg_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the tab where the 'Total Points' market is not present in 'Market Selector' dropdown list (e.g. 'Tomorrow' tab)
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • The events for the selected market are shown
        EXPECTED: • Values on Odds Header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_007_switch_to_todayfuture_tab_total_points_is_present(self):
        """
        DESCRIPTION: Switch to Today/Future tab (Total Points is present)
        EXPECTED: • Previously selected 'Total Points' option is displayed in the 'Market Selector' dropdown
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Odds Header are displayed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are displayed for each event according to selected market
        """
        pass

    def test_008_repeat_steps_1_7_for_the_below_markets_handicap_2_way_total_points(self):
        """
        DESCRIPTION: Repeat steps 1-7 for the below markets:
        DESCRIPTION: • Handicap 2 way
        DESCRIPTION: • Total Points
        EXPECTED: 
        """
        pass
