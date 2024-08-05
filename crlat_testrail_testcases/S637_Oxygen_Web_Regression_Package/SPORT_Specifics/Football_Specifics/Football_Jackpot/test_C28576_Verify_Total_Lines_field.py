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
class Test_C28576_Verify_Total_Lines_field(Common):
    """
    TR_ID: C28576
    NAME: Verify 'Total Lines' field
    DESCRIPTION: This test case verifies 'Total Lines:' label and field
    PRECONDITIONS: 1) Make sure there is at least one active pool available to be displayed on front-end
    PRECONDITIONS: 2) The user may be logged in or logged out for the functionality to work
    PRECONDITIONS: **Notes:**
    PRECONDITIONS: **Line** - 15 selections, 1 from each event
    PRECONDITIONS: **Total Lines - **number of selected combinations of 15 match results
    """
    keep_browser_open = True

    def test_001_open_jackpot_page(self):
        """
        DESCRIPTION: Open 'Jackpot' page
        EXPECTED: Football Jackpot Page is opened
        """
        pass

    def test_002_go_tobet_placement_section(self):
        """
        DESCRIPTION: Go to  Bet Placement section
        EXPECTED: 'Total Lines:' label and field are displayed
        """
        pass

    def test_003_verify_default_value_which_is_shown_in_the_total_lines_field(self):
        """
        DESCRIPTION: Verify default value which is shown in the 'Total Lines' field
        EXPECTED: Default value '0' is shown in the 'Total Lines' field (while no lines are chosen)
        """
        pass

    def test_004_make_1_selection_from_each_of_15_availableevents(self):
        """
        DESCRIPTION: Make 1 selection from **each of 15 available **events
        EXPECTED: *   Selections that were made are highlighted
        EXPECTED: *   One line is formed
        EXPECTED: *   '1' is shown in the 'Total Lines' field
        """
        pass

    def test_005_make_more_than_15_selections_at_least_1_from_each_event(self):
        """
        DESCRIPTION: Make **more** than 15 selections (at least 1 from each event)
        EXPECTED: *   The number of permed (permutations) lines is determined as follows:
        EXPECTED: (No. of selections for Match 1) *** **(No. of selections for Match 2) ***** (No. of selections for Match 3) *****…etc…*** **(No. of selections for Match <number of **active **events>)
        EXPECTED: *   Received number of lines is shown in the 'Total Lines' field
        EXPECTED: *   There is no restriction on the number of lines that can be selected
        """
        pass

    def test_006_verify_total_lines_field_view(self):
        """
        DESCRIPTION: Verify 'Total Lines' field view
        EXPECTED: 'Total Lines' field is able to handle at least 4 digits as standard – for more than 4 digits number can overflow field boundary on screen but must not truncate
        """
        pass

    def test_007_verify_total_lines_value_updating(self):
        """
        DESCRIPTION: Verify 'Total Lines' value updating
        EXPECTED: Shown value is automatically updated as the user updates the number of selections
        """
        pass
