import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2080064_Verify_SAVED_FILTERS_tab_functionality(Common):
    """
    TR_ID: C2080064
    NAME: Verify 'SAVED FILTERS' tab functionality
    DESCRIPTION: 
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Select 'Connect' from header ribbon
    PRECONDITIONS: 3. Select 'Football Bet Filter' item
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
    """
    keep_browser_open = True

    def test_001_load_football_filter_page(self):
        """
        DESCRIPTION: Load Football filter page
        EXPECTED: 
        """
        pass

    def test_002_go_to_saved_filters_tab_and_verify_it_default_view(self):
        """
        DESCRIPTION: Go to 'SAVED FILTERS' tab and verify it default view
        EXPECTED: * Title: SAVED FILTERS
        EXPECTED: * Text: 'Your saved filter are listed below. You can save a maximum of 5 filters.'
        EXPECTED: * 'i' icon
        EXPECTED: * Text: 'Select an option and tap on 'Apply' to reuse your filter.'
        EXPECTED: * Area with filters: 'radio button' 'filter's name'
        EXPECTED: * 'None' filter is created and selected by default
        EXPECTED: * 'Apply' button is active
        """
        pass

    def test_003_verify_i_icon(self):
        """
        DESCRIPTION: Verify 'i' icon
        EXPECTED: * After tapping it additional area with text is expanded
        EXPECTED: * Second tapping collapses this area
        EXPECTED: * Text says:
        EXPECTED: Save filters [bold] is a quick and easy feature that allows you to use the same filters again.
        EXPECTED: Steps to save filters:[bold]
        EXPECTED: 1. Select your options from Your Teams and The Opposition tabs
        EXPECTED: 2. Then tap on 'Save Filters'
        EXPECTED: 3. Give it a Name
        EXPECTED: 4. Then tap on 'Save'
        EXPECTED: You can save maximum of 5 filters. Your saved filters will appear in this section.
        """
        pass

    def test_004_verify_apply_button(self):
        """
        DESCRIPTION: Verify 'Apply' button
        EXPECTED: * 'Apply' button redirects user to 'YOUR TEAMS' tab where nothing is selected
        """
        pass

    def test_005__make_random_selections_for_each_filter_on_both_tabs_tap_save_filter_button(self):
        """
        DESCRIPTION: * Make random selections for each filter on both tabs
        DESCRIPTION: * Tap 'Save filter' button
        EXPECTED: * 'Enter the name in the field below' pop-up appears
        EXPECTED: * Entry field with watermark 'Name' allows to enter up to 25 symbols
        EXPECTED: * 'Cancel' button closes pop-up
        EXPECTED: * 'Save' button saves filter
        """
        pass

    def test_006_save_filter_and_check_it_on_saved_filters_tab(self):
        """
        DESCRIPTION: Save filter and check it on 'SAVED FILTERS' tab
        EXPECTED: * New filter is added at the top of the filters list
        EXPECTED: * New filter is selected
        EXPECTED: * 'Delete' link is located from the right (exception is 'None' filter)
        """
        pass

    def test_007__select_none_tap_apply_button_check_your_teams_the_opposition_tabs(self):
        """
        DESCRIPTION: * Select 'None'
        DESCRIPTION: * Tap 'Apply' button
        DESCRIPTION: * Check 'YOUR TEAMS', 'THE OPPOSITION' tabs
        EXPECTED: * Nothing is selected
        """
        pass

    def test_008__go_to_saved_filters_tab_select_recently_created_filter_tap_apply_button_check_your_teams_the_opposition_tabs(self):
        """
        DESCRIPTION: * Go to 'SAVED FILTERS' tab
        DESCRIPTION: * Select recently created filter
        DESCRIPTION: * Tap 'Apply' button
        DESCRIPTION: * Check 'YOUR TEAMS', 'THE OPPOSITION' tabs
        EXPECTED: * All items are selected respectively to configurations made in step #5
        """
        pass

    def test_009__try_to_create_new_filter_with_existing_filters_name(self):
        """
        DESCRIPTION: * Try to create new filter with existing filter's name
        EXPECTED: * Once user enters occupied filter's name 'Save' button gets disabled
        """
        pass

    def test_010__create_several_new_filters_apply_each_of_them_and_after_each_time_verify_configurations_on_both_tabs(self):
        """
        DESCRIPTION: * Create several new filters
        DESCRIPTION: * Apply each of them and after each time verify configurations (on both tabs)
        EXPECTED: * All selections correspond to selected filter
        EXPECTED: * When 5 filters are created, button Save Filters becomes disabled
        """
        pass

    def test_011__go_to_saved_filters_tab_tap_delete_link_for_any_filter_go_to_other_tab(self):
        """
        DESCRIPTION: * Go to 'SAVED FILTERS' tab
        DESCRIPTION: * Tap 'Delete' link for any filter
        DESCRIPTION: * Go to other tab
        EXPECTED: * Filter disappears from the list
        EXPECTED: * Button Save Filters becomes enabled again
        """
        pass
