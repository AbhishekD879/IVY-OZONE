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
class Test_C60075249_Verify_Market_Selector_dropdown_list_on_Basketball_Specific_Competition_Page(Common):
    """
    TR_ID: C60075249
    NAME: Verify 'Market Selector' dropdown list on Basketball Specific Competition Page
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Basketball Specific Competition Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Competition Tab -> 'Click on Specific Competition'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        pass

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Money Line
        EXPECTED: • Total Points
        EXPECTED: • Handicap (Handicap in Lads and Spread in Coral)
        EXPECTED: • Home Team Total Points
        EXPECTED: • Away Team Total Points
        EXPECTED: • Current Half Total Points
        EXPECTED: • Current Quarter Total Points
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        pass

    def test_003_select_total_points_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        pass

    def test_004_repeat_step_3_for_the_following_markets_money_line_handicap_handicap_in_lads_and_spread_in_coral_home_team_total_points_away_team_total_points_current_half_total_points_current_quarter_total_points(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Money Line
        DESCRIPTION: • Handicap (Handicap in Lads and Spread in Coral)
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        DESCRIPTION: • Current Half Total Points
        DESCRIPTION: • Current Quarter Total Points
        EXPECTED: 
        """
        pass
