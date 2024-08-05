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
class Test_C62701193_Verify_Edit_Remove_for_existing_footer_menu(Common):
    """
    TR_ID: C62701193
    NAME: Verify Edit/Remove for existing footer menu
    DESCRIPTION: This test case verifies updating existing footer menu
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > Menus > footer menus
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
        DESCRIPTION: Go to menu &gt;footer menu &gt;click on existing footer menu
        EXPECTED: Footer menu details page is opened
        """
        pass

    def test_003_change_title_for_existing_footer_menu_button_and_save_changes(self):
        """
        DESCRIPTION: Change title for existing Footer menu button and save changes.
        EXPECTED: Changes are saved successfully.Footer menu item should update with universal/segment
        """
        pass

    def test_004_load_oxygen_app_go_to_the_page_where_footer_menu_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Footer menu is set up
        EXPECTED: Title of Footer menu is updated according to changes without page refresh
        """
        pass

    def test_005_load_cms_change_svg_icon_option_for_existing_footer_menu_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change SVG icon option for existing Footer menu and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app_go_to_the_page_where_footer_menu_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Footer menu is set up
        EXPECTED: SVG icon option for existing Footer menu  is updated according to changes without page refresh
        """
        pass

    def test_007_load_cms_change_activeinactive_option_for_existing__and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change active/inactive option for existing  and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_remove_exisiting_footer_menu_verify_in_application(self):
        """
        DESCRIPTION: Remove exisiting footer menu ,verify in application
        EXPECTED: User should able to remove ,should be remove from application.
        """
        pass
