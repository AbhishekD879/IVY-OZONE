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
class Test_C1501418_Configure_Knockout_Matches_on_Knockout_module_of_Big_Competition(Common):
    """
    TR_ID: C1501418
    NAME: Configure 'Knockout Matches' on 'Knockout' module of Big Competition
    DESCRIPTION: This test case verify configuration of 'Knockout Matches' table for Knockout Round of 'Knockout' module
    PRECONDITIONS: Valid event means that it excites in Open Bet TI and dispayed
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: https://coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: * Big Competition > Competition (e.g. World Cup) > tab (e.g. Knockout) > module (e.g. Knockout) with 'KNOCKOUTS' type are created & opened
    PRECONDITIONS: * 'Knockout Round' table is created https://ladbrokescoral.testrail.com/index.php?/cases/view/1473948
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: * CMS is loaded
        EXPECTED: * User is logged in
        """
        pass

    def test_002_go_to_big_competition__competition_eg_world_cup__tab_eg_knockout__module_eg_knockout_with_knockouts_type_are_created__opened(self):
        """
        DESCRIPTION: Go to Big Competition > Competition (e.g. World Cup) > tab (e.g. Knockout) > module (e.g. Knockout) with 'KNOCKOUTS' type are created & opened
        EXPECTED: 'Knockout' page is opened
        """
        pass

    def test_003_go_to_knockouts_module_details_page(self):
        """
        DESCRIPTION: Go to 'Knockouts' module details page
        EXPECTED: * 'Knockouts' module details page is loaded
        EXPECTED: * 'Knockout Round' table is created
        """
        pass

    def test_004_verify_default_controls_on_knockouts_matches_table(self):
        """
        DESCRIPTION: Verify default controls on 'Knockouts matches' table
        EXPECTED: * 'Add Match details' button
        EXPECTED: * 'Download CSV' button (downloads CSV file)
        EXPECTED: * 'Search For Matches' field (finds a match of an entered value in the table)
        EXPECTED: * 'Rounds Details List is Empty' message is shown when the table is empty
        """
        pass

    def test_005_click_on_the_add_match_details_button(self):
        """
        DESCRIPTION: Click on the 'Add Match Details' button
        EXPECTED: Add a New Match Details' pop up is open with following fields:
        EXPECTED: * Event id
        EXPECTED: * Event name
        EXPECTED: * Home Team Name
        EXPECTED: * Away Team Name
        EXPECTED: * Home Team remark
        EXPECTED: * Away Team remark
        EXPECTED: * Venue
        EXPECTED: * Start date and time (date picker), Today, Tomorrow buttons. Today date is auto-populated by default
        EXPECTED: * Selected round (drop down) (mandatory)
        EXPECTED: * Abbreviation round (drop down) become available after specifying 'Selected round' field (mandatory)
        EXPECTED: * 'Upload event' button
        """
        pass

    def test_006_enter_valid_event_id_and_click_on_the_upload_event_button(self):
        """
        DESCRIPTION: Enter valid event id and click on the 'Upload event' button
        EXPECTED: The following fields are populated from Back Office TI:
        EXPECTED: * Event name
        EXPECTED: * Home Team Name
        EXPECTED: * Away Team Name
        EXPECTED: * Start date and time (date picker), Today, Tomorrow buttons. Today is populated by default
        """
        pass

    def test_007_specify_round_and_abbreviation_round_and_click_on_the_add_button(self):
        """
        DESCRIPTION: Specify round and abbreviation round and click on the 'Add' button
        EXPECTED: 'Match record' is saved . 'Match Details' table contains event record with all specified data is created
        """
        pass

    def test_008_specify_round_that_is_already_exist_and_click_on_the_save_changes_button(self):
        """
        DESCRIPTION: Specify round that is already exist and click on the 'Save changes' button
        EXPECTED: 'Match record' is not saved
        """
        pass

    def test_009_repeat_step_4_and_enter_invalid_event_id_and_click_on_the_upload_event_button(self):
        """
        DESCRIPTION: Repeat step 4 and enter invalid event id and click on the 'Upload event' button
        EXPECTED: 'Event is not valid' message is shown under the field
        """
        pass

    def test_010_click_on_the_add_button(self):
        """
        DESCRIPTION: Click on the 'Add' button
        EXPECTED: 'Match record' is saved . 'Match Details' table contains event record with all specified data is created
        """
        pass

    def test_011_click_on_the_edit_icon(self):
        """
        DESCRIPTION: Click on the 'Edit' icon
        EXPECTED: 'Match Details' edit page (Round edit page) is opened with 'Update Event' button
        """
        pass

    def test_012_edit_any_data_and_click_save_changes_button(self):
        """
        DESCRIPTION: Edit any data and click 'Save Changes' button
        EXPECTED: Updated data saved and it is shown into the table
        """
        pass

    def test_013_remove_a_round_by_clicking__remove_icon_in_the_match_details_table__remove_button_on_edit_page_of_a_round(self):
        """
        DESCRIPTION: Remove a round by clicking:
        DESCRIPTION: - 'Remove' icon in the 'Match details' table
        DESCRIPTION: - 'Remove' button on Edit page of a Round
        EXPECTED: Event event record is removed from 'Match Details' table. Corresponding round is removed from 'Round' table after deleting the last related event
        """
        pass
