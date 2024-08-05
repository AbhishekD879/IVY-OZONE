import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1669318_Verify_Build_Your_Own_Racecard_functionality_on_Horse_Racing_Landing_page(Common):
    """
    TR_ID: C1669318
    NAME: Verify 'Build Your Own Racecard' functionality on 'Horse Racing' Landing page
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' functionality on 'Horse Racing' Landing page.
    PRECONDITIONS: There are HR events in 'UK&IRE', 'INTERNATIONAL', 'VIRTUALS' groups
    PRECONDITIONS: There is at least one resulted event
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page___featured_tab(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page -> 'Featured' tab
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab (Coral) 'Meetings' tab (Ladbrokes) is selected by default
        EXPECTED: * 'Build Your Own Racecard' section with text block and 'Build a Racecard' button is displayed at the top of the main content area and below the tabs
        """
        pass

    def test_002_click_on_build_a_racecard_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: * 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: * Checkboxes appear before 'Event off time' tabs
        EXPECTED: * 'Clear All Selections' and 'Build Your Racecard' buttons appear below the 'Build Your Own Racecard' section
        """
        pass

    def test_003_verify_checkboxes_displaying_before_event_off_timetime_for_each_event_tabs(self):
        """
        DESCRIPTION: Verify checkboxes displaying before 'Event off time'(time for each event) tabs
        EXPECTED: * Checkboxes appear before each of 'Event off time' tab only for 'UK&IRE' and 'INTERNATIONAL' sections
        EXPECTED: * Checkboxes are NOT displayed before 'Event off time' tabs for 'VIRTUALS' section
        EXPECTED: * Checkboxes are NOT displayed before 'Event off time' tabs with 'Resulted' icon
        """
        pass

    def test_004_verify_clear_all_selections_and_build_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Verify 'Clear All Selections' and 'Build Your Own Racecard' buttons
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons are disabled and NOT clickable
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Racecard' buttons is sticky
        """
        pass

    def test_005_tick_at_least_one_checkbox_before_event_off_time_tab_and_verify_clear_all_selectionsbuild_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Tick at least one checkbox before 'Event off time' tab and verify 'Clear All Selections'/'Build Your Own Racecard' buttons
        EXPECTED: * Checkbox before 'Event off time' tab is ticked
        EXPECTED: * 'Clear All Selections' and 'Build Your Racecard' buttons become active and clickable
        """
        pass

    def test_006_click_at_clear_all_selections_button(self):
        """
        DESCRIPTION: Click at 'Clear All Selections' button
        EXPECTED: * All ticked checkboxes before each 'Event off time' tab become unchecked
        EXPECTED: * 'Clear All Selections' and 'Build Your Racecard' buttons became disabled and NOT clickable
        """
        pass

    def test_007_tick_several_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick several checkboxes before 'Event off time' tabs
        EXPECTED: * Checkboxes before 'Event off time' tabs are ticked
        EXPECTED: * 'Clear All Selections' and 'Build Your Racecard' buttons became active and clickable
        """
        pass

    def test_008_tick_10_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick 10 checkboxes before 'Event off time' tabs
        EXPECTED: * All unselected checkboxes before 'Event off time' tabs are disabled and NOT clickable
        EXPECTED: * 'You cannot select anymore races for build your racecard' message appears below 'Clear All Selections' and 'Build Your Racecard' buttons
        """
        pass

    def test_009_untick_one_of_the_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Untick one of the checkboxes before 'Event off time' tabs
        EXPECTED: * Checkbox before 'Event off time' tab is unticked
        EXPECTED: * 'You cannot select anymore races for build your racecard' message disappears
        """
        pass

    def test_010_click_at_build_your_own_racecard_button(self):
        """
        DESCRIPTION: Click at 'Build Your Own Racecard' button
        EXPECTED: * User is navigated to 'Build Your Own Racecard' page
        EXPECTED: * All selected racecards are displayed in the list
        """
        pass
