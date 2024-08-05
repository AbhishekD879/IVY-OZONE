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
class Test_C62701192_Verify_Primary_tabsFooter_menu_display_on_page_load_in_CMS(Common):
    """
    TR_ID: C62701192
    NAME: Verify Primary tabs(Footer menu)  display on page load in CMS
    DESCRIPTION: This test case verifies display of Primary tab(Footer menu) module page in CMS
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

    def test_002_go_to_menu_gt_footer_menus(self):
        """
        DESCRIPTION: Go to Menu &gt; footer menus
        EXPECTED: User should be able to view the Primary Tab Module page
        """
        pass

    def test_003_verify_footermenues_page(self):
        """
        DESCRIPTION: Verify FooterMenues page
        EXPECTED: The Primary Tab Module page as per the designs below
        EXPECTED: Create Footer Menu
        EXPECTED: Segment
        EXPECTED: Download CSV
        EXPECTED: Search field
        """
        pass

    def test_004_verify_segment_dropdown(self):
        """
        DESCRIPTION: Verify Segment dropdown
        EXPECTED: The dropdown will show all the segments,Segmented drop down should Universal is highlighted by default
        """
        pass

    def test_005_verify_segment_dropdown_defaulted_by_universal(self):
        """
        DESCRIPTION: Verify Segment dropdown defaulted by Universal
        EXPECTED: Should display Universal records by default
        """
        pass
