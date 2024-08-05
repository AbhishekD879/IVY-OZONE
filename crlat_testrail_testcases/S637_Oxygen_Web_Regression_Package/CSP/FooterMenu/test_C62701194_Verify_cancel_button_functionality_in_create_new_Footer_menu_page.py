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
class Test_C62701194_Verify_cancel_button_functionality_in_create_new_Footer_menu_page(Common):
    """
    TR_ID: C62701194
    NAME: Verify cancel button functionality in create new Footer menu page
    DESCRIPTION: This test case verifies cancel process while creating new Footer menu.
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

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_click_on_footer_menu__link(self):
        """
        DESCRIPTION: Click on Footer menu  link.
        EXPECTED: User should be able to view Create  Footer menu CTA and exixting Footer menus should be displayed.
        """
        pass

    def test_004_click_on_create_footer_menu_cta(self):
        """
        DESCRIPTION: Click on create Footer menu CTA.
        EXPECTED: On creating new record, user should redirect to module screen
        """
        pass

    def test_005_click_on_cancel_button(self):
        """
        DESCRIPTION: Click on cancel button.
        EXPECTED: User should able to cancel the creation process.
        """
        pass
