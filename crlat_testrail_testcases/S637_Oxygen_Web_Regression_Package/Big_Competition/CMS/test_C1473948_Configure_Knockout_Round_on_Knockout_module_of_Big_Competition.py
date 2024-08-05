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
class Test_C1473948_Configure_Knockout_Round_on_Knockout_module_of_Big_Competition(Common):
    """
    TR_ID: C1473948
    NAME: Configure 'Knockout Round' on 'Knockout' module of Big Competition
    DESCRIPTION: This test case verifies creating/editing/deleting a Knockout Round for 'Knockouts' module type in CMS
    PRECONDITIONS: 1. User is logged into CMS
    PRECONDITIONS: 2. Big Competition > Competition (e.g. World Cup) > tab (e.g. Knockout) > module (e.g. Knockout) with 'KNOCKOUTS' type are created & opened
    """
    keep_browser_open = True

    def test_001_verify_breadcrumb_on_module_eg_knockouts_page(self):
        """
        DESCRIPTION: Verify breadcrumb on module (e.g. Knockouts) page
        EXPECTED: * Competitions > Competition (World Cup) > Tab (Knockout)> Module (Knockouts) breadcrumb is available on the top of the page
        EXPECTED: * Knockouts module breadcrumb is active and not clickable
        """
        pass

    def test_002_verify_default_controls_on_knockouts_matches_table(self):
        """
        DESCRIPTION: Verify default controls on 'Knockouts matches' table
        EXPECTED: * 'Add Round Name' button
        EXPECTED: * 'Download CSV' button (downloads CSV file)
        EXPECTED: * 'Search For Round Names' field (finds a match of an entered value in the table)
        EXPECTED: * "Round details list is empty" message is displayed in the table
        """
        pass

    def test_003_click_on_add_round_button(self):
        """
        DESCRIPTION: Click on 'Add Round' button
        EXPECTED: * 'Create a new round name' pop up appears with:
        EXPECTED: - 'Name' mandatory field
        EXPECTED: - 'Abbreviation' mandatory field
        EXPECTED: - 'Round Number' mandatory field (accepts only numbers)
        EXPECTED: - 'Current' check box (unchecked by default)
        EXPECTED: - 'Cancel' button (closes the pop up)
        EXPECTED: - 'Create' button (disabled until all mandatory fields are filled out)
        """
        pass

    def test_004_enter_correct_name_abbreviation_round_number_current_click_create(self):
        """
        DESCRIPTION: Enter correct:
        DESCRIPTION: * 'Name'
        DESCRIPTION: * 'Abbreviation'
        DESCRIPTION: * 'Round Number'
        DESCRIPTION: * 'Current'
        DESCRIPTION: > Click 'Create'
        EXPECTED: * Success pop-up is displayed
        EXPECTED: * 'Knockout Rounds' table columns are filled with an added round:
        EXPECTED: - Name link (taken from 'Name' field when adding a round)
        EXPECTED: - 'Abbreviation' (taken from 'Abbreviation' field when adding a round)
        EXPECTED: - Number (taken from 'Round Number' field when adding a round)
        EXPECTED: - Current (depends on 'Current' check box state when adding a round)
        EXPECTED: - Actions ('Remove' icon (removes round from the table) and 'Edit' icon (opens Edit page of a corresponding round))
        EXPECTED: * 'Knockouts Matches' table appears below 'Knockout Rounds' table
        """
        pass

    def test_005__click_on_add_round_button__fill_out_required_fields_see_step_4__check_current_field__click_create_verify_current_state_current_column_of_available_rounds(self):
        """
        DESCRIPTION: * Click on 'Add Round' button > Fill out required fields (see Step 4) > Check 'Current' field > Click 'Create'
        DESCRIPTION: * Verify 'Current' state ('Current' column) of available rounds
        EXPECTED: * Newly added round is set as 'Current'
        EXPECTED: * Previously added round (see Step 4) is no longer 'Current'
        """
        pass

    def test_006_click_on_name_linkedit_icon_of_any_added_round(self):
        """
        DESCRIPTION: Click on 'Name' link/'Edit' icon of any added round
        EXPECTED: * Edit page of a Knockout Round appears
        EXPECTED: * 'Round Name' breadcrumb is active and not clickable
        EXPECTED: * 'Leaving' confirmation appears when clicking on any other than active breadcrumb after any changes are made
        EXPECTED: * 'Name', 'Abbreviation', 'Round Number' fields and 'Current' check box are filled added values (Step 4)
        EXPECTED: * 'Save Changes' button is disabled, until any changes are made
        EXPECTED: * 'Revert Changes' button is disabled, until any changes are made (reverts changes to previous state)
        EXPECTED: * 'Remove' button (enabled)
        """
        pass

    def test_007_make_any_changes_eg_in_nameabbreviation_round_number_fields_current_check_box_click_save_changes(self):
        """
        DESCRIPTION: Make any changes (e.g. in 'Name'/'Abbreviation', 'Round Number' fields 'Current' check box)
        DESCRIPTION: > Click 'Save Changes'
        EXPECTED: * Confirmation pop up appears
        EXPECTED: * Module page is opened
        EXPECTED: * Changes for an edited round are displayed in 'Knockout Rounds' table
        """
        pass

    def test_008_verify_current_state_current_column_of_available_rounds(self):
        """
        DESCRIPTION: Verify 'Current' state ('Current' column) of available rounds
        EXPECTED: * Only last edited round is set as 'Current'
        EXPECTED: * All other rounds are NOT set as 'Current'
        """
        pass

    def test_009_remove_a_round_by_clicking__remove_icon_in_the_knockout_rounds_table__remove_button_on_edit_page_of_a_knockout_round(self):
        """
        DESCRIPTION: Remove a round by clicking:
        DESCRIPTION: - 'Remove' icon in the 'Knockout Rounds' table
        DESCRIPTION: - 'Remove' button on Edit page of a Knockout Round
        EXPECTED: * Confirmation pop up appears
        EXPECTED: * Round is removed from 'Knockout Rounds' table
        """
        pass
