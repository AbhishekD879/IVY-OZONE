import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C60658036_Verify_MS_on_Inplay_Tab_for_Basketball_for_Multiple_bet_placement(Common):
    """
    TR_ID: C60658036
    NAME: Verify MS on Inplay Tab for Basketball for Multiple bet placement
    DESCRIPTION: This test case verifies 'Market Selector' drop down displaying for Basketball on in-Play page (SLP-Basketball ->Inplay Tab) and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB using the following market Templates:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **Mobile:**
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: **Desktop:**
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change Market' button is placed next to  'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: • 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        pass

    def test_002_click_on_the_change_market_button_to_verify_options_available_for_basketball_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on the 'Change Market' button to verify options available for Basketball in the Market selector dropdown
        EXPECTED: Market selector drop down becomes expanded (with chevron/arrow pointing upwards) with the below listed markets:
        EXPECTED: * Main Markets
        EXPECTED: • Money Line
        EXPECTED: • Total Points
        EXPECTED: • Handicap (Handicap in Lads and Spread in coral)
        EXPECTED: • Current Half Total Points
        EXPECTED: • Current Quarter Total Points
        EXPECTED: •If any Market is not available it is not displayed in the Market selector drop-down list*
        """
        pass

    def test_003_verify_bet_placement_for_multiple_bet_for_the_below_markets_money_line_total_points_handicap_handicap_in_lads_and_spread_in_coral_current_half_total_points_current_quarter_total_points(self):
        """
        DESCRIPTION: Verify Bet Placement for multiple Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Total Points
        DESCRIPTION: • Handicap (Handicap in Lads and Spread in coral)
        DESCRIPTION: • Current Half Total Points
        DESCRIPTION: • Current Quarter Total Points
        EXPECTED: Bet should be placed successfully
        """
        pass
