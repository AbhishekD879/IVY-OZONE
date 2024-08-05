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
class Test_C60079467_Verify_previously_selected_Handicap_WW_Market_Template_is_saved_when_user_is_switching_between_Today_Tomorrow_Future_on_Basketball_Landing_Page(Common):
    """
    TR_ID: C60079467
    NAME: Verify previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Basketball Landing Page
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Basketball Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Total Points' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Points' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Total Points' in 'Market selector' **Coral**
        """
        pass

    def test_002_select_total_points_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
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

    def test_003_verify_text_of_the_labels_for_total_points_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        """
        pass

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        pass

    def test_005_verify_ga_tracking_for_the_total_points(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Total Points'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Total Points"
        EXPECTED: categoryID: "6"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        pass

    def test_006_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Total Points)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        EXPECTED: Note: If events are not present for Total Points market and if events are present for either Home Team Total Points/Away Team Total Points/Handicap  markets then those markets will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
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
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under
        """
        pass

    def test_010_repeat_steps_2_9_for_the_below_markets_home_team_total_points_away_team_total_points_handicap_except_step_3(self):
        """
        DESCRIPTION: Repeat steps 2-9 for the below markets
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        DESCRIPTION: • Handicap (except step 3)
        EXPECTED: 
        """
        pass

    def test_011_verify_text_of_the_labels_for_handicap_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        pass
