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
class Test_C60075515_Verify_previously_selected_Handicap_WW_Market_Template_is_saved_when_user_is_switching_between_Today_Tomorrow_Future_in_Matches_tab_in_Ice_Hockey_Landing_Page(Common):
    """
    TR_ID: C60075515
    NAME: Verify previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future in Matches tab in Ice Hockey Landing Page
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future in Matches tab in Ice Hockey Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3)etc using the following Market Template Names:
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
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
        EXPECTED: • Primary market is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Puck Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Puck Line' in 'Market selector' **Coral**
        """
        pass

    def test_002_select_puck_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Puck Line' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        """
        pass

    def test_003_verify_text_of_the_labels_for_puck_line_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Puck Line' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label Over & Under.
        """
        pass

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        pass

    def test_005_verify_ga_tracking_for_the_puck_line(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Puck Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: 'Puck Line'
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        pass

    def test_006_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Puck Line)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note: If events are not present for 'Puck Line' market and if events are present for 'Total Goals 2-way' market then 'Total Goals 2-way' will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display
        """
        pass

    def test_007_repeat_steps_45(self):
        """
        DESCRIPTION: Repeat steps 4,5
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_456_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 4,5,6 for the 'Future' tab
        EXPECTED: 
        """
        pass

    def test_009_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        pass

    def test_010_repeat_steps_2_9_for_the_below_markets_total_goals_2_wayexcept_validating_the_labels_from_step_9(self):
        """
        DESCRIPTION: Repeat steps 2-9 for the below markets
        DESCRIPTION: • Total Goals 2-way(except validating the labels from step 9)
        EXPECTED: 
        """
        pass

    def test_011_verify_text_of_the_labels_for_total_goals_2_way_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Goals 2-way' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under
        """
        pass
