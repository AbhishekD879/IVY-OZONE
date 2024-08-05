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
class Test_C62701189_On_successful_creation_page_should_navigate_to_the_Primary_Tab_ModuleFooter_menu_page(Common):
    """
    TR_ID: C62701189
    NAME: On successful creation, page should navigate to the Primary Tab Module(Footer menu ) page
    DESCRIPTION: This test case verifies page navigation after successful creation to the Primary Tab Module page
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

    def test_002_go_to_menu_gt_footer_menus(self):
        """
        DESCRIPTION: Go to Menu &gt; footer menus
        EXPECTED: User should be navigated successfully.
        """
        pass

    def test_003_verify_footermenu_page(self):
        """
        DESCRIPTION: Verify FooterMenu page
        EXPECTED: Existing footer menus should be displayed in tabular format  with below feilds
        EXPECTED: Link Title
        EXPECTED: Segment(s)
        EXPECTED: Segment(s) Exclusion
        EXPECTED: Item Type
        EXPECTED: Target URI
        EXPECTED: In App
        EXPECTED: Show Item for
        EXPECTED: Mobile
        EXPECTED: Tablet
        EXPECTED: Desktop
        EXPECTED: Auth required
        EXPECTED: Remove
        """
        pass

    def test_004_click_on_create_footermenu_button(self):
        """
        DESCRIPTION: Click on Create FooterMenu button
        EXPECTED: a) User should be able to view Create FooterMenu CTA.
        EXPECTED: b)Upon clicking Create FooterMenu CTA, Link Tiltle, Traget URI pop up should display with Save and Close buttons
        """
        pass

    def test_005_verify_navigation_after_creation_of_footer_menu(self):
        """
        DESCRIPTION: Verify navigation after creation of Footer menu
        EXPECTED: After creating new record page should navigate to the Footer menu page
        """
        pass
