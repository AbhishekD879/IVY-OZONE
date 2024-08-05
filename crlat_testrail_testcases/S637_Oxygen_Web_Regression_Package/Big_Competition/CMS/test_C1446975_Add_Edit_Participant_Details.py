import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1446975_Add_Edit_Participant_Details(Common):
    """
    TR_ID: C1446975
    NAME: Add/Edit Participant Details
    DESCRIPTION: This test case verifies adding new Participant in CMS
    PRECONDITIONS: Link to CMS:
    PRECONDITIONS: https://coral-cms-dev0.symphony-solutions.eu
    PRECONDITIONS: Big Competition should be created
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_navigate_to_big_competition_in_the_left_pane(self):
        """
        DESCRIPTION: Navigate to Big Competition in the left pane
        EXPECTED: Big Competition section is opened
        """
        pass

    def test_003_scroll_down_to_add_participant_area_and_click_add_participant_details_button(self):
        """
        DESCRIPTION: Scroll down to 'Add Participant' area and click 'Add Participant Details' button
        EXPECTED: 'Add Participant Details' button is present
        EXPECTED: 'Participants Details List is Empty' text is present below the button
        EXPECTED: 'Add a New Participant Details' pop-up is displayed
        """
        pass

    def test_004_verify_add_a_new_participant_details_pop_up_details(self):
        """
        DESCRIPTION: Verify 'Add a New Participant Details' pop-up details
        EXPECTED: Next items are present:
        EXPECTED: 'Add a New Participant Details' title
        EXPECTED: 'OB Name' (mandatory) text field
        EXPECTED: 'Front End Full Name' text field
        EXPECTED: 'Name Abbreviation' text field
        EXPECTED: 'Cancel' (active) button
        EXPECTED: 'Add' (inactive by default) button
        """
        pass

    def test_005_enter_front_end_full_name_name_abbreviation_and_leave_ob_name_empty(self):
        """
        DESCRIPTION: Enter Front End Full Name, Name Abbreviation and leave OB Name empty
        EXPECTED: 'Add' button should be inactive as OB name is a mandatory field
        """
        pass

    def test_006_enter_ob_name_front_end_full_name_name_abbreviation_and_click_add_button(self):
        """
        DESCRIPTION: Enter OB Name, Front End Full Name, Name Abbreviation and click 'Add' button
        EXPECTED: 'Add' button is active
        EXPECTED: New Participant is added
        EXPECTED: User is navigated to Big Competition Details section
        EXPECTED: Grid table with next columns is displayed :
        EXPECTED: - Ob Name
        EXPECTED: - Front End Full Name
        EXPECTED: - Name Abbreviation
        EXPECTED: - Flag/Logo
        EXPECTED: - Actions
        EXPECTED: New Participant is displayed within the list of all existing Participants
        """
        pass

    def test_007_click_add_participant_details_button_fill_all_fields_and_click_cancel_button(self):
        """
        DESCRIPTION: Click 'Add Participant Details' button, fill all fields and click 'Cancel' button
        EXPECTED: New Participant isn't added
        EXPECTED: User is navigated to Big Competition Details section
        """
        pass

    def test_008_click_on_participant_ob_name_on_the_list(self):
        """
        DESCRIPTION: Click on Participant OB name on the list
        EXPECTED: Participant details (edit) page is displayed
        """
        pass

    def test_009_verify_participant_details_edit_page(self):
        """
        DESCRIPTION: Verify Participant details (edit) page
        EXPECTED: Next items are present:
        EXPECTED: On the top of the page breadcrumbs (navigation) area 'Big competition name' > 'Participant name'
        EXPECTED: Participant header with created at/by and updated at/by information
        EXPECTED: Participant details:
        EXPECTED: - OB name
        EXPECTED: - Front End Full Name
        EXPECTED: - Name Abbreviation
        EXPECTED: - SVG Flag/Logo
        EXPECTED: - 'Upload File' active button
        EXPECTED: Inactive 'Save Changes', 'Revert Changes' buttons
        EXPECTED: Active 'Remove' button
        """
        pass

    def test_010_change_ob_name_front_end_full_name_name_abbreviation(self):
        """
        DESCRIPTION: Change OB Name, Front End Full Name, Name Abbreviation
        EXPECTED: 'Save Changes' button became active
        """
        pass

    def test_011_scroll_down_to_svg_flaglogo_area_and_press_upload_file_button(self):
        """
        DESCRIPTION: Scroll down to 'SVG Flag/Logo' area and press 'Upload File' button
        EXPECTED: 'File upload window' is displayed
        """
        pass

    def test_012_select_any_file_type_except_svg_eg_png_jpg_etc(self):
        """
        DESCRIPTION: Select any file type, except svg (e.g. png, jpg, etc.)
        EXPECTED: 'Error: png file type not supported, supported types are [svg]' error message is  displayed
        """
        pass

    def test_013_press_upload_file_button_and_select_svg_file_format(self):
        """
        DESCRIPTION: Press 'Upload File' button and select svg file format
        EXPECTED: Svg file is uploaded successfully
        EXPECTED: 'Svg uploaded' notification is displayed
        EXPECTED: Filename is shown in 'File name' field
        EXPECTED: 'Remove File' button became active
        """
        pass

    def test_014_press_save_changes_button(self):
        """
        DESCRIPTION: Press 'Save Changes' button
        EXPECTED: 'Save of: (New participant name)' pop-up with 'Are You Sure You Want to Save This: (New participant name)' is displayed
        """
        pass

    def test_015_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: 'Participant Details Saving' pop-up with 'Participant Details are Successfully Saved' message is displayed
        """
        pass

    def test_016_press_ok_button(self):
        """
        DESCRIPTION: Press 'Ok' button
        EXPECTED: All changes should be saved successfully
        EXPECTED: User stays in Participant details page
        """
        pass

    def test_017_navigate_to_the_list_of_all_existing_participants(self):
        """
        DESCRIPTION: Navigate to the list of all existing Participants
        EXPECTED: All changes should be displayed successfully on the list
        """
        pass

    def test_018_click_on_edit_icon_near_the_participant_name(self):
        """
        DESCRIPTION: Click on edit icon near the Participant name
        EXPECTED: Participant details (edit) page is displayed
        """
        pass

    def test_019_press_remove_file_button_from_svg_flaglogo_area(self):
        """
        DESCRIPTION: Press 'Remove File' button from 'SVG Flag/Logo' area
        EXPECTED: 'Remove File' pop-up with 'Are You Sure You Want to Remove file?' message is displayed
        """
        pass

    def test_020_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: 'Svg Deleted' notification is displayed
        EXPECTED: File is removed successfully
        """
        pass

    def test_021_press_remove_button_on_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Press 'Remove' button on the bottom of the page
        EXPECTED: 'Remove (participant name)' pop-up with 'Are You Sure You Want to Remove : (Participant name)?' message is displayed
        """
        pass

    def test_022_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: Participant is removed successfully
        EXPECTED: User should be redirected to the list of all existing Participants
        EXPECTED: Participant is not displayed on the list
        """
        pass

    def test_023_add_new_participant(self):
        """
        DESCRIPTION: Add new Participant
        EXPECTED: New Participant is added
        """
        pass

    def test_024_press_remove_icon_next_to_the_participant_name(self):
        """
        DESCRIPTION: Press 'Remove' icon next to the Participant name
        EXPECTED: 'Remove Participant Details' pop-up with 'Are You Sure You Want to Remove Participant Details : (Participant name)?' message is displayed
        """
        pass

    def test_025_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: 'Remove Completed' pop-up with 'Participant Details were Removed' message is displayed
        """
        pass

    def test_026_press_ok_button(self):
        """
        DESCRIPTION: Press 'Ok' button
        EXPECTED: Participant is removed successfully
        EXPECTED: Participant is not displayed on the list
        """
        pass
