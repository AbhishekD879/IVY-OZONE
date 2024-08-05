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
class Test_C1217998_Add_new_Competition(Common):
    """
    TR_ID: C1217998
    NAME: Add new Competition
    DESCRIPTION: This test case verifies adding new Competition in CMS
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_big_competition_section_in_cms(self):
        """
        DESCRIPTION: Go to Big Competition section in CMS
        EXPECTED: Big Competition section is opened
        """
        pass

    def test_003_click_create_competition_button(self):
        """
        DESCRIPTION: Click 'Create Competition' button
        EXPECTED: 'Create a new Competition' pop-up is displayed
        """
        pass

    def test_004_enter_competition_name__url_appears_automatically_but_invalid_ob_type_id_and_click_create_competition_button(self):
        """
        DESCRIPTION: Enter Competition Name  (URL appears automatically), but invalid OB type ID and click 'Create Competition' button
        EXPECTED: Error message is displayed - "Error: Request processing failed; nested exception is java.lang.IllegalArgumentException: Can't find competition at SS by typeId"
        """
        pass

    def test_005_enter_competition_name_url_appears_automatically_valid_ob_type_id_you_can_get_it_from_open_bet_ti_and_click_create_competition_button(self):
        """
        DESCRIPTION: Enter Competition Name (URL appears automatically), valid OB type ID (you can get it from Open Bet TI) and click 'Create Competition' button
        EXPECTED: * New Competition is created
        EXPECTED: * User is navigated to Big Competition section
        EXPECTED: * New Competition is displayed within list of all existing Competitions on Big Competition section
        """
        pass

    def test_006_repeat_steps_3_4_but_on_step_4_click_cancel_button(self):
        """
        DESCRIPTION: Repeat steps #3-4, but on step #4 click 'Cancel' button
        EXPECTED: * New Competition is NOT created
        EXPECTED: * User is navigated to Big Competition section
        """
        pass

    def test_007_click_on_competition_name_on_the_list_of_all_existing_competitions(self):
        """
        DESCRIPTION: Click on Competition name on the list of all existing Competitions
        EXPECTED: Edit Big Competition page is displayed
        """
        pass

    def test_008_check_active_checkbox_edit_competition_name_and_url_and_press_save_change_button(self):
        """
        DESCRIPTION: Check 'Active' checkbox, edit Competition Name and URL and press Save change button
        EXPECTED: 'Save of: (Competition name)' pop-up with 'Are You Sure You Want to Save This: (Competition name)' is displayed
        """
        pass

    def test_009_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: 'Competition' pop-up with 'Competition was successfully saved' message is displayed
        """
        pass

    def test_010_press_ok_button(self):
        """
        DESCRIPTION: Press 'Ok' button
        EXPECTED: All changes should be saved successfully
        """
        pass

    def test_011_navigate_to_the_list_of_all_existing_competitions(self):
        """
        DESCRIPTION: Navigate to the list of all existing Competitions
        EXPECTED: All changes should be displayed successfully on the list
        """
        pass

    def test_012_click_on_edit_icon_next_to_the_competition_name(self):
        """
        DESCRIPTION: Click on edit icon next to the Competition name
        EXPECTED: Edit Big Competition page is displayed
        """
        pass

    def test_013_press_remove_button(self):
        """
        DESCRIPTION: Press 'Remove' button
        EXPECTED: 'Remove (Competition name)' pop-up with 'Are You Sure You Want to Remove : (Competition name)?' message is displayed
        """
        pass

    def test_014_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: * Competition is removed successfully
        EXPECTED: * User should be redirected to the list of all existing Competitions
        EXPECTED: * Competition is not displayed on the list
        """
        pass

    def test_015_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: New Competition is created
        """
        pass

    def test_016_press_remove_icon_next_to_the_competition_name(self):
        """
        DESCRIPTION: Press 'Remove' icon next to the Competition name
        EXPECTED: 'Remove Big Competition' pop-up with 'Are You Sure You Want to Delete Competition (Competition name)?' message is displayed
        """
        pass

    def test_017_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: 'Delete Completed' pop-up with 'Big Competition Removed' message is displayed
        """
        pass

    def test_018_press_ok_button(self):
        """
        DESCRIPTION: Press 'Ok' button
        EXPECTED: * Competition is removed successfully
        EXPECTED: * Competition is not displayed on the list
        """
        pass
