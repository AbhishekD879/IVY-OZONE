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
class Test_C62701191_Verify_enabling_disabling_of_Footer_menu_Module(Common):
    """
    TR_ID: C62701191
    NAME: Verify enabling/disabling of 'Footer menu' Module
    DESCRIPTION: This test case verifies enabling/disabling of "Footermenu" Module on Home page/SLP via CMS
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Menus>Footer Menu
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_go_to_menu_gtfooter_menu_gtclick_on_existing_footer_menu(self):
        """
        DESCRIPTION: Go to Menu &gt;footer menu &gt;click on existing footer menu
        EXPECTED: Footer menu details page is opened
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
        EXPECTED: a)Existing Footer menu  is active
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_005_load_oxygen_app_and_verify_footer_menu(self):
        """
        DESCRIPTION: Load Oxygen app and verify Footer menu
        EXPECTED: Footer menu  is displayed on Front End
        """
        pass

    def test_006_go_back_to_the_same__unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same , unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Footer menu  is inactive
        EXPECTED: b)Changes is saved successfully
        """
        pass

    def test_007_load_oxygen_app_and_verify_footer_menu(self):
        """
        DESCRIPTION: Load Oxygen app and verify Footer menu
        EXPECTED: Footer menu is NOT displayed on FrontEnd which is inactive.
        EXPECTED: Active footermenu should display
        """
        pass
