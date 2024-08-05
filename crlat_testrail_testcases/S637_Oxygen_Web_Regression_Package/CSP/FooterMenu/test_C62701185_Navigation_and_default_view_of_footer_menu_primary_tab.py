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
class Test_C62701185_Navigation_and_default_view_of_footer_menu_primary_tab(Common):
    """
    TR_ID: C62701185
    NAME: Navigation and default view of footer menu (primary tab)
    DESCRIPTION: This test case verifies navigation and default view  of footer menu
    PRECONDITIONS: 1) User should have admin access to CMS.
    PRECONDITIONS: 2) CMS configuration for footer menu has to created
    PRECONDITIONS: CMS > Menu > footer menus
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_go_to_menu__gt_footer_menues(self):
        """
        DESCRIPTION: Go to Menu -&gt; footer menues
        EXPECTED: User should be able to see the Primary Tab Module page with exisiting Universal footer menu records
        EXPECTED: Existing footer menus should be displayed in tabular format with below feilds
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
