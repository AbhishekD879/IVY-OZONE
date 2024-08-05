import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C63761086_Verify_enabling_disabling_of_Module_ribbon_tab_Module(Common):
    """
    TR_ID: C63761086
    NAME: Verify enabling/disabling of 'Module ribbon tab' Module
    DESCRIPTION: This test case verifies enabling/disabling of "Module ribbon tab" Module on Home page/SLP via CMS, If we disable one Module ribbon tab next available Module ribbon tab should display
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Module ribbon tab
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___module_ribbon_tab_section___open_existing_module_ribbon_tab(self):
        """
        DESCRIPTION: Go to Sports Pages -> Module ribbon tab section -> open existing Module ribbon tab
        EXPECTED: Module ribbon tab details page is opened
        """
        pass

    def test_003_validate_the_user_is_able_to_enabledisable_and_save_the_changes_successfully(self):
        """
        DESCRIPTION: Validate the User is able to enable/disable and save the changes successfully.
        EXPECTED: User should be able to enable/ disable the check box.
        """
        pass

    def test_004_set_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Set 'Active' checkbox and save changes
        EXPECTED: a)Existing Module ribbon tab is active
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_005_load_oxygen_app_and_verify_module_ribbon_tab_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Module ribbon tab displaying
        EXPECTED: Module ribbon tab is displayed on Front End
        """
        pass

    def test_006_go_back_to_the_same_module_ribbon_tab_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Module ribbon tab, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Module ribbon tab is inactive
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_module_ribbon_tab_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Module ribbon tab displaying
        EXPECTED: a) Module ribbon tab is NOT displayed on Front End
        EXPECTED: b) If we have other Module ribbon tab with valid date it should display
        """
        pass
