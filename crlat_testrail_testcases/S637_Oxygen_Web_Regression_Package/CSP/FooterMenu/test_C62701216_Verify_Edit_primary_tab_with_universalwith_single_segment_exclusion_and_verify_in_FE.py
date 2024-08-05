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
class Test_C62701216_Verify_Edit_primary_tab_with_universalwith_single_segment_exclusion_and_verify_in_FE(Common):
    """
    TR_ID: C62701216
    NAME: Verify Edit primary tab with universal(with single segment exclusion) and verify in FE
    DESCRIPTION: This test case verifies editing of existing Universal segmented Footer menu
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: CMS configuration&gt;
    PRECONDITIONS: CMS &gt; Menus &gt; Footer menu
    PRECONDITIONS: 2)Create a Universal Footer menu (without segment exclusion )
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_module_from_precondition(self):
        """
        DESCRIPTION: Navigate to module from precondition
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_footer_menu_link(self):
        """
        DESCRIPTION: Click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus should be displayed.
        """
        pass

    def test_004_click_on_existing_footer_menu_with_segment_exclusion(self):
        """
        DESCRIPTION: Click on existing Footer menu with segment exclusion
        EXPECTED: Footer menu detail page should be opened  with universal and segment(s) exclusion text box
        """
        pass

    def test_005_edit_exisiting_footer_menu(self):
        """
        DESCRIPTION: Edit exisiting Footer menu
        EXPECTED: Add segments in segment(s) exclusion text box
        """
        pass

    def test_006_click_on_save_changes_button(self):
        """
        DESCRIPTION: Click on save changes button
        EXPECTED: Footer menu should be update successfully.
        """
        pass

    def test_007_load_oxygen_and_verify_footer_menu(self):
        """
        DESCRIPTION: Load oxygen and verify footer menu
        EXPECTED: Updated Footer menu should be shown for
        EXPECTED: 1.Universal (not segmented) users
        EXPECTED: 2.Loggedout User
        EXPECTED: 3.All segmented users except segment which is mentioned in the segment(s) exclusion text box
        """
        pass
