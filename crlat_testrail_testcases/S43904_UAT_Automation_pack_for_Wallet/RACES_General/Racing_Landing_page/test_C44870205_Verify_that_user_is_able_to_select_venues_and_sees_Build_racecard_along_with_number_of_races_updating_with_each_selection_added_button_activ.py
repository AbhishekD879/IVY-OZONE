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
class Test_C44870205_Verify_that_user_is_able_to_select_venues_and_sees_Build_racecard_along_with_number_of_races_updating_with_each_selection_added_button_active_green_on_the_bottom_Verify_that_on_tap_user_is_navigated_to_Racecard_page_where_all_selected_races_a(Common):
    """
    TR_ID: C44870205
    NAME: "Verify that user is able to select venues and sees Build racecard (along with number of races updating with each selection added) button active (green) on the bottom  Verify that on tap, user is navigated to Racecard page, where all selected races a
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' functionality for 'Horse Racing'.
    PRECONDITIONS: User is in Horse Racing/Greyhounds Landing page
    """
    keep_browser_open = True

    def test_001_click_on_build_a_racecard_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: Build a Racecard' button is clickable
        EXPECTED: 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: 'Clear All Selections' and 'Build Your Own Racecard' buttons appear below the 'Build Your Own Racecard' section and it's disabled and NOT clickable
        EXPECTED: Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        EXPECTED: Checkboxes appear before each of 'Event off time' tab only for 'UK&IRE' and 'INTERNATIONAL' sections
        """
        pass

    def test_002_tick_at_least_one_checkbox_before_event_off_time_tab_and_verify_clear_all_selectionsbuild_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Tick at least one checkbox before 'Event off time' tab and verify 'Clear All Selections'/'Build Your Own Racecard' buttons
        EXPECTED: Checkbox before 'Event off time' tabs is ticked
        EXPECTED: 'Clear All Selections' and 'Build Your Own Racecard' buttons became active and clickable
        """
        pass

    def test_003_click_at_clear_all_selections_button(self):
        """
        DESCRIPTION: Click at 'Clear All Selections' button
        EXPECTED: All ticked checkboxes before each 'Event off time' tab become unchecked
        EXPECTED: 'Clear All Selections' and 'Build Your Own Racecard' buttons became disabled and NOT clickable
        """
        pass

    def test_004_tick_10_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick 10 checkboxes before 'Event off time' tabs
        EXPECTED: All unselected checkboxes before 'Event off time' tabs are disabled and NOT clickable
        EXPECTED: 'You cannot select anymore races for build your racecard' message appears below 'Clear All Selections' and 'Build Your Own Racecard' buttons
        """
        pass

    def test_005_untick_one_of_the_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Untick one of the checkboxes before 'Event off time' tabs
        EXPECTED: Checkbox before 'Event off time' tab is unticked
        EXPECTED: 'You cannot select anymore races for build your racecard' message disappears
        """
        pass

    def test_006_click_at_build_your_own_racecard_button(self):
        """
        DESCRIPTION: Click at 'Build Your Own Racecard' button
        EXPECTED: User is navigated to 'Build Your Own Racecard' page
        EXPECTED: Selected multiple race cards are displayed one after another, separated by 'Event details' sections
        EXPECTED: Selected multiple race cards are ordered by start date and time in ascending i.e. starting from earliest one
        EXPECTED: In case start time is identical, alphabetically
        """
        pass

    def test_007_verify_event_details_section(self):
        """
        DESCRIPTION: Verify 'Event details' section
        EXPECTED: Event details section contains:
        EXPECTED: Event name (corresponds to attribute 'name' in SS response)
        EXPECTED: Event off time (taken from attribute 'name' and corresponds to the race local time)
        EXPECTED: Date (for tomorrow and future events only) in the format: 'Tuesday 22nd May' (attribute 'startTime')
        EXPECTED: Race Event Status e.g. 'Going GOOD' (attribute 'going' within 'racingFormEvent' section)
        EXPECTED: Distance in the format: 'Distance: Xm Yf Zy' (attribute 'distance')
        EXPECTED: Countdown timer (shown only for events with Race start time less then or equal to 45 minutes)
        """
        pass

    def test_008_verify_displaying_of_markets_tabs(self):
        """
        DESCRIPTION: Verify displaying of Markets tabs
        EXPECTED: Market tabs are displayed below 'Event details' section
        EXPECTED: The next tabs are displayed in the following order:
        EXPECTED: 'Win Or E/W' tab
        EXPECTED: 'Win Only' tab
        EXPECTED: 'Betting WO' tab
        EXPECTED: 'To Finish' tab
        EXPECTED: 'Top Finish' tab
        EXPECTED: 'Place Insurance' tab
        EXPECTED: 'More Markets' tab
        EXPECTED: 'Win or E/W' market is selected by default
        """
        pass

    def test_009_verify_event_cards(self):
        """
        DESCRIPTION: Verify Event cards
        EXPECTED: Event cards consist of the next items:
        EXPECTED: 'Each way' terms are displayed above the list of selection
        EXPECTED: 'Class' of Race parameter is displayed next to 'Each way' terms/places
        EXPECTED: BPG icon is displayed in the same line as the Each-way terms (but on the right-hand side)
        EXPECTED: 'CASH OUT' icon is displayed in the same line as 'Each way' terms from the right side (next to BPG icon if available)
        EXPECTED: Promotion icon is shown on the same line as 'Each way' terms, on the right side, next to BPG/CashOut icons
        EXPECTED: List of selections/outcomes are displayed for every Event card
        """
        pass
