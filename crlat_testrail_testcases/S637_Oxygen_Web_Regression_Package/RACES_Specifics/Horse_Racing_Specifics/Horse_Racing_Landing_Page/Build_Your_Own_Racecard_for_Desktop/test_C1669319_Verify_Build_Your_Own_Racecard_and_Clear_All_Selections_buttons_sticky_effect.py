import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1669319_Verify_Build_Your_Own_Racecard_and_Clear_All_Selections_buttons_sticky_effect(Common):
    """
    TR_ID: C1669319
    NAME: Verify 'Build Your Own Racecard' and 'Clear All Selections' buttons sticky effect
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' and 'Clear All Selections' buttons sticky effect.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page___featured_tab(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page -> 'Featured' tab
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'Build Your Own Racecard' section with text block and 'Build a Racecard' button is displayed at the top of the main content area and below the tabs
        """
        pass

    def test_003_click_on_build_a_racecard_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: * 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: * Checkboxes appear before each of 'Event off time' tab only for 'UK&IRE' and
        EXPECTED: 'INTERNATIONAL' section
        EXPECTED: * Checkboxes do NOT appear before 'Event off time' tab with 'Resulted' icon
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons appear below the 'Build Your Own Racecard' section
        """
        pass

    def test_004_verify_clear_all_selections_and_build_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Verify 'Clear All Selections' and 'Build Your Own Racecard' buttons
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons are displayed below 'Build Your Own Racecard' section
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttos are disabled and NOT clickable
        """
        pass

    def test_005_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        EXPECTED: * It remains at the top of the scrolling page
        """
        pass

    def test_006_scroll_the_page_and_reach_virtuals_section(self):
        """
        DESCRIPTION: Scroll the page and reach 'Virtuals' section
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is NOT sticky anymore
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons disappear
        """
        pass

    def test_007_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        EXPECTED: * It remains at the top of the scrolling page
        """
        pass

    def test_008_tick_10_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick 10 checkboxes before 'Event off time' tabs
        EXPECTED: * All unselected checkboxes before 'Event off time' tabs are disabled and NOT clickable
        EXPECTED: * 'You cannot select anymore races for build your racecard' message appears below 'Clear All Selections' and 'Build Your Own Racecard' buttons
        """
        pass

    def test_009_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        EXPECTED: * 'You cannot select anymore races for build your racecard' message is sticky too
        EXPECTED: * Both of them remain at the top of the scrolling page
        """
        pass

    def test_010_scroll_the_page_and_reach_virtuals_section(self):
        """
        DESCRIPTION: Scroll the page and reach 'Virtuals' section
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is NOT sticky anymore
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons disappear
        EXPECTED: * 'You cannot select anymore races for build your racecard' message is NOT sticky too and disappers
        """
        pass

    def test_011_scroll_the_page_up(self):
        """
        DESCRIPTION: Scroll the page up
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        EXPECTED: * 'You cannot select anymore races for build your racecard' message is sticky too
        EXPECTED: * Both of them remain at the top of the scrolling page
        """
        pass
