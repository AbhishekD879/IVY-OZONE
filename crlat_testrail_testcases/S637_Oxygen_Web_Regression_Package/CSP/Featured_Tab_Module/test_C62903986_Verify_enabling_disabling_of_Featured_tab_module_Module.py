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
class Test_C62903986_Verify_enabling_disabling_of_Featured_tab_module_Module(Common):
    """
    TR_ID: C62903986
    NAME: Verify enabling/disabling of 'Featured tab module' Module
    DESCRIPTION: This test case verifies enabling/disabling of "Featured tab module" Module on Home page/SLP via CMS, If we disable one Featured tab module next available Featured tab module should display
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Featured tab module
    PRECONDITIONS: Configure multiple Featured tab modules with different publish dates
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___featured_tab_module_section___open_existing_featured_tab_module(self):
        """
        DESCRIPTION: Go to Sports Pages -> Featured tab module section -> open existing Featured tab module
        EXPECTED: Featured tab module details page is opened
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
        EXPECTED: a)Existing Featured tab module is active
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_006_load_oxygen_app_and_verify_featured_tab_module_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Featured tab module displaying
        EXPECTED: Featured tab module is displayed on Front End
        """
        pass

    def test_007_go_back_to_the_same_featured_tab_module_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Featured tab module, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Featured tab module is inactive
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_009_load_oxygen_app_and_verify_featured_tab_module_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Featured tab module displaying
        EXPECTED: a) Featured tab module is NOT displayed on Front End
        """
        pass

    def test_010_(self):
        """
        DESCRIPTION: 
        EXPECTED: b) If we have other Featured tab module with valid date it should display
        """
        pass
