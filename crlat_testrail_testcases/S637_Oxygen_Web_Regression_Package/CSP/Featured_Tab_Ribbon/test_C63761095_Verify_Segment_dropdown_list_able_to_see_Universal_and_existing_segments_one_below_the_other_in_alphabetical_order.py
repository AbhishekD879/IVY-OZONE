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
class Test_C63761095_Verify_Segment_dropdown_list_able_to_see_Universal_and_existing_segments_one_below_the_other_in_alphabetical_order(Common):
    """
    TR_ID: C63761095
    NAME: Verify Segment dropdown list, able to see Universal and existing segments one below the other in alphabetical order.
    DESCRIPTION: This test case verifies order of in the segment dropdown list
    PRECONDITIONS: 1) "User should have admin access to CMS.
    PRECONDITIONS: CMS configuration&gt;
    PRECONDITIONS: CMS &gt; Module ribbon tab
    PRECONDITIONS: 2) Should have some Module ribbon tab for Universal and segments
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

    def test_003_click_on_module_ribbon_tab_link(self):
        """
        DESCRIPTION: click on Module ribbon tab link.
        EXPECTED: User should be able to view existing Module ribbon tabs should be displayed.
        """
        pass

    def test_004_click_on_segment_dropdown_and_verify_universal_segments_order(self):
        """
        DESCRIPTION: Click on segment dropdown and verify universal ,segments order
        EXPECTED: a) segment dropdown list should show Universal first and other segments should be in alphabetical order.
        EXPECTED: B) if user select any segment from drop down list the Module ribbon tabs in that segment should display in alphabetical order.
        EXPECTED: C) If we remove all Module ribbon tabs of any segment it should not display in drop down
        """
        pass
