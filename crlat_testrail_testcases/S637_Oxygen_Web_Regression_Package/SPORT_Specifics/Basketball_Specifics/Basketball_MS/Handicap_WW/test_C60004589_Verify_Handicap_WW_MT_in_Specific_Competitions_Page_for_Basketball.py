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
class Test_C60004589_Verify_Handicap_WW_MT_in_Specific_Competitions_Page_for_Basketball(Common):
    """
    TR_ID: C60004589
    NAME: Verify ‘Handicap WW’ MT in Specific Competitions Page for Basketball
    DESCRIPTION: This test case verifies the behavior of Handicap WW market’ Template in Specific Competition Page
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing Page -> Click on 'Specific Competition Page'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3)etc  using the following Market Template Names:
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under) | - "Quarter Total Points"
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Total Points' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Points' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Total Points' in 'Market selector' Coral
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Total Points
        EXPECTED: • Handicap (handicap in Lads and Spread in coral)
        EXPECTED: • Home Team Total Points
        EXPECTED: • Away Team Total Points
        EXPECTED: • Half Total Points
        EXPECTED: • Quarter Total Points
        """
        pass

    def test_003_select_total_points_in_the_market_selector_dropdown_list(self):
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
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        pass

    def test_004_verify_displaying_of_preplayinplay_or_both_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay/Inplay or both events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Total Points (Preplay and Inplay)
        EXPECTED: • Handicap (handicap in Lads and Spread in coral) (Preplay and Inplay)
        EXPECTED: • Home Team Total Points (Preplay and Inplay)
        EXPECTED: • Away Team Total Points (Preplay and Inplay)
        EXPECTED: • Half Total Points (Preplay and Inplay)
        EXPECTED: • Quarter Total Points (Preplay and Inplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        pass

    def test_005_verify_text_of_the_labels_for_total_points(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under.
        """
        pass

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        pass

    def test_007_verify_ga_tracking_for_the_games_total(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Games Total'
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

    def test_008_repeat_3_7_steps_for_the_below_markets_total_points_handicap_expect_step_5_home_team_total_points_away_team_total_points_half_total_points_quarter_total_points(self):
        """
        DESCRIPTION: Repeat 3-7 steps for the below markets
        DESCRIPTION: • Total Points
        DESCRIPTION: • Handicap (expect step 5)
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        DESCRIPTION: • Half Total Points
        DESCRIPTION: • Quarter Total Points
        EXPECTED: 
        """
        pass

    def test_009_verify_text_of_the_labels_for_handicap_handicap_in_lads_and_spread_in_coral(self):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap' (Handicap in Lads and Spread in Coral)
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
        """
        pass
