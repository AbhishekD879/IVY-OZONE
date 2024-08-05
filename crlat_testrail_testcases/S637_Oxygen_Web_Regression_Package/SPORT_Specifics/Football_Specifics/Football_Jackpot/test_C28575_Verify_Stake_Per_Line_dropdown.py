import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28575_Verify_Stake_Per_Line_dropdown(Common):
    """
    TR_ID: C28575
    NAME: Verify 'Stake Per Line' dropdown
    DESCRIPTION: This test case verifies 'Stake Per Line' dropdown
    DESCRIPTION: AUTOTEST [C9771286]
    PRECONDITIONS: 1) Make sure there is at least one active pool available to be displayed on front-end
    PRECONDITIONS: 2) The user may be logged in or logged out for the functionality to work
    PRECONDITIONS: **Notes:**
    PRECONDITIONS: **Line** - 15 selections, 1 from each event
    PRECONDITIONS: **Stake per line** - how much users wish to bet on each line (on pool for each combination of 15 match results selected)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: Football Jackpot Page is opened
        """
        pass

    def test_004_go_tobet_placement_section(self):
        """
        DESCRIPTION: Go to  Bet Placement section
        EXPECTED: 'Stake Per Line:' label and dropdown are displayed
        """
        pass

    def test_005_verify_default_value_which_is_shown_in_dropdown(self):
        """
        DESCRIPTION: Verify default value which is shown in dropdown
        EXPECTED: Default Value is '£1.00'
        """
        pass

    def test_006_try_to_edit_stake_manually(self):
        """
        DESCRIPTION: Try to edit stake manually
        EXPECTED: It is not possible to enter/edit stake manually
        """
        pass

    def test_007_check_stake_per_line_drop_down_values(self):
        """
        DESCRIPTION: Check 'Stake Per Line' drop-down values
        EXPECTED: *   Available drop-down values are only integers (i.e. multiples of £1.00)
        EXPECTED: *   Drop-down values are amounts from £1.00 to £20.00 in format: **£XX.XX**
        """
        pass

    def test_008_tap_lucky_dip_option_or_manually_add_15_selections_one_selection_per_event_to_form_one_pool_bet_line(self):
        """
        DESCRIPTION: Tap 'Lucky Dip' option or manually add 15 selections (one selection per event) to form one pool bet line
        EXPECTED: *   Corresponding selections are highlighted
        EXPECTED: *   'Total Lines' value is '1'
        """
        pass

    def test_009_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step #7
        EXPECTED: 
        """
        pass

    def test_010_manually_add_one_more_selection_to_form_two_pool_bet_lines(self):
        """
        DESCRIPTION: Manually add one more selection to form two pool bet lines
        EXPECTED: *   Corresponding selections are highlighted
        EXPECTED: *   'Total Lines' value is changed to '2'
        """
        pass

    def test_011_check_stake_per_line_drop_down_values(self):
        """
        DESCRIPTION: Check 'Stake Per Line' drop-down values
        EXPECTED: *   '£0.50' decimal option becomes available for selecting
        EXPECTED: *   Previously available drop-down values are only integers (i.e. multiples of £1.00)
        EXPECTED: *   Drop-down values are £0.50 and amounts from £1.00 to £20.00 in format: **£XX.XX**
        """
        pass

    def test_012_manually_add_one_more_selection_to_form_three_pool_bet_lines(self):
        """
        DESCRIPTION: Manually add one more selection to form three pool bet lines
        EXPECTED: *   Corresponding selections are highlighted
        EXPECTED: *   'Total Lines' value is changed to '3'
        """
        pass

    def test_013_repeat_step_11(self):
        """
        DESCRIPTION: Repeat step #11
        EXPECTED: 
        """
        pass

    def test_014_manually_add_one_more_selection_to_form_four_pool_bet_lines(self):
        """
        DESCRIPTION: Manually add one more selection to form four pool bet lines
        EXPECTED: *   Corresponding selections are highlighted
        EXPECTED: *   'Total Lines' value is changed to '6'
        """
        pass

    def test_015_check_stake_per_line_drop_down_values(self):
        """
        DESCRIPTION: Check 'Stake Per Line' drop-down values
        EXPECTED: *   '£0.25' decimal option becomes available for selecting
        EXPECTED: *   Drop-down values are £0.25, £0.50 and amounts from £1.00 to £20.00 in format: **£XX.XX**
        """
        pass

    def test_016_manually_add_a_few_more_selections_to_form_more_than_four_pool_bet_lines(self):
        """
        DESCRIPTION: Manually add a few more selections to form more than four pool bet lines
        EXPECTED: *   Corresponding selections are highlighted
        EXPECTED: *   'Total Lines' value is changed accordingly
        """
        pass

    def test_017_repeat_step_15(self):
        """
        DESCRIPTION: Repeat step #15
        EXPECTED: 
        """
        pass

    def test_018_choose_025_option_in_stake_per_line_dropdown(self):
        """
        DESCRIPTION: Choose '£0.25' option in 'Stake Per Line' dropdown
        EXPECTED: Selected option is shown in 'Stake Per Line' dropdown field
        """
        pass

    def test_019_manually_remove_highlighted_selections_to_have_just_two_or_three_bet_lines_ie_total_lines_value_is_23(self):
        """
        DESCRIPTION: Manually remove highlighted selections to have just two or three bet lines (i.e. 'Total Lines' value is '2'/'3')
        EXPECTED: *   '£0.25' option in 'Stake Per Line' dropdown field is automatically changed to '£0.50' when two or three bet lines are selected
        EXPECTED: *   Drop-down values are £0.50 and amounts from £1.00 to £20.00
        """
        pass

    def test_020_manually_remove_highlighted_selections_to_have_just_one_bet_line_ie_total_lines_value_is_1(self):
        """
        DESCRIPTION: Manually remove highlighted selections to have just one bet line (i.e. 'Total Lines' value is '1')
        EXPECTED: *   '£0.50' option in 'Stake Per Line' dropdown field is automatically changed to '£1.00' when just one bet line is selected
        EXPECTED: *   Drop-down values are amounts from £1.00 to £20.00
        """
        pass
