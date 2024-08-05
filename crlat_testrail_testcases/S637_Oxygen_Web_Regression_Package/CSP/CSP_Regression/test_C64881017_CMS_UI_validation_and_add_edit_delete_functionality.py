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
class Test_C64881017_CMS_UI_validation_and_add_edit_delete_functionality(Common):
    """
    TR_ID: C64881017
    NAME: CMS UI validation and add/edit/delete functionality
    DESCRIPTION: This test case verifies CMS UI validation
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.( all modules )
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on super button link.
        EXPECTED: User should be able to view existing super buttons
        """
        pass

    def test_004_verify_changes_in_modular_page(self):
        """
        DESCRIPTION: Verify changes in modular page
        EXPECTED: User should able to see new implementations in Modular page
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: 1.Segment dropdown
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2.Segment (s)coloumn
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: 3.Segment(s) Exclusion coloumn
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: 4.Drag and drop functionality
        """
        pass

    def test_009_verify_edit_and__remove_buttons(self):
        """
        DESCRIPTION: Verify Edit and  Remove buttons
        EXPECTED: Edit and remove buttons should be enabled for universal/segmented related records in Universal/segment view
        """
        pass

    def test_010_click_on_title_to_open_in_edit_mode_verify_csp_related_fields(self):
        """
        DESCRIPTION: Click on title to open in edit mode ,Verify CSP related fields
        EXPECTED: CSP related radio buttons are added
        """
        pass

    def test_011_(self):
        """
        DESCRIPTION: 
        EXPECTED: 1.Universal with Exclusion segment text box
        """
        pass

    def test_012_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2.Segment(s) Inclusion with inclusion segment text box
        """
        pass

    def test_013_click_on_create_surfacebets(self):
        """
        DESCRIPTION: Click on create surfacebets
        EXPECTED: User should able to Create surfacebet for Universal /Segements with using newly added Radio buttons
        """
        pass

    def test_014_verify_remove_functionality(self):
        """
        DESCRIPTION: Verify Remove functionality
        EXPECTED: User should able to delete records in specific universal/segment list view and from the details view also by using remove button
        """
        pass

    def test_015_repeat_same_steps_for_all_the_modules(self):
        """
        DESCRIPTION: Repeat same steps for all the modules
        EXPECTED: Create,edit ,remove should be as expected
        """
        pass
