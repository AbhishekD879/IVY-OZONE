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
class Test_C60079321_Verify_Market_Selector_drop_down_displaying_for_Basketball_on_in_Play_page(Common):
    """
    TR_ID: C60079321
    NAME: Verify 'Market Selector' drop down displaying for Basketball  on in-Play page
    DESCRIPTION: This test case verifies 'Market Selector' drop down displaying for Basketball on in-Play page
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
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

    def test_003_click_on_somewhere_outside_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on somewhere outside the Market Selector dropdown
        EXPECTED: 'Market Selector' dropdown becomes collapsed
        """
        pass

    def test_004_select_upcoming_tab_from_the_in_play_sports_ribbon_menu(self):
        """
        DESCRIPTION: Select Upcoming tab from the 'In-Play Sports Ribbon' menu
        EXPECTED: The 'Market Selector' is not available
        """
        pass
