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
class Test_C1232383_Configure_Competition(Common):
    """
    TR_ID: C1232383
    NAME: Configure Competition
    DESCRIPTION: This case verifies configure a Big Competition
    PRECONDITIONS: Have at least one big competition with at least two main tabs already created.
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_big_competition_section(self):
        """
        DESCRIPTION: Go to Big Competition section
        EXPECTED: Big Competition section is opened
        """
        pass

    def test_003_tap_on_a_competition_previously_created(self):
        """
        DESCRIPTION: Tap on a Competition previously created
        EXPECTED: A new window is displayed with following elements at the top:
        EXPECTED: * 'Navigation tree', composed by 'COMPETITIONS' > 'Big competition' name
        EXPECTED: * 'Message': Created at YYYY-MM-DD HH:MM:SS AM/PM by test.admin@coral.co.uk, Updated at YYYY-MM-DD HH:MM:SS AM/PM by test.admin@coral.co.uk
        EXPECTED: Below a box with following elements:
        EXPECTED: * Untick Active/Disabled 'Checkbox'
        EXPECTED: * Competition Name, with respective name field below
        EXPECTED: * URL, with respective URL field below
        EXPECTED: * OB Type ID, with the corresponding Type Id of Big Competition
        EXPECTED: Below another box with:
        EXPECTED: * '+ Create Tab' button
        EXPECTED: * 'Download CVS' button
        EXPECTED: * A row composed by 4 fields: 'Name', 'Enabled', 'Tab has sub-tabs' and 'Actions'
        EXPECTED: Below tab following elements are present (from preconditions created tab):
        EXPECTED: * 'Up/down arrow' sign, which through 'Drag'-n-'Drop' has the ability to change order of tab
        EXPECTED: * Respective 'Tab Name'
        EXPECTED: * 'Checkbox', respective to visibility status of each tab
        EXPECTED: * 'Checkbox', respective to info if 'Tab has sub-tabs'
        EXPECTED: * 'Prohibited sign' button, which allows to delete tab
        EXPECTED: * 'Pen' button, which allows to edit tab (redirecting to edit tab page)
        EXPECTED: At the bottom of page the following buttons are present:
        EXPECTED: * 'Save Changes'
        EXPECTED: * 'Revert Changes'
        EXPECTED: * 'Remove'
        """
        pass

    def test_004_untick_active_checkbox_and_tap_on__save_changes_cta(self):
        """
        DESCRIPTION: Untick Active 'Checkbox' and tap on * 'Save Changes' CTA
        EXPECTED: Disabled tab is not displayed on FE
        """
        pass

    def test_005_tick_active_checkbox_and_tap_on__save_changes_cta(self):
        """
        DESCRIPTION: Tick Active 'Checkbox' and tap on * 'Save Changes' CTA
        EXPECTED: Active tab is displayed on FE
        """
        pass

    def test_006_tap_on_the_competitions_link_from_the_top_breadcrumbs(self):
        """
        DESCRIPTION: Tap on the 'COMPETITIONS' link from the top breadcrumbs
        EXPECTED: Return back to 'Big Competitions' homepage
        """
        pass

    def test_007_tap_on_prohibited_sign_button_which_allows_to_delete_competition(self):
        """
        DESCRIPTION: Tap on 'Prohibited sign' button, which allows to delete competition
        EXPECTED: A popup window appears with:
        EXPECTED: * Message: 'Are You Sure You Want to Remove Competition 'Competition Name'?'
        EXPECTED: * CTA buttons: 'Yes' and 'No'
        """
        pass

    def test_008_tap_no_cta_button(self):
        """
        DESCRIPTION: Tap 'No' CTA button
        EXPECTED: No changes are saved
        """
        pass

    def test_009_repeat_step_7tap_yes_cta_button(self):
        """
        DESCRIPTION: Repeat step #7
        DESCRIPTION: Tap 'Yes' CTA button
        EXPECTED: 'Remove Completed' pop-up with 'Big Competition is Removed' message is displayed
        """
        pass

    def test_010_tap_ok_button(self):
        """
        DESCRIPTION: Tap 'Ok' button
        EXPECTED: Competition is removed from the list
        """
        pass

    def test_011_navigate_to_another_competition_from_the_list_and_tap_on__pen_button_which_allows_to_edit_tab(self):
        """
        DESCRIPTION: Navigate to another competition from the list and tap on  'Pen' button, which allows to edit tab
        EXPECTED: Edit 'Big Competition' page is loaded
        """
        pass

    def test_012_on_the_competition_name_filed_change_the_name_of_competitiontap_revert_changes(self):
        """
        DESCRIPTION: On the 'Competition Name' filed change the name of competition
        DESCRIPTION: Tap 'Revert Changes'
        EXPECTED: 'Competition Name' is not changed
        """
        pass

    def test_013_on_the_competition_name_filed_change_the_name_of_competitiontap_save_changes(self):
        """
        DESCRIPTION: On the 'Competition Name' filed change the name of competition
        DESCRIPTION: Tap 'Save changes'
        EXPECTED: 'Competition Name' is changed accordingly
        """
        pass

    def test_014_drag_one_tab_previously_created_below_another_tab(self):
        """
        DESCRIPTION: Drag one 'Tab' previously created below another tab
        EXPECTED: Order of tabs should be changed accordingly
        """
        pass

    def test_015_go_to_competition_details_page_change_the_competition_name_field_and_save_changes(self):
        """
        DESCRIPTION: Go to Competition Details Page, change the 'Competition Name' field and save changes
        EXPECTED: * Changes are saved
        EXPECTED: * URL is changed automatically and accordingly to 'Competition Name' field
        EXPECTED: * URL starts with '/' symbol (e.g '/worldcup')
        EXPECTED: * Space in 'Competition Name' field is substituted by '-' symbol in 'URL' field
        EXPECTED: * URL is updated accordingly on Oxygen page
        """
        pass

    def test_016_make_some_changes_on_competition_details_page_click_on_revert_changes_button_and_click_yes_option_on_revert_changes_pop_up(self):
        """
        DESCRIPTION: Make some changes on Competition Details page, click on 'Revert Changes' button and click 'Yes' option on 'Revert Changes' pop-up
        EXPECTED: * Changes are reverted
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass

    def test_017_make_some_changes_on_competition_details_page_navigate_to_another_page_via_breadcrumbs_and_click_yes_on_leaving_pop_up(self):
        """
        DESCRIPTION: Make some changes on Competition Details page, navigate to another page via breadcrumbs and click 'Yes' on 'Leaving' pop-up
        EXPECTED: * Changes on Competition Details page are NOT saved
        EXPECTED: * User is navigated to the corresponding page
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass
