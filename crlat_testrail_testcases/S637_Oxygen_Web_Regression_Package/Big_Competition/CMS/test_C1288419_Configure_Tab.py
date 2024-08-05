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
class Test_C1288419_Configure_Tab(Common):
    """
    TR_ID: C1288419
    NAME: Configure Tab
    DESCRIPTION: This test case verifies configuration of Tab within Competition in CMS
    PRECONDITIONS: Have at least one Competition and Tab created in CMS
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

    def test_002_go_to_big_competition_section___choose_competition(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition
        EXPECTED: Competition landing page is opened
        """
        pass

    def test_003_create_a_few_different_enabled_tabs(self):
        """
        DESCRIPTION: Create a few different enabled Tabs
        EXPECTED: Tabs are created
        """
        pass

    def test_004_change_order_of_tabs_by_drag_n_drop(self):
        """
        DESCRIPTION: Change order of Tabs by drag-n-drop
        EXPECTED: Order is changed
        """
        pass

    def test_005_load_oxygen___check_order_of_tabs_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check order of Tabs on FE
        EXPECTED: Order of Tabs on FE corresponds to order configured on step #4
        """
        pass

    def test_006_in_cms_click_on_delete_icon_opposite_to_tab_name_and_confirm_removing_it(self):
        """
        DESCRIPTION: In CMS click on 'delete' icon opposite to Tab name and confirm removing it
        EXPECTED: * 'Remove Completed' success pop-up is displayed
        EXPECTED: * Tab is no more displayed within the list of all Tabs
        """
        pass

    def test_007_load_oxygen___check_tab_existence_on_fe(self):
        """
        DESCRIPTION: Load Oxygen -> check Tab existence on FE
        EXPECTED: Deleted on step #6 Tab is NOT displayed on FE
        """
        pass

    def test_008_in_cms_go_to_tab_details_page_and_change_the_tab_name_field_and_save_changes(self):
        """
        DESCRIPTION: In CMS go to Tab Details page and change the 'Tab Name' field and save changes
        EXPECTED: * Changes are saved
        EXPECTED: * URL is changed automatically and accordingly to 'Tab Name' field
        EXPECTED: * URL starts with '/' symbol (e.g '/featured' )
        EXPECTED: * Space in 'Competition Name' field is substituted by '-' symbol in 'URL' field
        EXPECTED: * URL is updated accordingly on Oxygen page
        """
        pass

    def test_009_make_some_changes_on_tab_details_page_click_on_revert_changes_button_and_click_yes_option_on_revert_changes_pop_up(self):
        """
        DESCRIPTION: Make some changes on Tab Details page, click on 'Revert Changes' button and click 'Yes' option on 'Revert Changes' pop-up
        EXPECTED: * Changes are reverted
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass

    def test_010_make_some_changes_on_tab_details_page_navigate_to_another_page_via_breadcrumbs_and_click_yes_on_leaving_pop_up(self):
        """
        DESCRIPTION: Make some changes on Tab Details page, navigate to another page via breadcrumbs and click 'Yes' on 'Leaving' pop-up
        EXPECTED: * Changes on Tab Details page are NOT saved
        EXPECTED: * User is navigated to corresponding page
        EXPECTED: * 'Save Changes' and 'Revert Changes' buttons are disabled
        """
        pass
