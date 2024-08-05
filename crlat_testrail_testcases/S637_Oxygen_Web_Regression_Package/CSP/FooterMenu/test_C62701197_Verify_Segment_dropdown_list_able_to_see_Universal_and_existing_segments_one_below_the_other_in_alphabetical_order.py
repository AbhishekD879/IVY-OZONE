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
class Test_C62701197_Verify_Segment_dropdown_list_able_to_see_Universal_and_existing_segments_one_below_the_other_in_alphabetical_order(Common):
    """
    TR_ID: C62701197
    NAME: Verify Segment dropdown list, able to see Universal and existing segments one below the other in alphabetical order.
    DESCRIPTION: This test case verifies order of in the segment dropdown list
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: CMS configuration&gt;
    PRECONDITIONS: CMS &gt; Menus &gt; Footer menu.
    PRECONDITIONS: 2)Should have some footer menu for Universal and segments
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

    def test_003_click_on_footer_menu_link(self):
        """
        DESCRIPTION: click on Footer Menu link.
        EXPECTED: User should be able to view existing Footer Menus should be displayed.
        """
        pass

    def test_004_click_on_segment_dropdown_and_verify_universal_segments_order(self):
        """
        DESCRIPTION: Click on segment dropdown and verify universal ,segments order
        EXPECTED: segment dropdown list should show Universal first and other segments should be in alphabetical order.
        """
        pass
