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
class Test_C62899958_Verify_enabling_disabling_of_Quick_links_Module(Common):
    """
    TR_ID: C62899958
    NAME: Verify enabling/disabling of 'Quick links' Module
    DESCRIPTION: This test case verifies enabling/disabling of "Quick links" Module on Home page/SLP via CMS, If we disable one Quick links next available Quick links should display
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages >Home page > Quick links
    PRECONDITIONS: Configure multiple Quick linkss with different publish dates
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_sports_pages___quick_links_section___open_existing_quick_links(self):
        """
        DESCRIPTION: Go to Sports Pages -> Quick links section -> open existing Quick links
        EXPECTED: Quick links details page is opened
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
        EXPECTED: a)Existing Quick links is active
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_006_load_oxygen_app_and_verify_quick_links_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Quick links displaying
        EXPECTED: Quick links is displayed on Front End
        """
        pass

    def test_007_go_back_to_the_same_quick_links_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Quick links, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Quick links is inactive
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_009_load_oxygen_app_and_verify_quick_links_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Quick links displaying
        EXPECTED: a) Quick links is NOT displayed on Front End
        """
        pass

    def test_010_(self):
        """
        DESCRIPTION: 
        EXPECTED: b) If we have other Quick links with valid date it should display
        """
        pass
