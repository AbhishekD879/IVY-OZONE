import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C60079323_Verify_the_behavior_of_Market_Selector_dropdown_list(Common):
    """
    TR_ID: C60079323
    NAME: Verify  the  behavior of 'Market Selector' dropdown list
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Choose the 'Basketball' tab
    PRECONDITIONS: 3. Navigate to the 'In-Play' page
    PRECONDITIONS: 4. Be aware that below markets are available in the 'Market Selector' dropdown list
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: Mobile:
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: Desktop:
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change Market' button is placed next to 'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: • 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        pass

    def test_002_tap_on_market_selector(self):
        """
        DESCRIPTION: Tap on Market Selector
        EXPECTED: 'Market Selector' dropdown is displayed
        """
        pass

    def test_003_verify_the_behavior_of_the_market_drop_down_list(self):
        """
        DESCRIPTION: Verify the behavior of the market drop down list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        pass

    def test_004_click_on_the_market_which_is_higlighted(self):
        """
        DESCRIPTION: Click on the market which is higlighted
        EXPECTED: Selected market should be displayed in the dropdown
        """
        pass

    def test_005_tap_on_the_change_button_again_and_mouse_over_content(self):
        """
        DESCRIPTION: Tap on the 'Change' button again and mouse over content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List the Markets will be displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards(Ladbrokes)
        """
        pass
