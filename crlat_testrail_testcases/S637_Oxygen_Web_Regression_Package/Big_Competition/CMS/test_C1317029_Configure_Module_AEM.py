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
class Test_C1317029_Configure_Module_AEM(Common):
    """
    TR_ID: C1317029
    NAME: Configure Module AEM
    DESCRIPTION: This test verifies configuration of Module AEM.
    DESCRIPTION: ADD AEM Page Value to test case!!
    PRECONDITIONS: Link for CMS:
    PRECONDITIONS: * https://coral-cms-dev1.symphony-solutions.eu - Phoenix env
    PRECONDITIONS: * https://coral-cms-dev0.symphony-solutions.eu - Develop
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is loaded
        """
        pass

    def test_002_go_to_big_competition_section___choose_competition___choose_tab_that_has_subtabs_option__choose_a_sub_tab(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has SubTabs option > choose a Sub-tab
        EXPECTED: Sub-Tab landing page is opened
        """
        pass

    def test_003_click_create_module_button(self):
        """
        DESCRIPTION: Click 'Create Module' button
        EXPECTED: A popup window is displayed with:
        EXPECTED: * Module Name field, writable
        EXPECTED: * Drop-down box composed by: AEM, Next Events, Promotions, Outright, Specials, Specials Overview, Groups and Groups Overview
        """
        pass

    def test_004_enter_module_name_select_aem_module_type_from_drop_down_click_create_and_then_ok_button(self):
        """
        DESCRIPTION: Enter Module name, select 'AEM' Module type from drop-down click 'Create' and then 'Ok' button
        EXPECTED: New module should be displayed on the all modules list
        """
        pass

    def test_005_click_on_module_name_or_edit_icon_to_view_module_details_page(self):
        """
        DESCRIPTION: Click on Module name or edit icon to view Module details page
        EXPECTED: Next elements should be present on module details page :
        EXPECTED: * Module breadcrumb, composed by: 'Competition' name > 'Tab' name > 'SubTab' name > 'Module' name (only this last is not clickable)
        EXPECTED: * Module Name, with a writable field
        EXPECTED: * 'Module Type' field pre-populated by 'AEM' value and disabled by default
        EXPECTED: * 'Active' checkbox
        EXPECTED: At the bottom there should be present following buttons:
        EXPECTED: * Save Changes
        EXPECTED: * Revert Changes
        EXPECTED: * Remove
        """
        pass

    def test_006_back_to_subtab_level(self):
        """
        DESCRIPTION: Back to 'SubTab' level
        EXPECTED: Sub-tab homepage is loaded
        """
        pass

    def test_007_tap_on_create_module_button(self):
        """
        DESCRIPTION: Tap on 'Create Module' button
        EXPECTED: 'Create a new Module' DLG is displayed
        """
        pass

    def test_008_enter_module_name_select_aem_module_type_from_drop_down_and_click__on_cancel_button(self):
        """
        DESCRIPTION: Enter Module name, select 'AEM' Module type from drop-down and click  on 'Cancel' button
        EXPECTED: Sub-tab homepage is loaded and no changes were saved.
        """
        pass

    def test_009_go_to_big_competition_section___choose_competition___choose_tab_that_has_inactive_subtabs_option(self):
        """
        DESCRIPTION: Go to Big Competition section -> choose Competition -> choose Tab that has inactive SubTabs option
        EXPECTED: Tab landing page is opened
        """
        pass

    def test_010_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps #3-8
        EXPECTED: 
        """
        pass
